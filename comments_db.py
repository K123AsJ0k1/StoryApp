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
        return -2

def remove_the_comment(id):
    try:
        sql = "DELETE FROM comments WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return 0
    except Exception as e:
        print(e)    
        return -2

def remove_the_comments(post_id):
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

def remove_the_chapter_row_subjects(post_id,chapter_number):
    try:
        sql = "SELECT id from comments WHERE post_id=:post_id AND chapter_number=:chapter_number AND row_id=0 AND row_comment=true"
        result = db.session.execute(sql, {"post_id":post_id, "chapter_number":chapter_number})
        chapter_subjects_id = result.fetchall()

        if not chapter_subjects_id == None:
            for chapter_subject_id in chapter_subjects_id:
                if remove_the_subject_comments(post_id,chapter_number,chapter_subject_id[0]) == -2:
                   return -2

            for chapter_subject_id in chapter_subjects_id:
                if remove_the_comment(chapter_subject_id[0]) == -2:
                   return -2 

        return 0
    except Exception as e:
        print(e)    
        return -2

def remove_the_subject_comments(post_id,chapter_number,subject_id):
    try:
        sql = "SELECT id from comments WHERE post_id=:post_id AND chapter_number=:chapter_number AND row_id=:subject_id AND row_comment=true"
        result = db.session.execute(sql, {"post_id":post_id, "chapter_number":chapter_number, "subject_id":subject_id})
        subject_comments_id = result.fetchall()

        if not subject_comments_id == None:
            for subject_comment_id in subject_comments_id:
                remove_the_comment(subject_comment_id[0])
        
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
        #Korjaa se, että tässä tulee general_comment ja row_id mukaan
        sql = "SELECT id,user_id,post_id,row_id,general_comment,chapter_number_on,chapter_number,comment FROM comments WHERE post_id=:post_id AND general_comment=true"
        result = db.session.execute(sql, {"post_id":post_id})
        general_comments = result.fetchall()

        if general_comments == None:
           return None

        return general_comments
    except Exception as e:
        print(e)    
        return None

def get_chapter_row_subjects(post_id,chapter_number):
    try:
        sql = "SELECT id,user_id,post_id,row_id,chapter_number_on,chapter_number,comment FROM comments WHERE post_id=:post_id AND chapter_number=:chapter_number AND row_id=0 AND row_comment=true"
        result = db.session.execute(sql, {"post_id":post_id, "chapter_number":chapter_number})
        chapter_subjects = result.fetchall()

        if chapter_subjects == None:
           return None
        
        return chapter_subjects
    except Exception as e:
        print(e)    
        return None   

def get_subject_comments(post_id,chapter_number,row_id):
    try:
        sql = "SELECT id,user_id,post_id,row_id,chapter_number,comment FROM comments WHERE post_id=:post_id AND chapter_number=:chapter_number AND row_id=:row_id AND row_comment=true"
        result = db.session.execute(sql , {"post_id":post_id, "chapter_number":chapter_number, "row_id":row_id})
        subject_comments = result.fetchall()

        if subject_comments == None:
            return None
        
        return subject_comments
    except Exception as e:
        print(e)    
        return None   