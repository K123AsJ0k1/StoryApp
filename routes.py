from app import app
import re
from flask import redirect, render_template, request, session
from os import getenv

from users_db import *
from posts_db import *
from chapters_db import *
from comments_db import *
from queries_db import *
from answers_db import *

from users_logic import *
from main_page_logic import *
from profile_logic import *
from workbench_logic import *
from view_logic import *
from comments_logic import *
from query_logic import *

app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def main_page():
   main_page_session_deletion()
   
   posts = get_public_posts()
   size = len(posts)

   post_creators = {}

   for post in posts:
      post_creator = get_post_creator(post[0])
      post_creators[post[0]] = post_creator

   posts_have_chapters = {}

   for post in posts:
      has_chapters = check_post_chapters(post[0])
      posts_have_chapters[post[0]] = has_chapters

   return render_template("main.html", posts=posts, size=size, post_creators=post_creators, owns_chapters=posts_have_chapters)

@app.route("/signup", methods=["get","post"])
def signup():
   if request.method == "GET":
      return render_template("signup.html") 
    
   if request.method == "POST":
      username = request.form["username"]
      password = request.form["password"]

      if not register(username,password):
         return render_template("signup.html")
         
      return redirect("/")

@app.route("/login", methods=["get","post"])
def login():
   if request.method == "GET":
      return render_template("login.html")

   if request.method == "POST":
      username = request.form["username"]
      password = request.form["password"]

      if not log_in(username, password):
         return render_template("login.html")

      return redirect("/")

@app.route("/logout")
def logout():
   session.clear()
   return redirect("/")

@app.route("/profile/<string:user_name>")
def profile(user_name):
   profile_session_deletion()
   user_id = get_user_id(user_name)
   posts = get_profile_posts(user_id)
   size = len(posts)
   
   posts_have_chapters = {}

   for post in posts:
      has_chapters = check_post_chapters(post[0])
      posts_have_chapters[post[0]] = has_chapters

   if not check_user():
      return redirect("/")

   return render_template("profile.html", user_name=user_name, posts=posts, size=size, owns_chapters=posts_have_chapters)

@app.route("/workbench/save/<string:mode>", methods=["get","post"])
def workbench_save(mode):
   #Luo creator_name, post_name, post_id ja chapter_number tarkastus
   if not check_user():
      return redirect("/")
   
   if mode == "create_post" and request.method == "GET":
      workbench_post_mode()   
      return render_template("workbench.html")

   if mode == "save_post" and request.method == "POST":
      user_id = session["user_id"]
      public = request.form["public"]
      general_comments = request.form["general"]
      name = request.form["name"]
      rating = request.form["rating"]
      genre = request.form["genre"]
      
      if not save_post(user_id,public,general_comments,name,rating,genre):
         return render_template("workbench.html") 
      
      user_name = session["user_name"]
      address = "/profile" + user_name
      return redirect(address)

   if mode == "create_chapter" and request.method == "GET":
      workbench_chapter_mode()
      posts = get_profile_posts(session["user_id"])
      size = len(posts)
      return render_template("workbench.html", posts=posts, size=size)

   if mode == "save_chapter" and request.method == "POST":
      post_id = request.form["chapter_picked_post"]
      chapter_public = request.form["chapter_public"]
      row_comments = request.form["chapter_row_comments_on"]
      inquiry = request.form["chapter_inquiry"]
      text_content = request.form["chapter_text"]

      if not save_chapter(post_id, chapter_public, row_comments, inquiry, text_content):
         return render_template("workbench.html") 
      
      user_name = session["user_name"]
      address = "/profile/" + user_name
      return redirect(address)

@app.route("/workbench/update/<string:mode>/<int:post_id>/<int:chapter_number>", methods=["get","post"])
def workbench_update(mode, post_id, chapter_number):
   #Luo creator_name, post_name, post_id ja chapter_number tarkastus
   if not check_user():
      return redirect("/")
   
   if mode == "change_post" and post_id > 0 and request.method == "GET":
      get_post(post_id)
      return render_template("workbench.html", post_id=post_id)

   if mode == "update_post" and post_id > 0 and request.method == "POST":
      old_name = session["given_post_name"]
      user_id = session["user_id"]
      public = request.form["public"]
      general_comments = request.form["general"]
      new_name = request.form["name"]
      rating = request.form["rating"]
      genre = request.form["genre"]
      
      if not update_post(old_name, user_id, public, general_comments, new_name, rating, genre):
         return render_template("workbench.html")
      
      user_name = session["user_name"]
      address = "/profile/" + user_name
      return redirect(address)

