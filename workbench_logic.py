from app import app
from flask import redirect, render_template, request, session
from users_logic import *
from users_db import *
from posts_db import *
from chapters_db import *
from text import *
from misc import *
    
def workbench_create_post_mode():
    session["workbench_mode"] = "create_post"

def workbench_create_chapter_mode():
    session["workbench_mode"] = "create_chapter"

def workbench_session_deletion():
    if 'workbench_mode' in session:
      del session["workbench_mode"]
    if 'workbench' in session:
      del session["workbench"]

def profile_session_deletion():
    if 'profile' in session:
      del session["profile"]

def view_session_deletion():
    if 'view' in session:
      del session["view"]

def get_post_session_deletion():
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

def get_chapter_session_deletion():
    if 'given_chapter_post_id' in session:
      del session["given_chapter_post_id"]
    if 'given_chapter_public' in session:
      del session["given_chapter_public"]
    if 'given_chapter_subject' in session:
      del session["given_chapter_subject"]
    if 'given_chapter_inquiry' in session:
      del session["given_chapter_inquiry"]
    if 'given_chapter_number' in session:
      del session["given_chapter_number"]
    if 'given_chapter_content' in session:
      del session["given_chapter_content"]
    if 'given_chapter_misc' in session:
      del session["given_chapter_misc"]
  
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
      session["workbench"] = "title_doesnt_fulfill_requirements"
      return False

    if not check_title_requirements(genre):
      session["workbench"] = "genre_doesnt_fulfill_requirements"
      return False
    
    misc = create_misc(rating,genre)
    
    check_number = save_the_post(user_id, visible, general_comments_on, name, misc)

    if check_number == -1:
      session["workbench"] = "post_name_exists"
      return False

    if check_number == -2:
      session["workbench"] = "database_error"
      return False
    
    return True

def save_chapter(post_id,chapter_public,row_comments,inquiry,text_content):
    if post_id == None:
      session["workbench"] = "database_error"
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
      session["workbench"] = "text_doesnt_fulfill_requirements"
      return False

    chapter_number = get_the_next_chapter_number(post_id)

    if chapter_number == 0:
      session["workbench"] = "database_error"
      return False

    text_rows = rows(text_content)
    text_source = get_source_text(text_content)
   
    misc = ""

    check_number = save_the_chapter(post_id, public, row_comments_on, inquiry_on, chapter_number, text_rows, text_source, misc)
    
    if check_number == -1:
      session["workbench"] = "database_error"
      return False
    if check_number == -2:
      session["workbench"] = "database_error"
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

    session["workbench_mode"] = "update_post"
    return True

def get_chapter(post_id,chapter_number):
    chapter = get_the_chapter(post_id, chapter_number)

    if chapter == None:
      return False
    
    session["given_chapter_post_id"] = chapter[1]
    
    check_public = chapter[2]
    
    session["given_chapter_public"] = "chapter_public_false"
    if check_public:
      session["given_chapter_public"] = "chapter_public_true"

    check_subject = chapter[3]
    
    session["given_chapter_subject"] = "chapter_subject_false"
    if check_subject:
      session["given_chapter_subject"] = "chapter_subject_true"

    check_inquiry = chapter[4]
    
    session["given_chapter_inquiry"] = "chapter_inquiry_false"
    if check_inquiry:
      session["given_chapter_inquiry"] = "chapter_inquiry_true"
  
    session["given_chapter_number"] = chapter[5]
    session["given_chapter_content"] = get_original_text(chapter[7])
    session["given_chapter_misc"] = chapter[8]
    
    session["workbench_mode"] = "update_chapter"
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

    if not check_title_requirements(new_name):
      session["workbench"] = "title_doesnt_fulfill_requirements"
      return False

    if not check_title_requirements(genre):
      session["workbench"] = "genre_doesnt_fulfill_requirements"
      return False

    misc = create_misc(rating,genre)
    
    check_number = update_the_post(old_name, user_id, visible, general_comments_on, new_name, misc)
    
    if check_number == -1:
      session["workbench"] = "target_post_doesnt_exist"
      return False

    if check_number == -2:
      session["workbench"] = "database_error"
      return False

    if check_number == -3:
      session["workbench"] = "database_error"
      return False
    
    return True

