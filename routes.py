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
from administration_logic import *

app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def main_page():
   main_page_other_page_session_deletion()

   if get_clearance_proxy() == None:
      if not create_clearance_proxy():
         main_page_proxy_init_problem()

   if 'user_role' in session:
      if session["user_role"] == 2:
         address = "/administration/" + session["user_name"]
         return redirect(address)

   posts = get_public_posts()
   
   if posts == None:
      return render_template("main.html", size=0)
   
   if len(posts) == 0:
      return render_template("main.html", size=0)

   ratings = get_post_ratings()
   
   if ratings == None:
      return render_template("main.html", size=0)
   
   if len(ratings) == 0:
      return render_template("main.html", size=0)

   genres = get_post_genres()
   
   if genres == None:
      return render_template("main.html", size=0)

   if len(genres) == 0:
      return render_template("main.html", size=0)
   
   size = len(posts)

   post_creators = {}

   for post in posts:
      post_creator = get_post_creator(post[0])
      post_creators[post[0]] = post_creator

   posts_have_chapters = {}

   for post in posts:
      has_chapters = check_post_chapters(post[0])
      posts_have_chapters[post[0]] = has_chapters

   return render_template("main.html", posts=posts, size=size, post_creators=post_creators, owns_chapters=posts_have_chapters, ratings=ratings, genres=genres)

@app.route("/signup/<string:mode>", methods=["get","post"])
def signup(mode):
   if mode == "create_user" and request.method == "GET":
      sign_up_user_mode()
      return render_template("signup.html") 
    
   if mode == "register_user" and request.method == "POST":
      username = request.form["username"]
      password = request.form["password"]

      if not register(mode,username,password,""):
         address = "/signup/create_user"
         return redirect(address)

      sign_up_session_deletion()
      return redirect("/")

   if mode == "create_admin" and request.method == "GET":
      sign_up_admin_mode()
      return render_template("signup.html") 
   
   if mode == "register_admin" and request.method == "POST":
      username = request.form["admin_name"]
      password = request.form["admin_password"]
      clearance_code = request.form["clearance_code"]

      if not register(mode,username,password,clearance_code):
         address = "/signup/create_admin"
         return redirect(address)
      sign_up_session_deletion()
      return redirect("/administration/" + session["user_name"])
   sign_up_session_deletion()
   return redirect("/")
      
@app.route("/login/<string:mode>", methods=["get","post"])
def login(mode):
   if mode == "log_in_user" and request.method == "GET":
      log_in_user_mode()
      return render_template("login.html")

   if mode == "check_user" and request.method == "POST":
      username = request.form["username"]
      password = request.form["password"]

      if not log_in(mode,username, password):
         address = "/login/log_in_user"
         return redirect(address)
      log_in_session_deletion()
      return redirect("/")
   
   if mode == "log_in_admin" and request.method == "GET":
      log_in_admin_mode()
      return render_template("login.html")

   if mode == "check_admin" and request.method == "POST":
      username = request.form["admin_name"]
      password = request.form["admin_password"]

      if not log_in(mode,username, password):
         address = "/login/log_in_admin"
         return redirect(address)
      
      log_in_session_deletion()
      address = "/administration/" + username
      return redirect(address)
   log_in_session_deletion()
   return redirect("/")

@app.route("/logout")
def logout():
   session.clear()
   return redirect("/")

@app.route("/administration/<string:admin_name>")
def administration(admin_name):
   if not check_user():
      return redirect("/")
   
   if not session["user_role"] == 2:
      return redirect("/")
   
   admin_session_deletion()
   admin_main_mode()
   return render_template("administration.html", admin_name=admin_name)
   
@app.route("/administration/users/<string:admin_name>")
def administration_users(admin_name):
   if not check_user():
      return redirect("/")
   
   if not session["user_role"] == 2:
      return redirect("/")

   users = get_users()
   
   if users == None:
      address = "/administration/" + admin_name
      return redirect(address)

   if len(users) == 0:
      address = "/administration/" + admin_name
      return redirect(address)

   amount_of_regulars = get_regulars_amount()
   amount_of_admins = get_admins_amount()
   
   admin_users_mode()
   return render_template("administration.html", admin_name=admin_name, users=users, amount_of_regulars=amount_of_regulars, amount_of_admins=amount_of_admins)

