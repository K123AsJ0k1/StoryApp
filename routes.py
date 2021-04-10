from app import app
import re
from db import *
from misc import *
from flask import redirect, render_template, request, session
from os import getenv

app.secret_key = getenv("SECRET_KEY")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route("/")
def index():
   if 'login' in session:
      del session["login"]
   if 'signup' in session:
       del session["signup"]
   if 'workbench' in session:
      del session["workbench"] 
    
   if 'given_post_name' in session:
      del session["given_post_name"]
    
   if 'given_post_public' in session:
      del session["given_post_public"]    
    
   if 'given_post_general' in session:
      del session["given_post_general"]  
    
   if 'given_post_rating' in session:
      del session["given_post_rating"]  
    
   if 'given_post_genre' in session:
      del session["given_post_genre"] 

   if 'view_chapter' in session:
      del session["view_chapter"] 

   if 'view_mode' in session:
      del session["view_mode"] 

   if 'view_error' in session:
      del session["view_error"] 
    
   posts = get_public_posts()
   size = len(posts)
   return render_template("main.html", posts=posts, size=size)

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/signup",methods=["POST"])
def signup_logic():
   username = request.form["username"]
   password = request.form["password"]

   if len(username) < 5:
      session["signup"] = "1"
      return render_template("signup.html")

   if len(password) < 8:
      session["signup"] = "2"
      return render_template("signup.html")

   check = create_user(username, password) 

   if not check:
      session["signup"] = "3"
      return render_template("signup.html")

   session["username"] = username
   return redirect("/")

@app.route("/login")
def login():
   return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_logic():
   username = request.form["username"]
   password = request.form["password"]
    
   check_number = login_user(username, password)
    
   if check_number == -1:
      session["login"] = "1"
      return render_template("login.html")

   if check_number == -2:
      session["login"] = "2"
      return render_template("login.html")
     
   session["username"] = username
   return redirect("/")
    
@app.route("/logout")
def logout():
   if 'username' in session:
      del session["username"]
    
   if 'workbench' in session:
      del session["workbench"]

   if 'workbencherror' in session:
      del session["workbencherror"]

   if 'profileerror' in session:
      del session["profileerror"]
    
   if 'given_post_name' in session:
      del session["given_post_name"]
    
   if 'given_post_public' in session:
      del session["given_post_public"]    
    
   if 'given_post_general' in session:
      del session["given_post_general"]  
    
   if 'given_post_rating' in session:
      del session["given_post_rating"]  
   
   if 'given_post_genre' in session:
      del session["given_post_genre"] 
    
   if 'view_chapter' in session:
      del session["view_chapter"] 

   if 'view_mode' in session:
      del session["view_mode"] 

   if 'view_error' in session:
      del session["view_error"] 
    
   return redirect("/")

@app.route("/profile")
def profile():
   if 'given_post_name' in session:
      del session["given_post_name"]
    
   if 'given_post_public' in session:
      del session["given_post_public"]    
    
   if 'given_post_general' in session:
      del session["given_post_general"]  
    
   if 'given_post_rating' in session:
      del session["given_post_rating"]  
    
   if 'given_post_genre' in session:
      del session["given_post_genre"] 

   if 'view_chapter' in session:
      del session["view_chapter"] 

   if 'view_mode' in session:
      del session["view_mode"] 

   if 'view_error' in session:
      del session["view_error"] 

   posts = get_profile_posts(get_user_id(session["username"]))
   size = len(posts)
   return render_template("profile.html", posts=posts, size=size)

@app.route("/workbench")
def workbench():
   session["workbench"] = "0"
   session["workbencherror"] = "0"
   if 'profileerror' in session:
      del session["profileerror"]
   return render_template("workbench.html")

@app.route("/post")
def post():
   session["workbench"] = "1"
   session["workbencherror"] = "1"
   return render_template("workbench.html")