def update_chapter(post_id, public, row_comments_on, inquiry_on, chapter_number, text_content, misc):
    if post_id == None:
      session["workbench"] = "database_error"
      return False

    if not check_text_requirements(text_content):
      session["workbench"] = "text_doesnt_fulfill_requirements"
      return False

    text_rows = rows(text_content)
    text_source = get_source_text(text_content)
    
    check_number = update_the_chapter(post_id, public, row_comments_on, inquiry_on, chapter_number, text_rows, text_source, misc)

    if check_number == -1:
      session["workbench"] = "target_chapter_doesnt_exist"
      return False

    if check_number == -2:
      session["workbench"] = "database_error"
      return False

    return True
    
def remove_post(user_id, post_id):
    post = get_the_post(post_id)

    if post == None:
      session["profile"] = "database_error"
      return False
    
    check_number = remove_the_post(user_id,post[4])
    
    if check_number == -1:
      session["profile"] = "target_post_doesnt_exist"
      return False

    if check_number == -2:
      session["profile"] = "database_error"
      return False

    if check_number == -3:
      session["profile"] = "database_error"
      return False
    
    session["profile"] = "post_removed"
    return True

def remove_chapter(post_id,chapter_number):
    check_number = remove_the_chapter_row_subjects(post_id,chapter_number)
    
    if check_number == -2:
      session["view"] = "database_error"
      return False

    check_number = remove_the_chapter(post_id,chapter_number)
    
    if check_number == -1:
      session["view"] = "target_chapter_doesnt_exist"
      return False
    
    if check_number == -2:
      session["view"] = "database_error"
      return False

    check_number = update_the_chapter_numbers(post_id)

    if check_number == -1:
      session["view"] = "target_chapter_doesnt_exist"
      return False

    if check_number == -2:
      session["view"] = "database_error"
      return False
    
    session["profile"] = "chapter_removed"
    return True

def get_post_creators():
    posts = get_posts()

    if posts == None:
      return None

    post_creators = {}

    for post in posts:
      user = get_the_user(post[1])
      post_creators[post[0]] = user[1]

    return post_creators

def get_chapter_posts():
    chapters = get_chapters()
    
    if chapters == None:
      return None
  
    chapter_post_list = {}

    for chapter in chapters:
      post = get_the_post(chapter[1])
      chapter_post_list[chapter[0]] = post[4]

    return chapter_post_list

def get_posts_amount():
    posts = get_posts()

    if posts == None:
      return 0

    return len(posts)

def get_public_post_amount():
    public_posts = get_public_posts()
    
    if public_posts == None:
      return 0
    
    return len(public_posts)

def check_post_owner(user_name,post_id):
    post_owner = get_post_creator(post_id)

    if not user_name == post_owner:
      return False

    return True

def get_chapters_amount():
    chapters = get_chapters()
    
    if chapters == None:
      return 0

    return len(chapters)

def get_public_chapters_amount():
    chapters = get_chapters()

    if chapters == None:
      return 0
    
    public_chapters = []

    for chapter in chapters:
        if chapter[2]:
          public_chapters.append(chapter)

    return len(public_chapters)

def get_largest_chapter_number():
    chapters = get_chapters()

    if chapters == None:
      return 0

    biggest_chapter_number = 0

    for chapter in chapters:
      if biggest_chapter_number < chapter[5]:
        biggest_chapter_number = chapter[5]

    return biggest_chapter_number

def get_largest_row_amount():
    chapters = get_chapters()

    if chapters == None:
      return 0

    biggest_row_amount = 0

    for chapter in chapters:
      if biggest_row_amount < chapter[6]:
        biggest_row_amount = chapter[6]

    return biggest_row_amount


    


    