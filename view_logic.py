from app import app
from flask import redirect, render_template, request, session
from users_logic import *
from posts_db import *
from chapters_db import *
from text import *

def view_none_mode():
    session["view_mode"] = "none_mode"

def view_read_mode():
    session["view_mode"] = "read_mode"

def view_chapter_session_deletion():
    if 'view' in session:
      del session["view"]
    if 'switch_chapter' in session:
      del session["switch_chapter"]
    if 'post_id' in session:
      del session["post_id"]
    if 'public' in session:
      del session["public"]
    if 'row_subject' in session:
      del session["row_subject"]
    if 'inquiry' in session:
      del session["inquiry"]
    if 'chapter_content' in session:
      del session["chapter_content"]

def view_chapter(creator_name,post_name,chapter_number):
    user_id = get_user_id(creator_name)
    
    if user_id == 0:
      return False
  
    post = get_profile_post(user_id,post_name)

    if post == None:
      return False

    post_id = post[0]
   
    chapter = get_the_chapter(post_id,chapter_number)

    if chapter == None:
      return False
    
    public = chapter[2]
    row_subject = chapter[3]
    inquiry_on = chapter[4]

    chapter_content = get_source_text_array(chapter[7])
        
    session["switch_chapter"] = "chapters_on_both_sides"

    if chapter_number == 1:
      session["switch_chapter"] = "chapters_on_right_side"
    if chapter_number == get_the_next_chapter_number(post_id)-1:
      session["switch_chapter"] = "chapters_on_left_side"
    if get_the_next_chapter_number(post_id) == 2:
      session["switch_chapter"] = "only_chapter"
    
    session["post_id"] = post_id
    session["public"] = public
    session["row_subject"] = row_subject
    session["inquiry"] = inquiry_on
    session["chapter_content"] = chapter_content

    return True
    