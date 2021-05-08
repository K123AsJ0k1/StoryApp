from app import app
from flask import redirect, render_template, request, session
from users_db import *
from posts_db import *
from chapters_db import *
from comments_db import *
from queries_db import *
from answers_db import *
from text import *

def query_none_mode():
    session["query_mode"] = "0"

def query_view_mode():
    session["query_mode"] = "1"

def query_create_mode():
    session["query_mode"] = "2"

def query_answers_mode():
    session["query_mode"] = "3"

def query_answer_mode():
    session["query_mode"] = "4"

def save_question(user_id,post_id,chapter_number,question):   
    chapter = get_the_chapter(post_id,chapter_number)

    if chapter == None:
      return False

    chapter_id = chapter[0]

    if not check_text_requirements(question):
      return False

    misc = ""

    check_number = save_the_query(user_id,chapter_id,question,misc)

    if check_number == -2:
      return False
   
    return True

def remove_question(question_id):   
    check_number = remove_the_query(question_id)

    if check_number == -2:
      return False

    return True

def save_answer(user_id, query_id, answer): 
    query = get_the_query(query_id)
   
    if query == None:
      return False
   
    if not check_text_requirements(answer):
      return False

    misc = ""

    check_number = save_the_answer(user_id, query_id, answer, misc)

    if check_number == -2:
      return False

    return True

def remove_answer(answer_id): 
   check_number = remove_the_answer(answer_id)

   if check_number == -2:
      return False
   
   return True

def get_queries_amount():
    queries = get_queries()

    if queries == None:
      return 0

    return len(queries)

def get_answers_amount():
    answers = get_answers()

    if answers == None:
      return 0

    return len(answers)


