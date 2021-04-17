from app import app
from db import *

def save_the_answer(user_id, query_id, answer, misc):
    try:
        sql = "INSERT INTO answers (user_id,query_id,answer,misc) VALUES (:user_id,:query_id,:answer,:misc)"
        db.session.execute(sql, {"user_id":user_id, "query_id": query_id, "answer": answer, "misc":misc})
        db.session.commit()
        return 0
    except Exception as e:
        print(e)    
        return -2

def remove_the_answer(answer_id):
    try:
        sql = "DELETE FROM answers WHERE id=:answer_id"
        db.session.execute(sql, {"answer_id":answer_id})
        db.session.commit()
        return 0
    except Exception as e:
        print(e)    
        return -2

def remove_the_answers(query_id):
    try:
        sql = "DELETE FROM answers WHERE query_id=:query_id"
        db.session.execute(sql, {"query_id":query_id})
        db.session.commit()
        return 0
    except Exception as e:
        print(e)    
        return -2

def get_answer_creator(answer_id):
    try:
        sql = "SELECT user_id FROM answers WHERE id=:answer_id"
        result = db.session.execute(sql, {"answer_id":answer_id})
        user_id = result.fetchone()

        if user_id == None:
           return None

        sql = "SELECT username FROM users WHERE id=:user_id"
        result = db.session.execute(sql, {"user_id":user_id[0]})
        username = result.fetchone()
        
        if username == None:
            return None

        return username[0]
    except Exception as e:
        print(e)    
        return None 

def get_the_query_answers(query_id):
    try:
        sql = "SELECT id,user_id,query_id,answer,misc FROM answers WHERE query_id=:query_id"
        result = db.session.execute(sql, {"query_id":query_id})
        answers = result.fetchall()

        if answers == None:
           return -1

        return answers
    except Exception as e:
        print(e)    
        return -2   