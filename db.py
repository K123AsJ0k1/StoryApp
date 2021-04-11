from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

def create_user(username, password):
    try:
        sql = "SELECT id FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        query = result.fetchone()

        if not query == None:
          return False
         
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username,password,role) VALUES (:username,:password,:role)"
        db.session.execute(sql, {"username":username,"password":hash_value,"role":0})
        db.session.commit()
        
        return True
    except Exception as e:
        print(e)
        return False

def login_user(username, password):
    try:
        sql = "SELECT password FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        user_password = result.fetchone()

        if user_password == None:
          return -1

        hash_value = user_password[0]
        if not check_password_hash(hash_value,password):
          return -2

        return 0
    except Exception as e:
        print(e)
        return -3

def get_user_id(username):
    try:
        sql = "SELECT id FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        user_id = result.fetchone()

        if user_id == None:
           return 0

        return user_id[0]
    except Exception as e:
        print(e)
        return 0

def save_post(user_id, visible, general_comments_on, name, misc):
    try:
        sql = "SELECT id FROM posts WHERE name=:name"
        result = db.session.execute(sql, {"name":name})
        post_id = result.fetchone()
        
        if not post_id == None:
            return -1

        sql = "INSERT INTO posts (user_id,visible,general_comments_on,name,misc) VALUES (:user_id,:visible,:general_comments_on,:name,:misc)"
        db.session.execute(sql, {"user_id":user_id,"visible":visible,"general_comments_on":general_comments_on,"name":name,"misc":misc})
        db.session.commit()
        
        return 0
    except Exception as e:
        print(e)
        return -2

def update_the_post(old_name, user_id, visible, general_comments_on, new_name, misc):
    try:
        sql = "SELECT id,user_id FROM posts WHERE name=:name"
        result = db.session.execute(sql, {"name":old_name})
        check = result.fetchone()

        if check == None:
            return -1

        post_id = check[0]
        username_id = check[1]

        if not username_id == user_id:
           return -2
        
        sql = "UPDATE posts SET visible=:visible WHERE id=:id"
        db.session.execute(sql, {"visible":visible,"id":post_id})
        db.session.commit()

        sql = "UPDATE posts SET general_comments_on=:general_comments_on WHERE id=:id"
        db.session.execute(sql, {"general_comments_on":general_comments_on,"id":post_id})
        db.session.commit()

        sql = "UPDATE posts SET name=:name WHERE id=:id"
        db.session.execute(sql, {"name":new_name,"id":post_id})
        db.session.commit()

        sql = "UPDATE posts SET misc=:misc WHERE id=:id"
        db.session.execute(sql, {"misc":misc,"id":post_id})
        db.session.commit()

        return 0
    except Exception as e:
        print(e)
        return -3

def remove_post(user_id,name):
    try:
        sql = "SELECT id,user_id FROM posts WHERE name=:name"
        result = db.session.execute(sql, {"name":name})
        check = result.fetchone()
        
        post_id = check[0]
        username_id = check[1]

        if check == None:
            return -1
        
        if not username_id == user_id:
            return -2
        
        check_number = remove_the_chapters(post_id)

        if check_number == -1:
            return -1

        if check_number == -2:
            return -3

        check_number = remove_the_general_comments(post_id)
        
        if check_number == -2:
            return -3

        sql = "DELETE FROM posts WHERE id=:id"
        db.session.execute(sql, {"id":post_id})
        db.session.commit()

        return 0
    except Exception as e:
        print(e)
        return -3

def get_post_creator(post_id):
    try:
        sql = "SELECT user_id FROM posts WHERE id=:id"
        result = db.session.execute(sql, {"id":post_id})
        user_id = result.fetchone()

        if user_id == None:
            return None
        
        sql = "SELECT username FROM users WHERE id=:user_id"
        result = db.session.execute(sql, {"user_id":user_id[0]})
        username = result.fetchone()

        return username[0]
    except Exception as e:
        print(e)
        return None

def get_the_post(post_id):
    try:
        sql = "SELECT id,user_id,visible,general_comments_on,name,misc FROM posts WHERE id=:post_id"
        result = db.session.execute(sql, {"post_id":post_id})
        post = result.fetchone()
        return post
    except Exception as e:
        print(e)
        return None   

def get_profile_post(user_id,name):
    try:
        sql = "SELECT id,user_id FROM posts WHERE name=:name"
        result = db.session.execute(sql, {"name":name})
        check = result.fetchone()
        post_id = check[0]
        username_id = check[1]

        if check == None:
            return None
        
        if not username_id == user_id:
            return None

        sql = "SELECT id,user_id,visible,general_comments_on,name,misc FROM posts WHERE id=:id"
        result = db.session.execute(sql, {"id":post_id})
        post = result.fetchone()
        
        if post == None:
            return None

        return post
    except Exception as e:
        print(e)
        return None

def get_profile_posts(user_id):
    try:
        sql = "SELECT id,visible,general_comments_on,name,misc FROM posts WHERE user_id=:user_id"
        result = db.session.execute(sql, {"user_id":user_id})
        posts = result.fetchall()
        return posts
    except Exception as e:
        print(e)
        return None

def get_public_posts():
    try:
        sql = "SELECT id,user_id,visible,general_comments_on,name,misc FROM posts WHERE visible=true"
        result = db.session.execute(sql)
        posts = result.fetchall()
        
        if posts == None:
            return None
        
        posts_with_chapters = []

        for post in posts:
            if check_post_chapters(post[0]):
               posts_with_chapters.append(post)
        
        return posts_with_chapters
    except Exception as e:
        print(e)
        return None

def check_post_chapters(post_id):
    try:
        sql = "SELECT id FROM chapters WHERE post_id=:post_id"
        result = db.session.execute(sql, {"post_id":post_id})
        chapter_id = result.fetchall()
        
        if len(chapter_id) == 0:
            return False
        
        return True
    except Exception as e:
        print(e)
        return None

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
           
    

    





    
    