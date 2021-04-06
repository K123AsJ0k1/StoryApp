from app import app
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
    return render_template("main.html")

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
    if 'profileerror' in session:
       del session["profileerror"]
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

@app.route("/chapter")
def chapter():
    session["workbench"] = "2"
    session["workbencherror"] = "2"
    return render_template("workbench.html")

@app.route("/save", methods=["POST"])
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

    

    
