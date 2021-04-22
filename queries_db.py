from app import app
from db import *
from answers_db import *

def save_the_query(user_id,chapter_id,question,misc):
    try:
        sql = "INSERT INTO queries (user_id,chapter_id,question,misc) VALUES (:user_id,:chapter_id,:question,:misc)"
        db.session.execute(sql, {"user_id":user_id, "chapter_id":chapter_id, "question":question, "misc":misc})
        db.session.commit()
        return 0
    except Exception as e:
        print(e)    
        return -2

def remove_the_query(query_id):
    try:
        sql = "DELETE FROM answers WHERE query_id=:query_id"
        db.session.execute(sql, {"query_id":query_id})
        db.session.commit()

        sql = "DELETE FROM queries WHERE id=:query_id"
        db.session.execute(sql, {"query_id":query_id})
        db.session.commit()
        return 0
    except Exception as e:
        print(e)    
        return -2

def remove_the_queries(chapter_id):
    try:
        sql = "SELECT id FROM queries WHERE chapter_id=:chapter_id"
        result = db.session.execute(sql, {"chapter_id":chapter_id})
        queries_id = result.fetchall()

        if not queries_id == None:
           for query_id in queries_id:
               remove_the_answers(query_id[0])
        
        sql = "DELETE FROM queries WHERE chapter_id=:chapter_id"
        db.session.execute(sql, {"chapter_id":chapter_id})
        db.session.commit()
        return 0
    except Exception as e:
        print(e)    
        return -2

def get_the_query(query_id):
    try:
        sql = "SELECT id,user_id,chapter_id,question,misc FROM queries WHERE id=:query_id"
        result = db.session.execute(sql, {"query_id":query_id})
        query = result.fetchone()
        
        if query == None:
            return None

        return query
    except Exception as e:
        print(e)    
        return None

def get_the_chapter_queries(chapter_id):
    try:
        sql = "SELECT id,user_id,chapter_id,question,misc FROM queries WHERE chapter_id=:chapter_id"
        result = db.session.execute(sql, {"chapter_id":chapter_id})
        queries = result.fetchall()

        if queries == None:
           return -1

        return queries
    except Exception as e:
        print(e)    
        return -2