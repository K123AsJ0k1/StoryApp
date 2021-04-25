from app import app
from flask import redirect, render_template, request, session
from users_logic import *
from posts_db import *
from chapters_db import *
from text import *
from misc import *


def workbench_view_mode():
    session["workbench"] = "0"
    
def workbench_post_mode():
    session["workbench"] = "1"

def workbench_chapter_mode():
    session["workbench"] = "2"

def save_post(user_id, public, general_comments, name, rating, genre):
    visible = '2'
   
    if public == "true":
      visible = '1'

    if public == "false":
      visible = '0'

    general_comments_on = '2'

    if general_comments == "true":
      general_comments_on = '1'

    if general_comments == "false":
      general_comments_on = '0'

    if not check_title_requirements(name):
      return False
    
    misc = create_misc(rating,genre)
    
    check_number = save_the_post(user_id, visible, general_comments_on, name, misc)

    if check_number == -1:
      return False

    if check_number == -2:
      return False
    
    return True

def save_chapter(post_id,chapter_public,row_comments,inquiry,text_content):
    if post_id == None:
      return False
   
    public = '2'
    
    if chapter_public == "true":
      public = '1'
    if chapter_public == "false":
      public = '0'

    row_comments_on = '2'
    
    if row_comments == "true":
      row_comments_on= '1'
    if row_comments == "false":
      row_comments_on = '0'

    inquiry_on = '2'

    if inquiry == "true":
      inquiry_on = '1'
    if inquiry == "false":
      inquiry_on = '0'

    if not check_text_requirements(text_content):
      return False

    chapter_number = get_the_next_chapter_number(post_id)

    if chapter_number == 0:
      return False

    text_rows = rows(text_content)
    text_source = get_source_text(text_content)
   
    misc = ""

    check_number = save_the_chapter(post_id, public, row_comments_on, inquiry_on, chapter_number, text_rows, text_source, misc)
    
    if check_number == -1:
      return False
    if check_number == -2:
      return False
    
    return True

def get_post(post_id):
    post = get_the_post(post_id)
 
    if post == None:
      return False

    session["given_post_name"] = post[4]
   
    check_public = post[2]
    if check_public:
      session["given_post_public"] = "1"
    if not check_public:
      session["given_post_public"] = "2"

    check_general = post[3]
    if check_general:
      session["given_post_general"] = "1"
    if not check_general:
      session["given_post_general"] = "2"

    misc_list = list_misc(post[5])

    session["given_post_rating"] = misc_list[0]
    session["given_post_genre"] = misc_list[1]

    session["workbench"] = "3"
    return True

def update_post(old_name, user_id, public, general_comments, new_name, rating, genre):
    visible = '2'
    if public == "true":
      visible = '1'
    if public == "false":
      visible = '0'

    general_comments_on = "2"
    if general_comments == "true":
      general_comments_on = '1'
    if general_comments == "false":
      general_comments_on = '0'

    misc = create_misc(rating,genre)
    
    check_number = update_the_post(old_name, user_id, visible, general_comments_on, new_name, misc)
    
    if check_number == -1:
      return False

    if check_number == -2:
      return False
    
    return True

def remove_post(user_id, post_id):
    post = get_the_post(post_id)

    if post == None:
       return False
    
    check_number = remove_the_post(user_id,post[4])
    
    if check_number == -1:
      return False

    if check_number == -2:
      return False

    if check_number == -3:
      return False

    return True

def remove_chapter(post_id,chapter_number):
    check_number = remove_the_chapter_row_subjects(post_id,chapter_number)
    
    if check_number == -2:
      return False

    check_number = remove_the_chapter(post_id,chapter_number)
    
    if check_number == -1:
      return False
    
    if check_number == -2:
      return False

    check_number = update_the_chapter_numbers(post_id)

    if check_number == -1:
      return False

    if check_number == -2:
      return False
    
    return True


    