@app.route("/administration/posts/<string:admin_name>")
def administration_posts(admin_name):
   if not check_user():
      return redirect("/")
   
   if not session["user_role"] == 2:
      return redirect("/")

   posts = get_posts()

   if posts == None:
      address = "/administration/" + admin_name
      return redirect(address)
   
   if len(posts) == 0:
      address = "/administration/" + admin_name
      return redirect(address)

   post_creators = get_post_creators()

   if post_creators == None:
      address = "/administration/" + admin_name
      return redirect(address)

   if len(post_creators) == 0:
      address = "/administration/" + admin_name
      return redirect(address)

   amount_of_posts = get_posts_amount()
   amount_of_public_posts = get_public_post_amount()

   admin_posts_mode()
   return render_template("administration.html", admin_name=admin_name, posts=posts, post_creators=post_creators, amount_of_posts=amount_of_posts, amount_of_public_posts=amount_of_public_posts)

@app.route("/administration/chapters/<string:admin_name>")
def administration_chapters(admin_name):
   if not check_user():
      return redirect("/")
   
   if not session["user_role"] == 2:
      return redirect("/")
    
   chapters = get_chapters()

   if chapters == None:
      address = "/administration/" + admin_name
      return redirect(address)
      
   if len(chapters) == 0:
      address = "/administration/" + admin_name
      return redirect(address)

   chapter_post_list = get_chapter_posts()

   if chapter_post_list == None:
      address = "/administration/" + admin_name
      return redirect(address)

   if len(chapter_post_list) == 0:
      address = "/administration/" + admin_name
      return redirect(address)
   
   amount_of_chapters = get_chapters_amount()
   amount_of_public_chapters = get_public_chapters_amount()
   largest_chapter_number = get_largest_chapter_number()
   largest_row_number = get_largest_row_amount()
   
   admin_chapters_mode()
   return render_template("administration.html", admin_name=admin_name, chapters=chapters, chapter_post_list=chapter_post_list,  amount_of_chapters=amount_of_chapters, amount_of_public_chapters=amount_of_public_chapters, largest_chapter_number=largest_chapter_number, largest_row_number=largest_row_number)

@app.route("/administration/comments/<string:admin_name>")
def administration_comments(admin_name):
   if not check_user():
      return redirect("/")
   
   if not session["user_role"] == 2:
      return redirect("/")

   comments = get_comments()

   if comments == None:
      address = "/administration/" + admin_name
      return redirect(address)

   if len(comments) == 0:
      address = "/administration/" + admin_name
      return redirect(address)

   comment_creators = get_comment_creators()
   
   if comment_creators == None:
      address = "/administration/" + admin_name
      return redirect(address)

   if len(comment_creators) == 0:
      address = "/administration/" + admin_name
      return redirect(address)

   comment_post_list = get_comment_posts()
   
   if comment_post_list == None:
      address = "/administration/" + admin_name
      return redirect(address)

   if len(comment_post_list) == 0:
      address = "/administration/" + admin_name
      return redirect(address)

   amount_of_general_comments = get_general_comment_amount()
   amount_of_row_subjects = get_row_subject_amount()
   amount_of_row_subject_comments = get_row_subject_comment_amount()
   
   admin_comments_mode()
   return render_template("administration.html", admin_name=admin_name, comments=comments, comment_creators=comment_creators, comment_post_list=comment_post_list, amount_of_general_comments=amount_of_general_comments, amount_of_row_subjects=amount_of_row_subjects, amount_of_row_subject_comments=amount_of_row_subject_comments)

