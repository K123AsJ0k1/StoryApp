from app import app
from flask import redirect, render_template, request, session
from users_db import *
import os

def sign_up_user_mode():
    session["sign_up_mode"] = "regular_mode"

def sign_up_admin_mode():
    session["sign_up_mode"] = "admin_mode"

def log_in_user_mode():
    session["login_mode"] = "1"

def log_in_admin_mode():
    session["login_mode"] = "2"

def register(mode, username, password, clearance_code):
    if mode == "register_user":
    
      if len(username) < 5:
        session["sign_up"] = "name_too_short"
        return False

      if len(password) < 8:
        session["sign_up"] = "password_too_short"
        return False

      check = create_user(username, password) 

      if not check:
        session["sign_up"] = "name_already_exists"
        return False
  
      user_id = get_user_id(username)

      if user_id == 0:
        return False
    
      session["csrf_token"] = os.urandom(16).hex()  
      session["user_id"] = user_id
      session["user_name"] = username 
      session["user_role"] = 1
    
      return True

    if mode == "register_admin":

      if len(username) < 10:
        return False

      if len(password) < 10:
        return False

      check_number = create_admin(username, password, clearance_code)
        
      if check_number == -1:
        return False

      if check_number == -2:
        return False

      if check_number == -3:
        return False

      user_id = get_user_id(username)

      if user_id == 0:
        return False

      session["csrf_token"] = os.urandom(16).hex()  
      session["user_id"] = user_id
      session["user_name"] = username 
      session["user_role"] = 2

      return True

def log_in(mode, username, password):
    if mode == "check_user":
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

    if mode == "check_admin":
      check_number = login_admin(username, password)

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
      session["user_role"] = 2

      return True

def check_user_name_exists(user_name):
    check_number = get_user_id(user_name)

    if check_number == 0:
      return False

    return True

def check_if_user_name_is_admin(user_name):
    user_role = get_user_role(user_name)

    if user_role == -1:
      return False

    if user_role == 2 or user_role == 3:
      return True

    return False
    
def check_user():
    if "user_name" in session:
       return True
    return False

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
      abort(403)

def get_regulars_amount():
    users = get_users()

    if users == None:
      return 0

    amount = 0

    for user in users:
      if user[2] == 1:
        amount = amount + 1

    return amount

def get_admins_amount():
    users = get_users()

    if users == None:
      return 0

    amount = 0

    for user in users:
      if user[2] == 2:
        amount = amount + 1

    return amount 
  
def get_user_name(user_id):
    users = get_users()

    if users == None:
      return None
    
    user_name = ""
    for user in users:
      if user[0] == user_id:
        user_name = user[1]

    return user_name
