from app import app
import re
from flask import redirect, render_template, request, session
from os import getenv

from comments_db import *
from queries_db import *
from answers_db import *

from users_logic import *
from main_page_logic import *
from profile_logic import *
from workbench_logic import *

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

@app.route("/profile")
def profile():
   profile_session_deletion()
   
   posts = get_profile_posts(session["user_id"])
   size = len(posts)
   
   posts_have_chapters = {}

   for post in posts:
      has_chapters = check_post_chapters(post[0])
      posts_have_chapters[post[0]] = has_chapters

   if not check_user():
      return redirect("/")

   return render_template("profile.html", posts=posts, size=size, owns_chapters=posts_have_chapters)

@app.route("/workbench/save/<string:mode>", methods=["get","post"])
def workbench_save(mode):
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
      return redirect("/profile")

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
      return redirect("/profile")

@app.route("/workbench/update/<string:mode>/<int:post_id>/<int:chapter_number>", methods=["get","post"])
def workbench_update(mode, post_id, chapter_number):
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
      return redirect("/profile")

@app.route("/workbench/remove/<string:mode>/<int:post_id>/<int:chapter_number>")
def workbench_remove(mode, post_id, chapter_number):
   if not check_user():
      return redirect("/")

   if mode == "remove_post" and post_id > 0:
      user_id = session["user_id"]
      remove_post(user_id,post_id)
      return redirect("/profile")
      
   if mode == "remove_chapter" and post_id > 0 and chapter_number > 0:
      remove_chapter(post_id,chapter_number)
      return redirect("/profile")

@app.route("/view/<string:creator_name>/<string:post_name>/<int:chapter_number>")
def chapter_view(creator_name, post_name, chapter_number):
   user_id = get_user_id(creator_name)
    
   if user_id == 0:
      session["view_mode"] = "0"
      session["view_error"] = "1"
      return render_template("view.html")

   post = get_profile_post(user_id, post_name)

   if post == None:
      session["view_mode"] = "0"
      session["view_error"] = "2"
      return render_template("view.html")

   post_id = post[0]

   chapter = get_the_chapter(post_id, chapter_number)

   if chapter == None:
      session["view_mode"] = "0"
      session["view_error"] = "3"
      return render_template("view.html", owns_chapters=False)
   
   chapter_content = get_source_text_array(chapter[7])
       
   # Edellinen luku, seuraava luku ja valittavat luku asiat
    
   # Row comment asiat
    
   # chapter_rows = chapter[6]

   # row_comments_on = chapter[3]

   inquiry_on = chapter[4]
   
   session["view_chapter"] = "0"

   if chapter_number == 1:
      session["view_chapter"] = "1"

   if chapter_number == get_the_next_chapter_number(post_id)-1:
      session["view_chapter"] = "2"

   if get_the_next_chapter_number(post_id) == 2:
      session["view_chapter"] = "3"
    
   session["view_mode"] = "1"
   session["view_error"] = "0"
   return render_template("view.html", creator=creator_name, story=post_name, post=post_id, owns_chapters=inquiry_on, chapter=chapter_number, text=chapter_content, previous_chapter=chapter_number-1, next_chapter=chapter_number+1)
    
@app.route("/view/<int:post_id>/<string:post_name>")
def redirect_into_chapter_view(post_id,post_name):
   creator_name = get_post_creator(post_id)
   address = "/view/" + creator_name + "/"+ post_name +"/1"
   return redirect(address)

@app.route("/comments/general/<int:post_id>/<string:post_name>")
def view_general_comments(post_id,post_name):
   post_creator = get_post_creator(post_id)
   comments = get_post_general_comments(post_id)
   
   if len(comments) == 0:
      session["comment_mode"] = "1"
      session["comment_error"] = "0"
      return render_template("comments.html", post_id=post_id, story=post_name)
   
   creators = {}

   for comment in comments:
       creator = get_comment_creator(comment[0])
       creators[comment[0]] = creator

   if len(creators) == 0:
      session["comment_mode"] = "1"
      session["comment_error"] = "1"
      return render_template("comments.html", post_id=post_id,  story=post_name)
   
   # luo parempi lista, jossa on ainoastaan kommentin luoja, kommentti, luku ja luku booleani
   session["comment_mode"] = "1"
   session["comment_error"] = "2"
   return render_template("comments.html", creator=post_creator, post_id=post_id, story=post_name, comments=comments, creators=creators)