@app.route("/administration/queries/<string:admin_name>")
def administration_queries(admin_name):
   if not check_user():
      return redirect("/")
   
   if not session["user_role"] == 2:
      return redirect("/")

   queries = get_queries()

   if queries == None:
      address = "/administration/" + admin_name
      return redirect(address)

   if len(queries) == 0:
      address = "/administration/" + admin_name
      return redirect(address)

   query_owner_list = get_query_owners()
   
   if query_owner_list == None:
      address = "/administration/" + admin_name
      return redirect(address)

   if len(query_owner_list) == 0:
      address = "/administration/" + admin_name
      return redirect(address)

   query_posts_list = get_query_posts()
   
   if query_posts_list == None:
      address = "/administration/" + admin_name
      return redirect(address)

   if len(query_posts_list) == 0:
      address = "/administration/" + admin_name
      return redirect(address)

   query_chapter_numbers_list = get_query_chapter_numbers()
   
   if query_chapter_numbers_list == None:
      address = "/administration/" + admin_name
      return redirect(address)

   if len(query_chapter_numbers_list) == 0:
      address = "/administration/" + admin_name
      return redirect(address)
   
   amount_of_queries = get_queries_amount()

   admin_queries_mode()
   return render_template("administration.html", admin_name=admin_name, queries=queries, query_owner_list=query_owner_list, query_posts_list=query_posts_list, query_chapter_numbers_list=query_chapter_numbers_list, amount_of_queries=amount_of_queries)

@app.route("/administration/answers/<string:admin_name>")
def administration_answers(admin_name):
   if not check_user():
      return redirect("/")
   
   if not session["user_role"] == 2:
      return redirect("/")

   answers = get_answers()

   if answers == None:
      address = "/administration/" + admin_name
      return redirect(address)

   if len(answers) == 0:
      address = "/administration/" + admin_name
      return redirect(address)

   answer_owner_list = get_answer_owner()

   if answer_owner_list == None:
      address = "/administration/" + admin_name
      return redirect(address)

   if len(answer_owner_list) == 0:
      address = "/administration/" + admin_name
      return redirect(address)

   answer_chapter_number_list = get_answer_chapter_numbers()

   if answer_chapter_number_list == None:
      address = "/administration/" + admin_name
      return redirect(address)

   if len(answer_chapter_number_list) == 0:
      address = "/administration/" + admin_name
      return redirect(address)

   answer_post_list = get_answer_posts()

   if answer_post_list == None:
      address = "/administration/" + admin_name
      return redirect(address)

   if len(answer_post_list) == 0:
      address = "/administration/" + admin_name
      return redirect(address)

   amount_of_answers = get_answers_amount()

   admin_answers_mode()
   return render_template("administration.html", admin_name=admin_name, answers=answers, answer_owner_list=answer_owner_list, answer_chapter_number_list=answer_chapter_number_list, answer_post_list=answer_post_list, amount_of_answers=amount_of_answers)

@app.route("/administration/clearance_code/<string:admin_name>", methods=["get","post"])
def administration_clearance_code(admin_name):
   if request.method == "GET":
      admin_clearance_code_mode()
      clearance_code = get_clearance_code()
      if clearance_code == None:
         address = "/administration/" + admin_name
         return redirect(address)
      return render_template("administration.html", admin_name=admin_name, clearance_code=clearance_code)
   if request.method == "POST":
      check_csrf()
      new_clearance_code = request.form["clearance_code"]
      if not change_clearance_code(new_clearance_code):
         address = "/administration/clearance_code/" + admin_name
         return redirect(address)
      address = "/administration/clearance_code/" + admin_name
      return redirect(address)

   return redirect("/")
    
