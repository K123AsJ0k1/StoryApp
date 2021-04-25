from app import app
from db import *
from werkzeug.security import check_password_hash, generate_password_hash

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

def create_admin(username, password, super_user_password):
    try:
        sql = "SELECT id FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        query = result.fetchone()
        
        if not query == None:
          return -1

        # Tarkoitus on hakea tietokannasta user taulusta käyttäjältä super user:in salasana
        if not super_user_password == "Salasana":
          return -2

        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username,password,role) VALUES (:username,:password,:role)"
        db.session.execute(sql, {"username":username, "password":hash_value, "role":1})
        db.session.commit()
    
        return 0
    except Exception as e:
        print(e)
        return -3

def login_user(username, password):
    try:
        sql = "SELECT password FROM users WHERE username=:username AND role=0"
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

def login_admin(username, password):
    try:
        sql = "SELECT password FROM users WHERE username=:username AND role=1"
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



