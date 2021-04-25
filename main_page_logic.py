from app import app
from flask import redirect, render_template, request, session

def main_page_session_deletion():
    if 'log_in' in session:
      del session["log_in"]
   
    if 'sign_up' in session:
      del session["sign_up"]
   
    if 'workbench' in session:
      del session["workbench"] 
    
    if 'given_post_name' in session:
      del session["given_post_name"]
    
    if 'given_post_public' in session:
      del session["given_post_public"]    
    
    if 'given_post_general' in session:
      del session["given_post_general"]  
    
    if 'given_post_rating' in session:
      del session["given_post_rating"]  
    
    if 'given_post_genre' in session:
      del session["given_post_genre"] 

    if 'view_chapter' in session:
      del session["view_chapter"] 

    if 'view_mode' in session:
      del session["view_mode"] 

    if 'view_error' in session:
      del session["view_error"] 

    if 'comment_mode' in session:
      del session["comment_mode"]

    if 'comment_error' in session:
      del session["comment_error"] 

    if 'query_mode' in session:
      del session["query_mode"]

    if 'query_error' in session:
      del session["query_error"]