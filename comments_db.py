from app import app
from db import *

def save_the_comment(user_id, post_id, row_id, general_comment, row_comment, chapter_number_on, chapter_number, comment):
    try:
        sql = "INSERT INTO comments (user_id,post_id,row_id,general_comment,row_comment,chapter_number_on,chapter_number,comment) VALUES (:user_id,:post_id,:row_id,:general_comment,:row_comment,:chapter_number_on,:chapter_number,:comment)"
        db.session.execute(sql, {"user_id":user_id,"post_id":post_id,"row_id":row_id,"general_comment":general_comment,"row_comment":row_comment,"chapter_number_on":chapter_number_on,"chapter_number":chapter_number,"comment":comment})
        db.session.commit()
        return 0
    except Exception as e:
        print(e)    
        return -1

def remove_the_comment(id):
    try:
        sql = "DELETE FROM comments WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return 0
    except Exception as e:
        print(e)    
        return -1

def remove_the_general_comments(post_id):
    try:
        sql = "SELECT id FROM comments WHERE post_id=:post_id"
        result = db.session.execute(sql, {"post_id":post_id})
        comments_id = result.fetchall()

        if not comments_id == None:
           for comment_id in comments_id:
               remove_the_comment(comment_id[0])

        return 0
    except Exception as e:
        print(e)    
        return -2  

def get_comment_creator(comment_id):
    try:
        sql = "SELECT user_id FROM comments WHERE id=:comment_id"
        result = db.session.execute(sql, {"comment_id": comment_id})
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
        
def get_post_general_comments(post_id):
    try:
        sql = "SELECT id,user_id,post_id,row_id,general_comment,chapter_number_on,chapter_number,comment FROM comments WHERE post_id=:post_id AND general_comment=true"
        result = db.session.execute(sql, {"post_id":post_id})
        general_comments = result.fetchall()

        if general_comments == None:
           return None

        return general_comments
    except Exception as e:
        print(e)    
        return None