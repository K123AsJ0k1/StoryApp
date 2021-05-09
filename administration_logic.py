from app import app
from flask import redirect, render_template, request, session
from users_db import *

def admin_main_mode():
    session["admin_mode"] = "main_mode"

def admin_users_mode():
    session["admin_mode"] = "users_mode"

def admin_posts_mode():
    session["admin_mode"] = "posts_mode"

def admin_chapters_mode():
    session["admin_mode"] = "chapters_mode"

def admin_comments_mode():
    session["admin_mode"] = "comments_mode"

def admin_queries_mode():
    session["admin_mode"] = "queries_mode"

def admin_answers_mode():
    session["admin_mode"] = "answers_mode"

def admin_clearance_code_mode():
    session["admin_mode"] = "clearance_code_mode"

def admin_session_deletion():
    if 'admin_mode' in session:
        del session["admin_mode"]
    if 'admin' in session:
        del session["admin"]

def get_clearance_code():
    proxy = get_clearance_proxy()
    
    if proxy == None:
       session["admin"] = "database_error"
       return None

    if len(proxy) == 0:
       session["admin"] = "database_error"
       return None

    return proxy[2]

def change_clearance_code(clearance_code):
    if clearance_code == None:
       session["admin"] = "empty_clearance_code"
       return False
    if len(clearance_code) < 20:
       session["admin"] = "short_clearance_code"
       return False
    
    check_number = update_clearance_code(clearance_code)

    if check_number == -1:
        session["admin"] = "database_error"
        return False
    if check_number == -2:
        session["admin"] = "database_error"
        return False
    
    session["admin"] = "clearance_code_updated"
    return True