@app.route("/profile/<string:user_name>")
def profile(user_name):
   comment_session_deletion()
   workbench_session_deletion()
   query_session_deletion()
   view_chapter_session_deletion()
   get_post_session_deletion()

   if not check_user_name_exists(user_name):
      return redirect("/")
   
   if check_if_user_name_is_admin(user_name):
      return redirect("/")
   

   owner = False
   admin = False
   if 'user_name' in session:
      if user_name == session["user_name"]:
         owner = True
      if session["user_role"] == 2:
         admin = True
   
   user_id = get_user_id(user_name)
   posts = get_profile_posts(user_id)
   
   if posts == None:
      return render_template("profile.html", user_name=user_name, size=0, owner=owner, admin=admin)

   if len(posts) == None:
      return render_template("profile.html", user_name=user_name, size=0, owner=owner, admin=admin)

   ratings = get_post_ratings()
   
   if ratings == None:
      return render_template("profile.html", user_name=user_name, size=0, owner=owner, admin=admin)
   
   if len(ratings) == 0:
      return render_template("profile.html", user_name=user_name, size=0, owner=owner, admin=admin)

   genres = get_post_genres()
   
   if genres == None:
      return render_template("profile.html", user_name=user_name, size=0, owner=owner, admin=admin)

   if len(genres) == 0:
      return render_template("profile.html", user_name=user_name, size=0, owner=owner, admin=admin)

   size = len(posts)
   
   posts_have_chapters = {}

   for post in posts:
      has_chapters = check_post_chapters(post[0])
      posts_have_chapters[post[0]] = has_chapters

   return render_template("profile.html", user_name=user_name, posts=posts, size=size, owns_chapters=posts_have_chapters, ratings=ratings, genres=genres, owner=owner, admin=admin)

@app.route("/workbench/save/<string:mode>", methods=["get","post"])
def workbench_save(mode):
   profile_session_deletion()
   if not check_user():
      return redirect("/")

   if 'user_role' in session:
      if session["user_role"] == 2:
         address = "/administration/" + session["user_name"]
         return redirect(address)
   
   if mode == "create_post" and request.method == "GET":
      workbench_create_post_mode()   
      return render_template("workbench.html")

   if mode == "save_post" and request.method == "POST":
      check_csrf()
      
      user_id = session["user_id"]
      public = request.form["public"]
      general_comments = request.form["general"]
      name = request.form["name"]
      rating = request.form["rating"]
      genre = request.form["genre"]
      
      if not save_post(user_id,public,general_comments,name,rating,genre):
         address = "/workbench/save/create_post"
         return redirect(address)
      
      workbench_session_deletion()
      user_name = session["user_name"]
      address = "/profile/" + user_name
      return redirect(address)

   if mode == "create_chapter" and request.method == "GET":
      workbench_create_chapter_mode()
      posts = get_profile_posts(session["user_id"])
      if posts == None:
         return redirect("/")
      size = len(posts)
      return render_template("workbench.html", posts=posts, size=size)

   if mode == "save_chapter" and request.method == "POST":
      check_csrf()
      
      post_id = request.form["chapter_picked_post"]
      chapter_public = request.form["chapter_public"]
      row_comments = request.form["chapter_row_comments_on"]
      inquiry = request.form["chapter_inquiry"]
      text_content = request.form["chapter_text"]
      
      if not save_chapter(post_id, chapter_public, row_comments, inquiry, text_content):
         address = "/workbench/save/create_chapter"
         return redirect(address)
      
      workbench_session_deletion()
      user_name = session["user_name"]
      address = "/profile/" + user_name
      return redirect(address)

   return redirect("/")

