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
    session["query_mode"] = "none_mode"

def query_view_mode():
    session["query_mode"] = "view_mode"

def query_create_mode():
    session["query_mode"] = "create_mode"

def query_answers_mode():
    session["query_mode"] = "answers_mode"

def query_answer_mode():
    session["query_mode"] = "answer_mode"

def query_session_deletion():
    if 'query_mode' in session:
      del session["query_mode"]
    if 'query' in session:
      del session["query"]

def save_question(user_id,post_id,chapter_number,question):   
    chapter = get_the_chapter(post_id,chapter_number)

    if chapter == None:
      session["query"] = "database_error"
      return False

    chapter_id = chapter[0]

    if not check_text_requirements(question):
      session["query"] = "question_doesnt_fulfill_requirements"
      return False

    misc = ""

    check_number = save_the_query(user_id,chapter_id,question,misc)

    if check_number == -2:
      session["query"] = "database_error"
      return False
   
    return True

def remove_question(question_id):   
    check_number = remove_the_query(question_id)

    if check_number == -2:
      session["query"] = "database_error"
      return False

    return True

def save_answer(user_id, query_id, answer): 
    query = get_the_query(query_id)
   
    if query == None:
      session["query"] = "database_error"
      return False
   
    if not check_text_requirements(answer):
      session["query"] = "answer_doesnt_fulfill_requirements"
      return False

    misc = ""

    check_number = save_the_answer(user_id, query_id, answer, misc)

    if check_number == -2:
      session["query"] = "database_error"
      return False

    return True

def remove_answer(answer_id): 
   check_number = remove_the_answer(answer_id)

   if check_number == -2:
      session["query"] = "database_error"
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

def get_query_owners():
    queries = get_queries()

    if queries == None:
      return None

    query_owner_list = {}

    for query in queries:
      user = get_the_user(query[1])
      query_owner_list[query[0]] = user[1]

    return query_owner_list

def get_query_posts():
    queries = get_queries()

    if queries == None:
      return None

    query_post_list = {}

    for query in queries:
      chapter = get_the_chapter_with_id(query[2])
      post = get_the_post(chapter[1])
      query_post_list[query[0]] = post[4]
      
    return query_post_list

def get_query_chapter_numbers():
    queries = get_queries()

    if queries == None:
      return None

    query_chapter_numbers_list = {}

    for query in queries:
      chapter = get_the_chapter_with_id(query[2])
      query_chapter_numbers_list[query[0]] = chapter[5]

    return query_chapter_numbers_list

def get_answer_owner():
    answers = get_answers()

    if answers == None:
      return None

    answer_owner_list = {}

    for answer in answers:
      user = get_the_user(answer[1])
      answer_owner_list[answer[0]] = user[1]

    return answer_owner_list

def get_answer_chapter_numbers():
    answers = get_answers()

    if answers == None:
      return None

    answer_chapter_numbers_list = {}

    for answer in answers:
      query = get_the_query(answer[2])
      chapter = get_the_chapter_with_id(query[2])
      answer_chapter_numbers_list[answer[0]] = chapter[5]

    return answer_chapter_numbers_list

def get_answer_posts():
    answers = get_answers()

    if answers == None:
      return None

    answer_post_list = {}

    for answer in answers:
      query = get_the_query(answer[2])
      chapter = get_the_chapter_with_id(query[2])
      post = get_the_post(chapter[1])
      answer_post_list[answer[0]] = post[4]

    return answer_post_list