@app.route("/save/post", methods=["POST"])
def save_post_logic():
   user_id = get_user_id(session["username"]) 
    
   if user_id == 0:
      session["workbencherror"] = "3"
      return render_template("workbench.html")

   public = request.form["public"]
   visible = '2'
   if public == "true":
      visible = '1'

   if public == "false":
      visible = '0'

   general_comments = request.form["general"]
   general_comments_on = '2'

   if general_comments == "true":
      general_comments_on = '1'

   if general_comments == "false":
      general_comments_on = '0'

   name = request.form["name"]
    
   rating = request.form["rating"]
   genre = request.form["genre"]
   misc = create_misc(rating,genre)
    
   check_number = save_post(user_id, visible, general_comments_on, name, misc)

   if check_number == -1:
      session["workbencherror"] = "4"
      return render_template("workbench.html")

   if check_number == -2:
      session["workbencherror"] = "5"
      return render_template("workbench.html") 
    
   session["workbench"] = "0"
   session["workbencherror"] = "0"
   return redirect("/profile")

@app.route("/update/<string:name>")
def update_post(name):
   user_id = get_user_id(session["username"]) 
    
   if user_id == 0:
      session["profileerror"] = "1"
      return redirect("/profile")

   post = get_profile_post(user_id,name)
    
   if post == None:
      session["profileerror"] = "2"
      return redirect("/profile")

   session["workbench"] = "3"

   session["given_post_name"] = post[4]
    
   check_public = post[2]

   if check_public:
      session["given_post_public"] = "1"

   if not check_public:
      session["given_post_public"] = "2"

   check_general = post[3]

   if check_general:
      session["given_post_general"] = "1"
    
   if not check_general:
      session["given_post_general"] = "2"

   misc_list = list_misc(post[5])

   session["given_post_rating"] = misc_list[0]

   session["given_post_genre"] = misc_list[1]

   return render_template("workbench.html") 

@app.route("/update", methods=["POST"])
def update_post_logic():
   old_name = session["given_post_name"]
   user_id = get_user_id(session["username"]) 
    
   if user_id == 0:
      session["workbencherror"] = "3"
      return render_template("workbench.html")

   public = request.form["public"]
   visible = '2'
    
   if public == "true":
      visible = '1'

   if public == "false":
      visible = '0'

   general_comments = request.form["general"]
   general_comments_on = "2"
    
   if general_comments == "true":
      general_comments_on = '1'

   if general_comments == "false":
      general_comments_on = '0'

   new_name = request.form["name"]
    
   rating = request.form["rating"]
   genre = request.form["genre"]
   misc = create_misc(rating,genre)
    
   check_number = update_the_post(old_name, user_id, visible, general_comments_on, new_name, misc)
    
   if check_number == -1:
      session["workbencherror"] = "4"
      return render_template("workbench.html")

   if check_number == -2:
      session["workbencherror"] = "5"
      return render_template("workbench.html") 
    
   session["workbench"] = "0"
   session["workbencherror"] = "0"
   return redirect("/profile")
         
@app.route("/remove/<string:name>")
def remove_post_logic(name):
   user_id = get_user_id(session["username"]) 
    
   if user_id == 0:
      session["profileerror"] = "1"
      return redirect("/profile")

   check_number = remove_post(user_id,name)
    
   if check_number == -1:
      session["profileerror"] = "2"
      return redirect("/profile")

   if check_number == -2:
      session["profileerror"] = "1"
      return redirect("/profile")

   if check_number == -3:
      session["profileerror"] = "1"
      return redirect("/profile")

   session["profileerror"] = "3"
   return redirect("/profile")

@app.route("/chapter")
def chapter():
   session["workbench"] = "2"
   session["workbencherror"] = "2"
   posts = get_profile_posts(get_user_id(session["username"]))
   size = len(posts)
   return render_template("workbench.html", posts=posts, size=size)

