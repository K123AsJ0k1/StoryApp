from app import app
from flask import redirect, render_template, request, session
from users_db import *
import os

def sign_up_user_mode():
    session["sign_up_mode"] = "regular_mode"

def sign_up_admin_mode():
    session["sign_up_mode"] = "admin_mode"

def log_in_user_mode():
    session["login_mode"] = "regular_mode"

def log_in_admin_mode():
    session["login_mode"] = "admin_mode"

def sign_up_session_deletion():
    if 'sign_up' in session:
      del session["sign_up"]
    if 'sign_up_mode' in session:
      del session["sign_up_mode"] 

def log_in_session_deletion():
    if 'log_in' in session:
      del session["log_in"]
    if 'login_mode' in session:
      del session["login_mode"]

def register(mode, user_name, password, clearance_code):
    user_id = 0
    if mode == "register_user":
      if len(user_name) < 5:
        session["sign_up"] = "name_too_short"
        return False
      if len(password) < 8:
        session["sign_up"] = "password_too_short"
        return False
      
      check_number = create_user(user_name, password) 
      
      if check_number == -1:
        session["sign_up"] = "name_already_exists"
        return False
      if check_number == -2:
        session["sign_up"] = "database_error"
        return False
      
      user_id = get_user_id(user_name)

    if mode == "register_admin":
      if len(user_name) < 10:
        session["sign_up"] = "name_too_short"
        return False
      if len(password) < 10:
        session["sign_up"] = "password_too_short"
        return False

      check_number = create_admin(user_name, password, clearance_code)

      if check_number == -1:
        session["sign_up"] = "name_already_exists"
        return False
      if check_number == -2:
        session["sign_up"] = "database_error"
        return False
      if check_number == -3:
        session["sign_up"] = "wrong_clearance_code"
        return False
      if check_number == -4:
        session["sign_up"] = "no_clearance_proxy"
        return False

      user_id = get_user_id(user_name)

    if user_id == 0:
        return False

    user = get_the_user(user_id)

    if user == None:
      return False

    session["csrf_token"] = os.urandom(16).hex() 
    session["user_id"] = user_id
    session["user_name"] = user_name 
    session["user_role"] = user[3]
    
    return True
  
def log_in(mode, user_name, password):
    check_number = 0
    
    if mode == "check_user":
      check_number = login_user(user_name, password)
    if mode == "check_admin":
      check_number = login_admin(user_name, password)
    
    if check_number == -1:
      session["log_in"] = "name_doesnt_exist"
      return False
    if check_number == -2:
      session["log_in"] = "database_error"
      return False
    if check_number == -3:
      session["log_in"] = "wrong_password"
      return False

    user_id = get_user_id(user_name) 

    if user_id == 0:
      return False

    user = get_the_user(user_id)

    if user == None:
      return False

    session["csrf_token"] = os.urandom(16).hex() 
    session["user_id"] = user_id
    session["user_name"] = user_name 
    session["user_role"] = user[3]
    
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