@app.route("/workbench/update/<string:mode>/<int:post_id>/<int:chapter_number>", methods=["get","post"])
def workbench_update(mode, post_id, chapter_number):
   profile_session_deletion()
   if not check_user():
      return redirect("/")

   if 'user_role' in session:
      if session["user_role"] == 2:
         address = "/administration/" + session["user_name"]
         return redirect(address)

   if not check_post_owner(session["user_name"],post_id):
      return redirect("/")
   
   if mode == "change_post" and post_id > 0 and request.method == "GET":
      if not get_post(post_id):
         return redirect("/")
      return render_template("workbench.html", post_id=post_id)

   if mode == "update_post" and post_id > 0 and request.method == "POST":
      check_csrf()
      
      old_name = session["given_post_name"]
      user_id = session["user_id"]
      public = request.form["public"]
      general_comments = request.form["general"]
      new_name = request.form["name"]
      rating = request.form["rating"]
      genre = request.form["genre"]
      
      if not update_post(old_name, user_id, public, general_comments, new_name, rating, genre):
         address = "/workbench/update/change_post" + "/" + str(post_id) + "/"+ str(chapter_number)
         return redirect(address)
      
      get_post_session_deletion()
      workbench_session_deletion()
      user_name = session["user_name"]
      address = "/profile/" + user_name
      return redirect(address)

   if mode == "change_chapter" and post_id > 0 and chapter_number > 0 and request.method == "GET":
      comment_session_deletion()
      if not get_chapter(post_id, chapter_number):
         return redirect("/")
      return render_template("workbench.html", post_id=post_id, chapter_number=chapter_number)

   if mode == "update_chapter" and post_id > 0 and chapter_number > 0 and request.method == "POST":
      check_csrf()
      public = request.form["chapter_public"]
      row_comments_on = request.form["chapter_row_comments_on"]
      inquiry_on = request.form["chapter_inquiry"]
      text_content = request.form["chapter_text"]
      misc = session["given_chapter_misc"]
      
      if not update_chapter(post_id, public, row_comments_on, inquiry_on, chapter_number, text_content, misc):
         address = "/workbench/update/change_chapter" + "/" + str(post_id) + "/"+ str(chapter_number)
         return redirect(address)
      
      get_chapter_session_deletion()
      workbench_session_deletion()
      user_name = session["user_name"]
      address = "/profile/" + user_name
      return redirect(address)
   
   return redirect("/")

@app.route("/workbench/remove/<string:mode>/<int:post_id>/<int:chapter_number>")
def workbench_remove(mode, post_id, chapter_number):
   if not check_user():
      return redirect("/")

   allowed = False

   if check_post_owner(session["user_name"],post_id):
      allowed = True

   if session["user_role"] == 2:
      allowed = True

   if not allowed:
      return redirect("/")

   if mode == "remove_post" and post_id > 0:
      post = get_the_post(post_id)

      if post == None:
         return redirect("/")

      if len(post) == 0:
         return redirect("/")

      user = get_the_user(post[1])

      if not remove_post(user[0],post_id):
         address = "/profile/" + user[1]
         return redirect(address)
      
      address = "/profile/" + user[1]
      return redirect(address)

   if mode == "remove_chapter" and post_id > 0 and chapter_number > 0:
      post = get_the_post(post_id)

      if post == None:
         return redirect("/")

      if len(post) == 0:
         return redirect("/")
      
      user = get_the_user(post[1])

      if not remove_chapter(post_id,chapter_number):
         address = "/profile/" + user[1]
         return redirect(address)
      
      address = "/profile/" + user[1]
      return redirect(address)

   return redirect("/")

@app.route("/view/<string:creator_name>/<string:post_name>/<int:post_id>/<int:chapter_number>")
def view(creator_name, post_name, post_id, chapter_number):
   profile_session_deletion()
   query_session_deletion()
   comment_session_deletion()
   workbench_session_deletion()
   get_chapter_session_deletion()

   if not view_chapter(creator_name, post_name, chapter_number):
      view_none_mode()
      return render_template("view.html")
   
   admin = False
   if check_user():
      if check_if_user_name_is_admin(session["user_name"]):
         admin = True
   
   view_read_mode()
   return render_template("view.html", creator_name=creator_name, post_name=post_name, post_id=post_id, chapter_number=chapter_number, admin=admin)

