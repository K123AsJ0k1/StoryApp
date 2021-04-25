from app import app
from flask import redirect, render_template, request, session
from posts_db import *
from chapters_db import *
from comments_db import *
from text import *

def comment_view_mode():
    session["comment_mode"] = "1"

def comment_creation_mode():
    session["comment_mode"] = "2"

def row_subject_view_mode():
    session["comment_mode"] = "3"

def row_subject_comments_view_mode():
    session["comment_mode"] = "4"

def row_subject_comments_creation_mode():
    session["comment_mode"] = "5"

def save_general_comment(post_id,user_id,comment,referenced_chapter):
    if not check_text_requirements(comment):
      return False

    chapter_list = get_the_chapter_numbers(post_id)
  
    chapter_number_on = '0'
    chapter_number = 0
    
    if referenced_chapter.isdigit(): 
      for chapter in chapter_list:
         if chapter[0] == int(referenced_chapter):
          chapter_number_on = '1'
          chapter_number = chapter[0]
   
    check_number = save_the_comment(user_id, post_id, 0, '1', '0', chapter_number_on, chapter_number, comment)
   
    if check_number == -2:
      return False
   
    return True

def save_row_subject(user_id, post_id, chapter_number, comment):
    if not check_text_requirements(comment):
      return False

    check_number = save_the_comment(user_id, post_id, 0, '0', '1', '1', chapter_number, comment)

    if check_number == -2:
      return False

    return True

def save_row_subject_comment(user_id, post_id, row_id, chapter_number, comment):
    if not check_text_requirements(comment):
      return False

    check_number = save_the_comment(user_id, post_id, row_id, '0', '1', '1', chapter_number, comment)

    if check_number == -2:
      return False

    return True

def remove_comment(comment_id):
   check_number = remove_the_comment(comment_id)

   if check_number == -2:
       return False

   return True
   