@app.route("/save/chapter", methods=["POST"])
def save_chapter():
   post_id = request.form["chapter_picked_post"]
    
   if post_id == None:
      session["workbencherror"] = "6"
      return redirect("/chapter")
    
   chapter_public = request.form["chapter_public"]

   public = '2'
    
   if chapter_public == "true":
      public = '1'

   if chapter_public == "false":
      public = '0'

   row_comments = request.form["chapter_row_comments_on"]
    
   row_comments_on = '2'
    
   if row_comments == "true":
      row_comments_on= '1'

   if row_comments == "false":
      row_comments_on = '0'

   inquiry = request.form["chapter_inquiry"]
    
   inquiry_on = '2'

   if inquiry == "true":
      inquiry_on = '1'

   if inquiry == "false":
      inquiry_on = '0'

   chapter_number = get_the_next_chapter_number(post_id)

   if chapter_number == 0:
      session["workbencherror"] = "7"
      return redirect("/chapter")

   text_content = request.form["chapter_text"]
    
   text_rows = len(text_content.split("\n"))

   misc = ""

   check_number = save_the_chapter(post_id, public, row_comments_on, inquiry_on, chapter_number, text_rows, text_content, misc)
    
   if check_number == -1:
      session["workbencherror"] = "8"
      return redirect("/chapter")

   if check_number == -1:
      session["workbencherror"] = "9"
      return redirect("/chapter")

   session["workbench"] = "0"
   session["workbencherror"] = "0"
   return redirect("/profile")

@app.route("/remove/chapter/<int:post_id>/<int:chapter_number>")
def remove_chapter_logic(post_id,chapter_number):
   check_number = remove_the_chapter(post_id,chapter_number)
    
   if check_number == -1:
      session["profileerror"] = "4"
      return redirect("/profile")
    
   if check_number == -2:
      session["profileerror"] = "1"
      return redirect("/profile")

   check_number = update_the_chapter_numbers(post_id)

   if check_number == -1:
      session["profileerror"] = "4"
      return redirect("/profile")

   if check_number == -2:
      session["profileerror"] = "1"
      return redirect("/profile")
    
   session["profileerror"] = "3"
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
      return render_template("view.html")

   chapter_content = chapter[7]

    
   # Edellinen luku, seuraava luku ja valittavat luku asiat
    
   # Row comment asiat
    
   # chapter_rows = chapter[6]

   # row_comments_on = chapter[3]

   # Kyselyt asiat

   # inquiry_on = chapter[4]

   session["view_chapter"] = "0"

   if chapter_number == 1:
      session["view_chapter"] = "1"

   if chapter_number == get_the_next_chapter_number(post_id)-1:
      session["view_chapter"] = "2"

   if get_the_next_chapter_number(post_id) == 2:
      session["view_chapter"] = "3"
    
   session["view_mode"] = "1"
   session["view_error"] = "0"
   return render_template("view.html", creator=creator_name, story=post_name, post=post_id, chapter=chapter_number, text=chapter_content, previous_chapter=chapter_number-1, next_chapter=chapter_number+1)
    
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
       creator = get_comment_creator(comment[1])
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
   session["comment_mode"] = "2"
   session["comment_error"] = "3"
   last_chapter = get_the_next_chapter_number(post_id)-1
   return render_template("comments.html", last_chapter=last_chapter,  post_id=post_id, story=post_name)

@app.route("/save/comment/general/<int:post_id>/<string:post_name>", methods=["POST"])
def save_general_comment(post_id,post_name):
   user_id = get_user_id(session["username"])
   
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

   if comment == "":
      address = "/create/comment/general/"+ str(post_id) + "/"+ post_name
      return redirect(address)

   check_number = save_the_comment(user_id, post_id, 0, '1', '0', chapter_number_on, chapter_number, comment)
   
   if check_number == -1:
      address = "/create/comment/general/"+ str(post_id) + "/"+ post_name
      return redirect("/create/comment/"+post_id+"/"+post_name)
   
   address = "/comments/general/"+ str(post_id) + "/"+ post_name
   return redirect(address)

@app.route("/remove/comment/general/<int:post_id>/<string:post_name>/<int:comment_id>")
def remove_general_comment(post_id, post_name, comment_id):
   check_number = remove_the_comment(comment_id)

   if check_number == -1:
       address = "/comments/general/"+ str(post_id) + "/"+ post_name
       return redirect(address)

   address = "/comments/general/"+ str(post_id) + "/"+ post_name
   return redirect(address)

   

   




   


   
    

   

   

   










    



    

    
