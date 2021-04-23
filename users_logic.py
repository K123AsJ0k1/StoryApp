from app import app
from flask import redirect, render_template, request, session
from users_db import *

def register(username, password):
   if len(username) < 5:
      session["signup"] = "1"
      return False

   if len(password) < 8:
      session["signup"] = "2"
      return False

   check = create_user(username, password) 

   if not check:
      session["signup"] = "3"
      return False

   session["username"] = username
   return True