@app.route("/workbench/remove/<string:mode>/<int:post_id>/<int:chapter_number>")
def workbench_remove(mode, post_id, chapter_number):
   #Luo creator_name, post_name, post_id ja chapter_number tarkastus
   if not check_user():
      return redirect("/")

   if mode == "remove_post" and post_id > 0:
      user_id = session["user_id"]
      
      if not remove_post(user_id,post_id):
         user_name = session["user_name"]
         address = "/profile/" + user_name
         return redirect(address)
      
      user_name = session["user_name"]
      address = "/profile/" + user_name
      return redirect(address)

   if mode == "remove_chapter" and post_id > 0 and chapter_number > 0:
      if not remove_chapter(post_id,chapter_number):
         user_name = session["user_name"]
         address = "/profile/" + user_name
         return redirect(address)
      
      remove_chapter_content_session()
      user_name = session["user_name"]
      address = "/profile/" + user_name
      return redirect(address)

@app.route("/view/<string:creator_name>/<string:post_name>/<int:chapter_number>")
def view(creator_name, post_name, chapter_number):
   if not view_chapter(creator_name, post_name, chapter_number):
       view_none_mode()
       return render_template("view.html")
   view_read_mode()
   return render_template("view.html", creator_name=creator_name, post_name=post_name, chapter_number=chapter_number)

@app.route("/view/<int:post_id>/<string:post_name>")
def redirect_into_view(post_id,post_name):
   creator_name = get_post_creator(post_id)
   address = "/view/" + creator_name + "/"+ post_name +"/1"
   return redirect(address)

@app.route("/comments/general/<string:creator_name>/<string:post_name>/<int:post_id>")
def comments_general(creator_name, post_name, post_id):
   #Luo creator_name, post_name, post_id tarkastus

   comments = get_post_general_comments(post_id)
   
   if len(comments) == 0:
      comment_view_mode()
      return render_template("comments.html", creator_name=creator_name, post_name=post_name, post_id=post_id, size=0)
   
   comment_creators = {}

   for comment in comments:
       comment_creators[comment[0]] = get_comment_creator(comment[0])

   if len(comment_creators) == 0:
      comment_view_mode()
      return render_template("comments.html", creator_name=creator_name, post_name=post_name, post_id=post_id, size=0)
   
   size = len(comments)
   comment_view_mode()
   return render_template("comments.html", creator_name=creator_name, post_name=post_name, post_id=post_id, comments=comments, comment_creators=comment_creators, size=size)

@app.route("/comments/save/<string:mode>/<string:creator_name>/<string:post_name>/<int:post_id>/<int:chapter_number>", methods=["get","post"])
def comments_save(mode, creator_name, post_name, post_id, chapter_number):
   #Luo creator_name, post_name, post_id ja chapter_number tarkastus
   if not check_user():
      return redirect("/")
   
   if mode == "create_general_comment" and request.method == "GET" and post_id > 0:
      comment_creation_mode()
      last_chapter = get_the_next_chapter_number(post_id)-1
      return render_template("comments.html", creator_name=creator_name, post_name=post_name, post_id=post_id, last_chapter=last_chapter)
   
   if mode == "save_general_comment" and request.method == "POST" and post_id > 0:
      user_id = session["user_id"]
      comment = request.form["comment_text"]
      referenced_chapter = request.form["referenced_chapter_number"]
      
      if not save_general_comment(post_id,user_id,comment,referenced_chapter):
         address = "/comments/save/create_general_comment/" + creator_name + "/" + post_name + "/" + str(post_id) + "/" + str(chapter_number)
         return redirect(address)
      
      address = "/comments/general/"+ creator_name + "/"+ post_name +"/" + str(post_id)
      return redirect(address)

@app.route("/comment/remove/<string:mode>/<string:creator_name>/<string:post_name>/<int:post_id>/<int:chapter_number>/<int:comment_id>")
def comment_remove(mode, creator_name, post_name, post_id, chapter_number, comment_id):
   #Luo creator_name, post_name, post_id ja chapter_number tarkastus
   if not check_user():
      return redirect("/")
   
   if mode == "remove_general_comment" and post_id > 0 and comment_id > 0:
      if not remove_comment(comment_id):
         address = "/comments/general/" + creator_name + "/" + post_name + "/" + str(post_id)
         return redirect(address)
      address = "/comments/general/" + creator_name + "/" + post_name + "/" + str(post_id)
      return redirect(address)

