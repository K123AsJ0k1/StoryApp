from app import app
from flask import redirect, render_template, request, session
from users_db import *
import os

def register(username, password):
    if len(username) < 5:
      session["sign_up"] = "1"
      return False

    if len(password) < 8:
      session["sign_up"] = "2"
      return False

    check = create_user(username, password) 

    if not check:
      session["sign_up"] = "3"
      return False
  
    user_id = get_user_id(username)

    if user_id == 0:
      return False
    
    session["csrf_token"] = os.urandom(16).hex()  
    session["user_id"] = user_id
    session["user_name"] = username 
    session["user_role"] = 1
    
    return True

def log_in(username, password):
    check_number = login_user(username, password)

    if check_number == -1:
      session["log_in"] = "1"
      return False

    if check_number == -2:
      session["log_in"] = "2"
      return False

    user_id = get_user_id(username)

    if user_id == 0:
      return False
   
    session["csrf_token"] = os.urandom(16).hex() 
    session["user_id"] = user_id
    session["user_name"] = username 
    session["user_role"] = 1

    return True

def check_user():
    if "user_name" in session:
       return True
    return False

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
      abort(403)




