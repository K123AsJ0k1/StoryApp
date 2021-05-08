from app import app
from flask import redirect, render_template, request, session
from users_db import *

def admin_statistic_mode():
    session["admin_mode"] = "1"

def admin_users_mode():
    session["admin_mode"] = "2"

def admin_posts_mode():
    session["admin_mode"] = "3"

def admin_chapters_mode():
    session["admin_mode"] = "4"

def admin_comments_mode():
    session["admin_mode"] = "5"

def admin_queries_mode():
    session["admin_mode"] = "6"

def admin_answers_mode():
    session["admin_mode"] = "7"

def admin_clearance_code_mode():
    session["admin_mode"] = "8"

def get_clearance_code():
    proxy = get_clearance_proxy()
    
    if proxy == None:
       return None

    if len(proxy) == 0:
       return None

    return proxy[2]

def change_clearance_code(clearance_code):
    if clearance_code == None:
       # session
       return False
    if len(clearance_code) < 20:
       # session
       return False
    
    check_number = update_clearance_code(clearance_code)

    if check_number == -1:
        # session
        return False
    if check_number == -2:
        # session
        return False

    return True