@app.route("/query/<string:mode>/<string:creator_name>/<string:post_name>/<int:post_id>/<int:chapter_number>/<int:query_id>")
def query(mode, creator_name, post_name, post_id, chapter_number, query_id):
   #Luo creator_name, post_name, post_id ja chapter_number tarkastus
   if not check_user():
      return redirect("/")
   
   if mode == "view_questions":
      post = get_the_post(post_id)

      if post == None:
         query_none_mode()
         return render_template("queries.html")

      chapter = get_the_chapter(post_id,chapter_number)

      if chapter == None:
         query_none_mode()
         return render_template("queries.html")

      queries = get_the_chapter_queries(chapter[0])

      if queries == -1:
         query_none_mode()
         return render_template("queries.html")

      if queries == -2:
         query_none_mode()
         return render_template("queries.html")

      size = len(queries)
      query_view_mode()
      return render_template("queries.html", creator_name=creator_name, post_name=post_name, post_id=post_id, chapter_number=chapter_number, queries=queries, size=size)
   
   if mode == "view_answers":
      post = get_the_post(post_id)

      if post == None:
         query_none_mode()
         return render_template("queries.html")

      answers = get_the_query_answers(query_id)

      if answers == -1:
         query_none_mode()
         return render_template("queries.html")

      if answers == -2:
         query_none_mode()
         return render_template("queries.html")
   
      if len(answers) == 0:
         query_answers_mode()
         return render_template("queries.html", creator_name=creator_name, post_name=post_name, post_id=post_id, chapter_number=chapter_number, size=0)

      answer_creators = {}

      for answer in answers:
         answer_creators[answer[0]] = get_answer_creator(answer[0])
   
      if len(answer_creators) == 0:
         query_answers_mode()
         return render_template("queries.html", creator_name=creator_name, post_name=post_name, post_id=post_id, chapter_number=chapter_number, size=0)
   
      the_amount_of_answers = len(answers)
      query_answers_mode()
      return render_template("queries.html", creator_name=creator_name, post_name=post_name, post_id=post_id, chapter_number=chapter_number, size=the_amount_of_answers, answers=answers, answer_creators=answer_creators)


@app.route("/query/save/<string:mode>/<string:creator_name>/<string:post_name>/<int:post_id>/<int:chapter_number>/<int:query_id>", methods=["get","post"])
def query_save(mode,creator_name,post_name,post_id,chapter_number,query_id):
   #Luo creator_name, post_name, post_id ja chapter_number tarkastus
   if not check_user():
      return redirect("/")

   if mode == "create_question" and post_id > 0 and request.method == "GET": 
      query_create_mode()
      return render_template("queries.html", creator_name=creator_name, post_name=post_name, post_id=post_id, chapter_number=chapter_number)
   
   if mode == "save_question" and post_id > 0 and request.method == "POST":
      user_id = session["user_id"]
      question = request.form["question"]
      
      if not save_question(user_id,post_id,chapter_number,question):
         address = "/query/save/create_question/" + creator_name + "/" + post_name + "/" + str(post_id) + "/" + str(chapter_number) + "/" + str(0)
         return redirect(address)
      
      address = "/query/view_questions/" + creator_name + "/" + post_name + "/" + str(post_id) + "/" + str(chapter_number) + "/" + str(0)
      return redirect(address)

   if mode == "create_answer" and query_id > 0 and request.method == "GET": 
      query_answer_mode()
      query = get_the_query(query_id)
      
      if query == None:
         query_none_mode()
         return render_template("queries.html")

      question = query[3]
      return render_template("queries.html", creator_name=creator_name, post_name=post_name, post_id=post_id, chapter_number=chapter_number, query_id=query_id, question=question)
   
   if mode == "save_answer" and query_id > 0 and request.method == "POST":
      user_id = session["user_id"]
      answer = request.form["answer"]
      
      if not save_answer(user_id, query_id, answer):
         query = get_the_query(query_id)
         question = query[3]
         return render_template("queries.html", creator_name=creator_name, post_name=post_name, post_id=post_id, chapter_number=chapter_number, query_id=query_id, question=question)
      
      address = "/query/view_questions/" + creator_name + "/" + post_name + "/" + str(post_id) + "/" + str(chapter_number) + "/" + str(0)
      return redirect(address)

@app.route("/query/remove/<string:mode>/<string:creator_name>/<string:post_name>/<int:post_id>/<int:chapter_number>/<int:query_id>/<int:answer_id>")
def query_remove(mode,creator_name,post_name,post_id,chapter_number,query_id,answer_id):
   #Luo creator_name, post_name, post_id ja chapter_number tarkastus
   if not check_user():
      return redirect("/")
   
   if mode == "remove_question" and query_id > 0:
      if not remove_question(query_id):
         query_none_mode()
         return render_template("queries.html")
      address = "/query/view_questions/" + creator_name + "/" + post_name + "/" + str(post_id) + "/" + str(chapter_number) + "/" + str(0)
      return redirect(address)

   if mode == "remove_answer" and answer_id > 0:
      if not remove_answer(answer_id):
         query_none_mode()
         return render_template("queries.html")
      address = "/query/view_answers/" + creator_name + "/" + post_name + "/" + str(post_id) + "/" + str(chapter_number) + "/" + str(query_id)
      return redirect(address)
       



   






   

   

   




   


   
    

   

   

   










    



    

    