@app.route("/create/comment/general/<int:post_id>/<string:post_name>")
def create_general_comment(post_id,post_name):
   if not check_user():
      return redirect("/")
   
   session["comment_mode"] = "2"
   session["comment_error"] = "3"
   last_chapter = get_the_next_chapter_number(post_id)-1
   return render_template("comments.html", last_chapter=last_chapter,  post_id=post_id, story=post_name)

@app.route("/save/comment/general/<int:post_id>/<string:post_name>", methods=["POST"])
def save_general_comment(post_id,post_name):
   if not check_user():
      return redirect("/")
   
   referenced_chapter = request.form["referenced_chapter_number"]
   
   chapter_list = get_the_chapter_numbers(post_id)
  
   chapter_number_on = '0'
   chapter_number = 0
   
   if referenced_chapter.isdigit(): 
      for chapter in chapter_list:
         if chapter[0] == int(referenced_chapter):
          chapter_number_on = '1'
          chapter_number = chapter[0]
   
   comment = request.form["comment_text"]
   
   if not check_text_requirements(comment):
      address = "/create/comment/general/"+ str(post_id) + "/"+ post_name
      return redirect(address)

   check_number = save_the_comment(session["user_id"], post_id, 0, '1', '0', chapter_number_on, chapter_number, comment)
   
   if check_number == -1:
      address = "/create/comment/general/"+ str(post_id) + "/"+ post_name
      return redirect(address)
   
   address = "/comments/general/"+ str(post_id) + "/"+ post_name
   return redirect(address)

@app.route("/remove/comment/general/<int:post_id>/<string:post_name>/<int:comment_id>")
def remove_general_comment(post_id, post_name, comment_id):
   if not check_user():
      return redirect("/")
   
   check_number = remove_the_comment(comment_id)

   if check_number == -1:
       address = "/comments/general/"+ str(post_id) + "/"+ post_name
       return redirect(address)

   address = "/comments/general/"+ str(post_id) + "/"+ post_name
   return redirect(address)

@app.route("/query/chapter/<int:post_id>/<int:chapter_number>")
def view_query(post_id,chapter_number):
   if not check_user():
      return redirect("/")
   
   username = get_post_creator(post_id)
   
   if username == None:
      session["query_mode"] = "0"
      session["query_error"] = "1"
      return render_template("queries.html")

   post = get_the_post(post_id)

   if post == None:
      session["query_mode"] = "0"
      session["query_error"] = "2"
      return render_template("queries.html")

   chapter = get_the_chapter(post_id,chapter_number)

   if chapter == None:
      session["query_mode"] = "0"
      session["query_error"] = "3"
      return render_template("queries.html")
   
   queries = get_the_chapter_queries(chapter[0])
   size = len(queries)

   if queries == -1:
      session["query_mode"] = "0"
      session["query_error"] = "4"
      return render_template("queries.html")

   if queries == -2:
      session["query_mode"] = "0"
      session["query_error"] = "5"
      return render_template("queries.html")

   session["query_mode"] = "1"
   session["query_error"] = "0"
   return render_template("queries.html", creator=username, story=post[4], post=post[0], chapter=chapter_number, queries=queries, size=size)

@app.route("/create/question/<int:post_id>/<int:chapter_number>")
def create_question(post_id,chapter_number):
   if not check_user():
      return redirect("/")
   
   post = get_the_post(post_id)

   if post == None:
      session["query_mode"] = "0"
      session["query_error"] = "2"
      return render_template("queries.html")

   session["query_mode"] = "2"
   session["query_error"] = "0"
   return render_template("queries.html", post=post[0], story=post[4], chapter=chapter_number)

@app.route("/save/question/<int:post_id>/<int:chapter_number>", methods=["POST"])
def save_question(post_id,chapter_number):
   if not check_user():
      return redirect("/")
   
   post = get_the_post(post_id)

   if post == None:
      session["query_mode"] = "0"
      session["query_error"] = "2"
      return render_template("queries.html")
   
   user_id = post[1]
   
   chapter = get_the_chapter(post_id,chapter_number)

   if chapter == None:
      session["query_mode"] = "0"
      session["query_error"] = "3"
      return render_template("queries.html")

   chapter_id = chapter[0]

   question = request.form["question"]

   if not check_text_requirements(question):
      session["query_mode"] = "2"
      session["query_error"] = "0"
      address = "/create/question/" + str(post_id) + "/" + str(chapter_number)
      return redirect(address)

   misc = ""

   check_number = save_the_query(user_id,chapter_id,question,misc)

   if check_number == -2:
      session["query_mode"] = "0"
      session["query_error"] = "5"
      return render_template("queries.html")
   
   address = "/query/chapter/" + str(post_id) + "/" + str(chapter_number)
   return redirect(address)

