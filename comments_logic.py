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

def save_row_subject_comment(user_id, post_id, chapter_number, row_id, comment):
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

def remove_subject(post_id,chapter_number,subject_id):
    check_number = remove_the_subject_comments(post_id,chapter_number,subject_id)

    if check_number == -2:
      return False
      
    check_number = remove_comment(subject_id)
    
    if check_number == -2:
      return False

    return True

def remove_subjects(post_id,chapter_number):
    check_number = remove_the_chapter_row_subjects(post_id,chapter_number)

    if check_number == -2:
      return False

    return True

def remove_subject_comments(post_id,chapter_number,subject_id):
    check_number = remove_the_subject_comments(post_id,chapter_number,subject_id)

    if check_number == -2:
      return False

    return True

def get_general_comment_amount():
    comments = get_comments()

    if comments == None:
      return 0

    size = 0
    
    for comment in comments:
      if comment[4]:
        size = size + 1

    return size

def get_row_subject_amount():
    comments = get_comments()

    if comments == None:
      return 0

    size = 0

    for comment in comments:
      if comment[5] and comment[3] == 0:
        size = size + 1

    return size

def get_row_subject_comment_amount():
    comments = get_comments()

    if comments == None:
      return 0

    size = 0

    for comment in comments:
      if comment[5] and comment[3] > 0:
        size = size + 1

    return size

    
   