@app.route("/comments/general/<string:creator_name>/<string:post_name>/<int:post_id>")
def comments_general(creator_name, post_name, post_id):
   comment_session_deletion()
   comments = get_post_general_comments(post_id)

   if comments == None:
      return redirect("/")
   
   admin = False
   if check_user():
      if check_if_user_name_is_admin(session["user_name"]):
         admin = True
   
   if len(comments) == 0:
      comment_view_mode()
      return render_template("comments.html", creator_name=creator_name, post_name=post_name, post_id=post_id, size=0, admin=admin)
   
   comment_creators = {}

   for comment in comments:
       comment_creators[comment[0]] = get_comment_creator(comment[0])

   if len(comment_creators) == 0:
      comment_view_mode()
      return render_template("comments.html", creator_name=creator_name, post_name=post_name, post_id=post_id, size=0, admin=admin)
   
   size = len(comments)
   comment_view_mode()
   return render_template("comments.html", creator_name=creator_name, post_name=post_name, post_id=post_id, comments=comments, comment_creators=comment_creators, size=size, admin=admin)

@app.route("/comments/row/subjects/<string:creator_name>/<string:post_name>/<int:post_id>/<int:chapter_number>")
def row_subjects(creator_name, post_name, post_id, chapter_number):
   comment_session_deletion()
   view_chapter_session_deletion()

   admin = False
   if check_user():
      if check_if_user_name_is_admin(session["user_name"]):
         admin = True
   
   subjects = get_chapter_row_subjects(post_id, chapter_number)

   if subjects == None:
      address = "/view/" + creator_name + "/" + post_name + "/" + str(post_id)  + "/" + str(chapter_number)
      return redirect(address)

   if len(subjects) == 0:
      address = "/view/" + creator_name + "/" + post_name + "/" + str(post_id)  + "/" + str(chapter_number)
      return redirect(address)
   
   subject_creators = {}

   for subject in subjects:
       subject_creators[subject[0]] = get_comment_creator(subject[0])

   if len(subject_creators) == 0:
      address = "/view/" + creator_name + "/" + post_name + "/" + str(post_id)  + "/" + str(chapter_number)
      return redirect(address)

   size = len(subjects)
   row_subject_view_mode()
   return render_template("comments.html", creator_name=creator_name, post_name=post_name, post_id=post_id, chapter_number=chapter_number ,subjects=subjects, subject_creators=subject_creators, size=size, admin=admin)

@app.route("/comments/row/subject_comments/<string:creator_name>/<string:post_name>/<int:post_id>/<int:chapter_number>/<int:subject_id>")
def row_subject_comments(creator_name, post_name, post_id, chapter_number, subject_id):
   comment_session_deletion()
   
   admin = False
   if check_user():
      if check_if_user_name_is_admin(session["user_name"]):
         admin = True

   subject_comments = get_subject_comments(post_id,chapter_number,subject_id)

   if subject_comments == None:
      return redirect("/")
   
   if len(subject_comments) == 0:
      row_subject_comments_view_mode()
      return render_template("comments.html", creator_name=creator_name, post_name=post_name, post_id=post_id, chapter_number=chapter_number, subject_id=subject_id, size=0, admin=admin)

   subject_comment_creators = {}

   for subject_comment in subject_comments:
      subject_comment_creators[subject_comment[0]] = get_comment_creator(subject_comment[0])

   if len(subject_comment_creators) == 0:
      row_subject_comments_view_mode()
      return render_template("comments.html", creator_name=creator_name, post_name=post_name, post_id=post_id, chapter_number=chapter_number, subject_id=subject_id, size=0, admin=admin)

   size = len(subject_comments)
   row_subject_comments_view_mode()
   return render_template("comments.html", creator_name=creator_name, post_name=post_name, post_id=post_id, chapter_number=chapter_number, subject_id=subject_id, subject_comments=subject_comments, subject_comment_creators=subject_comment_creators, size=size, admin=admin)