@app.route("/remove/question/<int:post_id>/<int:chapter_number>/<int:question_id>")
def remove_question(post_id, chapter_number, question_id):
   if not check_user():
      return redirect("/")
   
   check_number = remove_the_query(question_id)

   if check_number == -2:
      session["query_mode"] = "0"
      session["query_error"] = "5"
      return render_template("queries.html")

   address = "/query/chapter/" + str(post_id) + "/" + str(chapter_number)
   return redirect(address)

@app.route("/query/chapter/answers/<int:post_id>/<int:chapter_number>/<int:query_id>")
def view_answers_to_the_question(post_id,chapter_number,query_id):
   if not check_user():
      return redirect("/")
   
   username = get_post_creator(post_id)
   
   if username == None:
      session["query_mode"] = "0"
      session["query_error"] = "1"
      return render_template("queries.html")

   post = get_the_post(post_id)

   if post == None:
      session["query_mode"] = "0"
      session["query_error"] = "2"
      return render_template("queries.html")

   answers = get_the_query_answers(query_id)

   if answers == -1:
      session["query_mode"] = "0"
      session["query_error"] = "6"
      return render_template("queries.html")

   if answers == -2:
      session["query_mode"] = "0"
      session["query_error"] = "7"
      return render_template("queries.html")
   
   if len(answers) == 0:
      session["query_mode"] = "3"
      session["query_error"] = "0"
      return render_template("queries.html", creator=username, post=post_id, story=post[4], chapter=chapter_number, size=0)

   creators = {}

   for answer in answers:
       creator = get_answer_creator(answer[0])
       creators[answer[0]] = creator
   
   if len(creators) == 0:
      session["query_mode"] = "3"
      session["query_error"] = "8"
      return render_template("queries.html")
   
   the_amount_of_answers = len(answers)
   session["query_mode"] = "3"
   session["query_error"] = "0"
   return render_template("queries.html", creator=username, post=post_id, story=post[4], query_id=query_id, chapter=chapter_number, size=the_amount_of_answers, answers=answers, creators=creators)

@app.route("/create/answer/<int:post_id>/<int:chapter_number>/<query_id>")
def create_answer_to_the_question(post_id,chapter_number,query_id):
   if not check_user():
      return redirect("/")
   
   query = get_the_query(query_id)
   
   if query == None:
      session["query_mode"] = "0"
      session["query_error"] = "5"
      return render_template("queries.html")
   
   question = query[3]
   
   session["query_mode"] = "4"
   session["query_error"] = "0"
   return render_template("queries.html", question=question, post=post_id, query_id=query_id, chapter=chapter_number)

@app.route("/save/answer/<int:post_id>/<int:chapter_number>/<query_id>", methods=["POST"])
def save_the_answer_to_the_question(post_id,chapter_number,query_id):
   if not check_user():
      return redirect("/")
   
   query = get_the_query(query_id)
   
   if query == None:
      session["query_mode"] = "0"
      session["query_error"] = "5"
      return render_template("queries.html")
   
   question = query[3]

   answer = request.form["answer"]

   if not check_text_requirements(answer):
      session["query_mode"] = "4"
      #Luo errori
      return render_template("queries.html", question=question, post=post_id, query_id=query_id, chapter=chapter_number)

   misc = ""

   check_number = save_the_answer(session["user_id"], query_id, answer, misc)

   if check_number == -2:
      session["query_mode"] = "0"
      session["query_error"] = "7"
      return render_template("queries.html")

   address = "/query/chapter/" + str(post_id) + "/" + str(chapter_number)
   return redirect(address)

@app.route("/remove/answer/<int:post_id>/<int:chapter_number>/<int:query_id>/<answer_id>")
def remove_the_answer_to_the_question(post_id,chapter_number,query_id,answer_id):
   if not check_user():
      return redirect("/")
   
   check_number = remove_the_answer(answer_id)

   if check_number == -2:
      session["query_mode"] = "0"
      session["query_error"] = "7"
      return render_template("queries.html")
   
   address = "/query/chapter/answers/" + str(post_id) + "/" + str(chapter_number) + "/" + str(query_id)
   return redirect(address)
   



   






   

   

   




   


   
    

   

   

   










    



    

    
