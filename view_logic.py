from app import app
from flask import redirect, render_template, request, session
from users_logic import *
from posts_db import *
from chapters_db import *
from text import *

def view_none_mode():
    session["view_mode"] = "0"

def view_read_mode():
    session["view_mode"] = "1"

def remove_chapter_content_session():
    if "chapter_content" in session:
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

    inquiry_on = chapter[4]
   
    chapter_content = get_source_text_array(chapter[7])
       
    # Edellinen luku, seuraava luku ja valittavat luku asiat
    
    # Row comment asiat
    
    # chapter_rows = chapter[6]

    # row_comments_on = chapter[3]
   
    session["switch_chapter"] = "0"

    if chapter_number == 1:
      session["switch_chapter"] = "1"
    if chapter_number == get_the_next_chapter_number(post_id)-1:
      session["switch_chapter"] = "2"
    if get_the_next_chapter_number(post_id) == 2:
      session["switch_chapter"] = "3"
    
    session["post_id"] = post_id
    session["inquiry"] = inquiry_on
    session["chapter_content"] = chapter_content

    return True
    