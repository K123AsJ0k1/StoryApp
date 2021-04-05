from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

def create_user(username, password):
    try:
        sql = "SELECT id FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        query = result.fetchone()

        if not query == None:
          return False
         
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username,password,role) VALUES (:username,:password,:role)"
        db.session.execute(sql, {"username":username,"password":hash_value,"role":0})
        db.session.commit()
        
        return True
    except Exception as e:
        print(e)
        return False

def login_user(username, password):
    try:
        sql = "SELECT password FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        user_password = result.fetchone()

        if user_password == None:
          return -1

        hash_value = user_password[0]
        if not check_password_hash(hash_value,password):
          return -2

        return 0
    except Exception as e:
        print(e)
        return -3

def get_user_id(username):
    try:
        sql = "SELECT id FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        user_id = result.fetchone()

        if user_id == None:
           return 0

        return user_id[0]
    except Exception as e:
        print(e)
        return 0

def save_post(user_id, visible, general_comments_on, name, misc):
    try:
        sql = "SELECT id FROM posts WHERE name=:name"
        result = db.session.execute(sql, {"name":name})
        post_id = result.fetchone()
        
        if not post_id == None:
            return -1

        sql = "INSERT INTO posts (user_id,visible,general_comments_on,name,misc) VALUES (:user_id,:visible,:general_comments_on,:name,:misc)"
        db.session.execute(sql, {"user_id":user_id,"visible":visible,"general_comments_on":general_comments_on,"name":name,"misc":misc})
        db.session.commit()
        
        return 0
    except Exception as e:
        print(e)
        return -2

def get_post_creator(id):
    try:
        sql = "SELECT user_id FROM posts WHERE id=:id"
        result = db.session.execute(sql, {"id":id})
        user_id = result.fetchone()

        if user_id == None:
            return None

        sql = "SELECT username FROM users WHERE id=:user_id"
        result = db.session.execute(sql, {"user_id":user_id})
        username = result.fetchone()

        return username[0]
    except Exception as e:
        print(e)
        return None

def get_profile_posts(user_id):
    try:
        sql = "SELECT id,visible,general_comments_on,name,misc FROM posts WHERE user_id=:user_id"
        result = db.session.execute(sql, {"user_id":user_id})
        posts = result.fetchall()
        return posts
    except Exception as e:
        print(e)
        return None

