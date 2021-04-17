from app import app
from db import *
from queries_db import *

def save_the_chapter(post_id, public, row_comments_on, inquiry_on, chapter_number, text_rows, text_content, misc):
    try:
        sql = "SELECT id FROM chapters WHERE post_id=:post_id AND chapter_number=:chapter_number"
        result = db.session.execute(sql, {"post_id":post_id, "chapter_number":chapter_number})
        chapter_id = result.fetchone()

        if not chapter_id == None:
           return -1

        sql = "INSERT INTO chapters (post_id,public,row_comments_on,inquiry_on,chapter_number,text_rows,text_content,misc) VALUES (:post_id,:public,:row_comments_on,:inquiry_on,:chapter_number,:text_rows,:text_content,:misc)"
        db.session.execute(sql, {"post_id":post_id,"public":public,"row_comments_on":row_comments_on,"inquiry_on":inquiry_on,"chapter_number":chapter_number,"text_rows":text_rows,"text_content":text_content,"misc":misc})
        db.session.commit()

        return 0
    except Exception as e:
        print(e)
        return -2

def update_the_chapter(post_id, public, row_comments_on, inquiry_on, chapter_number, text_rows, text_content, misc):
    try:
        sql = "SELECT id FROM chapters WHERE post_id=:post_id AND chapter_number=:chapter_number"
        result = db.session.execute(sql, {"post_id":post_id, "chapter_number":chapter_number})
        chapter_id = result_fetchone()
        
        if chapter_id == None:
            return -1

        sql = "UPDATE chapters SET public=:public WHERE id=:id"
        db.session.execute(sql, {"public":public, "id":chapter_id})
        db.session.commit()

        sql = "UPDATE chapters SET row_comments_on=:row_comments_on WHERE id=:id"
        db.session.execute(sql, {"row_comments_on":row_comments_on, "id":chapter_id})
        db.session.commit()

        sql = "UPDATE chapters SET inquiry_on=:inquiry_on WHERE id=:id"
        db.session.execute(sql, {"inquiry_on":inquiry_on, "id":chapter_id})
        db.session.commit()

        sql = "UPDATE chapters SET text_rows=:text_rows WHERE id=:id"
        db.session.execute(sql, {"text_rows":text_rows, "id":chapter_id})
        db.session.commit()

        sql = "UPDATE chapters SET text_content=:text_content WHERE id=:id"
        db.session.execute(sql, {"text_content":text_content, "id":chapter_id})
        db.session.commit()

        sql = "UPDATE chapters SET misc=:misc WHERE id=:id"
        db.session.execute(sql, {"misc":misc, "id":chapter_id})
        db.session.commit()

        return 0
    except Exception as e:
        print(e)
        return -2

def update_the_chapter_numbers(post_id):
    try:
        sql = "SELECT id,chapter_number FROM chapters WHERE post_id=:post_id"
        result = db.session.execute(sql, {"post_id":post_id})
        chapter_info = result.fetchall()

        if chapter_info == None:
            return -1
        
        index = 1
        correct_number = 0
        
        for info in chapter_info:
            if not info[1] == index:
               correct_number = index 
               break
            index = index + 1

        if correct_number == 0:
            return 0

        sql = "UPDATE chapters SET chapter_number=:correct_number WHERE id=:id"
         
        index = 1
        fixed_number = correct_number

        for info in chapter_info:
            if index >= correct_number:
                db.session.execute(sql, {"correct_number":fixed_number, "id":info[0]})
                db.session.commit()
                fixed_number = fixed_number + 1

            index = index + 1

        return 0
    except Exception as e:
        print(e)
        return -2    

def remove_the_chapter(post_id,chapter_number):
    try:
        sql = "SELECT id FROM chapters WHERE post_id=:post_id AND chapter_number=:chapter_number"
        result = db.session.execute(sql, {"post_id":post_id, "chapter_number":chapter_number})
        chapter_id = result.fetchone()

        if chapter_id == None:
            return -1

        remove_the_queries(chapter_id[0])

        sql = "DELETE FROM chapters WHERE id=:id"
        db.session.execute(sql, {"id":chapter_id[0]})
        db.session.commit()

        return 0
    except Exception as e:
        print(e)
        return -2

def remove_the_chapters(post_id):
    try:
        sql = "SELECT id FROM chapters WHERE post_id=:post_id"
        result = db.session.execute(sql, {"post_id":post_id})
        chapters_id = result.fetchall()

        if chapters_id == None:
            return -1

        for chapter_id in chapters_id:
            remove_the_queries(chapter_id[0])  

        sql = "DELETE FROM chapters WHERE post_id=:post_id"
        db.session.execute(sql, {"post_id":post_id})   
        db.session.commit() 

        return 0
    except Exception as e:
        print(e)
        return -2

def get_the_chapter(post_id, chapter_number):
    try:
        sql = "SELECT id FROM chapters WHERE post_id=:post_id AND chapter_number=:chapter_number"
        result = db.session.execute(sql, {"post_id":post_id, "chapter_number":chapter_number})
        chapter_id = result.fetchone()

        if chapter_id == None:
            return None

        sql = "SELECT id,post_id,public,row_comments_on,inquiry_on,chapter_number,text_rows,text_content,misc FROM chapters WHERE id=:id"
        result = db.session.execute(sql, {"id":chapter_id[0]})
        chapter = result.fetchone()

        return chapter
    except Exception as e:
        print(e)
        return None

def get_the_next_chapter_number(post_id):
    try:
        sql = "SELECT chapter_number FROM chapters WHERE post_id=:post_id ORDER BY chapter_number DESC"
        result = db.session.execute(sql, {"post_id":post_id})
        last_chapter_number = result.fetchone()

        if last_chapter_number == None:
            return 1 

        return last_chapter_number[0] + 1
    except Exception as e:
        print(e)
        return 0

def get_the_chapter_numbers(post_id):
    try:
        sql = "SELECT chapter_number FROM chapters WHERE post_id=:post_id"
        result = db.session.execute(sql, {"post_id":post_id})
        chapter_numbers = result.fetchall()

        if chapter_numbers == None:
            return None

        return chapter_numbers
    except Exception as e:
        print(e)
        return None