@app.route("/comments/save/<string:mode>/<string:creator_name>/<string:post_name>/<int:post_id>/<int:chapter_number>/<int:subject_id>", methods=["get","post"])
def comments_save(mode, creator_name, post_name, post_id, chapter_number, subject_id):
   if not check_user():
      return redirect("/")

   if 'user_role' in session:
      if session["user_role"] == 2:
         address = "/administration/" + session["user_name"]
         return redirect(address)
   
   if mode == "create_general_comment" and request.method == "GET" and post_id > 0:
      comment_creation_mode()
      last_chapter = get_the_next_chapter_number(post_id)-1
      return render_template("comments.html", creator_name=creator_name, post_name=post_name, post_id=post_id, last_chapter=last_chapter)
   
   if mode == "save_general_comment" and request.method == "POST" and post_id > 0:
      check_csrf()
      
      user_id = session["user_id"]
      comment = request.form["comment_text"]
      referenced_chapter = request.form["referenced_chapter_number"]
      
      if not save_general_comment(post_id,user_id,comment,referenced_chapter):
         address = "/comments/save/create_general_comment/" + creator_name + "/" + post_name + "/" + str(post_id) + "/" + str(chapter_number) + "/" + str(subject_id)
         return redirect(address)
      
      comment_session_deletion()
      address = "/comments/general/"+ creator_name + "/"+ post_name +"/" + str(post_id)
      return redirect(address)

   if mode == "save_row_subject" and request.method == "POST" and post_id > 0 and chapter_number > 0:
      check_csrf()
      
      user_id = session["user_id"]
      subject = request.form["selected_text"]
      
      if not save_row_subject(user_id, post_id, chapter_number, subject):
         address = "/view/" + creator_name + "/" + post_name + "/" + str(post_id)  + "/" + str(chapter_number)
         return redirect(address)
      
      comment_session_deletion()
      address = "/comments/row/subjects/" + creator_name + "/" + post_name + "/" + str(post_id) + "/" + str(chapter_number)
      return redirect(address)

   if mode == "create_row_subject_comment" and request.method == "GET" and post_id > 0 and chapter_number > 0 and subject_id > 0:
      row_subject_comments_creation_mode()
      return render_template("comments.html", creator_name=creator_name, post_name=post_name, post_id=post_id, chapter_number=chapter_number, subject_id=subject_id)
   
   if mode == "save_row_subject_comment" and request.method == "POST" and post_id > 0 and chapter_number > 0 and subject_id > 0:
      check_csrf()
      
      user_id = session["user_id"]
      comment = request.form["row_subject_comment"]
      
      if not save_row_subject_comment(user_id, post_id, chapter_number, subject_id, comment):
         address = "/comments/save/create_row_subject_comment/" + creator_name + "/" + post_name + "/" + str(post_id) + "/" + str(chapter_number) + "/" + str(subject_id)
         return redirect(address)
      
      comment_session_deletion()
      row_subject_comments_view_mode()
      address = "/comments/row/subject_comments/" + creator_name + "/" + post_name + "/" + str(post_id) + "/" + str(chapter_number) + "/" + str(subject_id)
      return redirect(address)

   return redirect("/")
      
@app.route("/comment/remove/<string:mode>/<string:creator_name>/<string:post_name>/<int:post_id>/<int:chapter_number>/<int:subject_id>/<int:comment_id>")
def comment_remove(mode, creator_name, post_name, post_id, chapter_number, subject_id, comment_id):
   if not check_user():
      return redirect("/")

   allowed = False

   if check_post_owner(session["user_name"],post_id):
      allowed = True

   if session["user_role"] == 2:
      allowed = True

   if not allowed:
      return redirect("/")

   if mode == "remove_general_comment" and post_id > 0 and comment_id > 0:
      if not remove_comment(comment_id):
         address = "/comments/general/" + creator_name + "/" + post_name + "/" + str(post_id)
         return redirect(address)
      address = "/comments/general/" + creator_name + "/" + post_name + "/" + str(post_id)
      return redirect(address)

   if mode == "remove_row_subject" and post_id > 0 and chapter_number > 0 and subject_id > 0:
      if not remove_subject(post_id,chapter_number,subject_id):
         address = "/comments/row/subjects/" + creator_name + "/" + post_name + "/" + str(post_id) + "/" + str(chapter_number)
         return redirect(address)
      address = "/comments/row/subjects/" + creator_name + "/" + post_name + "/" + str(post_id) + "/" + str(chapter_number)
      return redirect(address)

   if mode == "remove_subject_comment" and post_id > 0 and chapter_number > 0 and comment_id > 0:
      if not remove_comment(comment_id):
         address = "/comments/row/subject_comments/" + creator_name + "/" + post_name + "/" + str(post_id) + "/" + str(chapter_number) + "/" + str(subject_id)
         return redirect(address)
      address = "/comments/row/subject_comments/" + creator_name + "/" + post_name + "/" + str(post_id) + "/" + str(chapter_number) + "/" + str(subject_id)
      return redirect(address)

   return redirect("/")
         
