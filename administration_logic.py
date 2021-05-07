from app import app
from flask import redirect, render_template, request, session

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
