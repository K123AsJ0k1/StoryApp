from app import app
from db import *
from werkzeug.security import check_password_hash, generate_password_hash

def create_clearance_proxy():
    try:
        sql = "SELECT username FROM users WHERE role=3"
        result = db.session.execute(sql)
        proxy = result.fetchone()
        
        if not proxy == None:
          return False
 
        username = "clearance_proxy"
        password = "starter_clearance_proxy_code"
        
        sql = "INSERT INTO users (username,password,role) VALUES (:username,:password,:role)"
        db.session.execute(sql, {"username":username,"password": password,"role":3})
        db.session.commit()

        return True
    except Exception as e:
        print(e)
        return False    

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

def create_admin(username, password, given_clearance_code):
    try:
        sql = "SELECT id FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        query = result.fetchone()
        
        if not query == None:
          return -1

        sql = "SELECT password FROM users WHERE role=3"
        result = db.session.execute(sql)
        clearance_code = result.fetchone()
        
        if clearance_code == None:
          return -3

        if not given_clearance_code == clearance_code[0]:
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

def update_clearance_code(clearance_code):
    try:
        sql = "SELECT id FROM users WHERE role=3"
        result = db.session.execute(sql)
        proxy_id = result.fetchone()
  
        if proxy_id == None:
          return -1

        sql = "UPDATE users SET password=:clearance_code WHERE id=:proxy_id"
        db.session.execute(sql, {"clearance_code":clearance_code, "proxy_id":proxy_id[0]})
        db.session.commit()
       
        return 0
    except Exception as e:
        print(e)
        return -2 

def get_clearance_proxy():
    try:
        sql = "SELECT id,username,password,role FROM users WHERE role=3"
        result = db.session.execute(sql)
        proxy = result.fetchone()
        if proxy == None:
          return None
        if len(proxy) == 0:
          return None
        return proxy
    except Exception as e:
        print(e)
        return None    
        
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

def get_user_role(user_name):
    try:
        sql = "SELECT role FROM users WHERE username=:user_name"
        result = db.session.execute(sql, {"user_name":user_name})
        user_role = result.fetchone()

        if user_role == None:
          return -1

        return user_role[0]
    except Exception as e:
        print(e)
        return -2
       
def get_regulars_amount():
    try:
        sql = "SELECT username FROM users WHERE role=0"
        result = db.session.execute(sql)
        regulars = result.fetchall()

        if regulars == None:
          return 0

        return len(regulars)
    except Exception as e:
        print(e)
        return -2

def get_admins_amount():
    try:
        sql = "SELECT username FROM users WHERE role=1"
        result = db.session.execute(sql)
        admins = result.fetchall()

        if admins == None:
          return 0

        return len(admins)
    except Exception as e:
        print(e)
        return -2  

def get_users():
    try:
       sql = "SELECT id,username,role FROM users"
       result = db.session.execute(sql)
       users = result.fetchall()

       if users == None:
         return None
      
       return users
    except Exception as e:
        print(e)
        return None  