@app.route("/query/<string:mode>/<string:creator_name>/<string:post_name>/<int:post_id>/<int:chapter_number>/<int:query_id>")
def query(mode, creator_name, post_name, post_id, chapter_number, query_id):
   view_chapter_session_deletion()
   query_session_deletion()
   if not check_user():
      return redirect("/")

   admin = False
   if check_user():
      if check_if_user_name_is_admin(session["user_name"]):
         admin = True
   
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
      return render_template("queries.html", creator_name=creator_name, post_name=post_name, post_id=post_id, chapter_number=chapter_number, queries=queries, size=size,admin=admin)
   
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
         return render_template("queries.html", creator_name=creator_name, post_name=post_name, post_id=post_id, chapter_number=chapter_number, size=0,admin=admin)

      answer_creators = {}

      for answer in answers:
         answer_creators[answer[0]] = get_answer_creator(answer[0])
   
      if len(answer_creators) == 0:
         query_answers_mode()
         return render_template("queries.html", creator_name=creator_name, post_name=post_name, post_id=post_id, chapter_number=chapter_number, size=0,admin=admin)
   
      the_amount_of_answers = len(answers)
      query_answers_mode()
      return render_template("queries.html", creator_name=creator_name, post_name=post_name, post_id=post_id, chapter_number=chapter_number, size=the_amount_of_answers, answers=answers, answer_creators=answer_creators,admin=admin)
   
   return redirect("/")

@app.route("/query/save/<string:mode>/<string:creator_name>/<string:post_name>/<int:post_id>/<int:chapter_number>/<int:query_id>", methods=["get","post"])
def query_save(mode,creator_name,post_name,post_id,chapter_number,query_id):
   if not check_user():
      return redirect("/")

   if 'user_role' in session:
      if session["user_role"] == 2:
         address = "/administration/" + session["user_name"]
         return redirect(address)
   
   if mode == "create_question" and post_id > 0 and request.method == "GET": 
      if not check_post_owner(session["user_name"],post_id):
         return redirect("/")

      query_create_mode()
      return render_template("queries.html", creator_name=creator_name, post_name=post_name, post_id=post_id, chapter_number=chapter_number)
   
   if mode == "save_question" and post_id > 0 and request.method == "POST":
      check_csrf()

      if not check_post_owner(session["user_name"],post_id):
         return redirect("/")

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
      check_csrf()
      user_id = session["user_id"]
      answer = request.form["answer"]
      
      if not save_answer(user_id, query_id, answer):
         query = get_the_query(query_id)
         question = query[3]
         return render_template("queries.html", creator_name=creator_name, post_name=post_name, post_id=post_id, chapter_number=chapter_number, query_id=query_id, question=question)
      
      address = "/query/view_questions/" + creator_name + "/" + post_name + "/" + str(post_id) + "/" + str(chapter_number) + "/" + str(0)
      return redirect(address)

   return redirect("/")

@app.route("/query/remove/<string:mode>/<string:creator_name>/<string:post_name>/<int:post_id>/<int:chapter_number>/<int:query_id>/<int:answer_id>")
def query_remove(mode,creator_name,post_name,post_id,chapter_number,query_id,answer_id):
   if not check_user():
      return redirect("/")

   allowed = False

   if check_post_owner(session["user_name"],post_id):
      allowed = True

   if session["user_role"] == 2:
      allowed = True

   if not allowed:
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

   return redirect("/")
       
