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
    return redirect("/")

@app.route("/profile")
def profile():
    if 'workbench' in session:
        del session["workbench"] 
    posts = get_profile_posts(get_user_id(session["username"]))
    size = len(posts)
    return render_template("profile.html", posts=posts, size=size)

@app.route("/workbench")
def workbench():
    session["workbench"] = "0"
    session["workbencherror"] = "0"
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
def save_logic():
    user_id = get_user_id(session["username"]) 
    
    if user_id == 0:
       session["workbencherror"] = "3"
       return render_template("workbench.html")

    general_comments = request.form["general"]
    
    if general_comments == "true":
       general_comments_on = '1'

    if general_comments == "false":
       general_comments_on = '0'
    
    name = request.form["name"]
    
    rating = request.form["rating"]
    genre = request.form["genre"]
    misc = create_misc(rating,genre)
    
    check_number = save_post(user_id, general_comments_on, name, misc)

    if check_number == -1:
       session["workbencherror"] = "4"
       return render_template("workbench.html")

    if check_number == -2:
       session["workbencherror"] = "5"
       return render_template("workbench.html") 
    
    session["workbench"] = "0"
    session["workbencherror"] = "0"
    return redirect("/profile")

