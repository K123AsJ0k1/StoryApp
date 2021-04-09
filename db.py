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
        
        # Tätä ennen on tuhottava postaukseen liitettyn chapterit, commentit, kyselyt ja kyselyiden vastaukset

        sql = "DELETE FROM posts WHERE id=:id"
        db.session.execute(sql, {"id":post_id})
        db.session.commit()

        return 0
    except Exception as e:
        print(e)
        return -3

def get_post_creator(id):
    try:
        sql = "SELECT user_id FROM posts WHERE id=:id"
        result = db.session.execute(sql, {"id":id})
        user_id = result.fetchone()

        if user_id == None:
            return None

        sql = "SELECT username FROM users WHERE id=:user_id"
        result = db.session.execute(sql, {"user_id":user_id})
        username = result.fetchone()

        return username[0]
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
        sql = "SELECT id,visible,general_comments_on,name,misc FROM posts WHERE visible=true"
        result = db.session.execute(sql)
        posts = result.fetchall()
        return posts
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

# Luo update_the_chapter_numbers, jossa jokainen postauksen chapter_numberit paikataa siten

def remove_the_chapter(post_id,chapter_number):
    try:
        sql = "SELECT id FROM chapters WHERE post_id=:post_id AND chapter_number=:chapter_number"
        result = db.session.execute(sql, {"post_id":post_id, "chapter_number":chapter_number})
        chapter_id = result_fetchone()

        if chapter_id == None:
            return -1

        # tätä ennen on tuhottava chapteriin liitetyn kyselyt ja kommentit

        sql = "DELETE FROM chapters WHERE id=:id"
        db.session.execute(sql, {"id":chapter_id})
        db.session.commit()

        return 0
    except Exception as e:
        print(e)
        return -2

def remove_the_chapters(post_id):
    try:
        sql = "SELECT id FROM chapters WHERE post_id=:post_id"
        result = db.session.execute(sql, {"post_id":post_id})
        chapter_ids = result.fetchall()

        if chapter_ids == None:
            return -1

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
        sql = "SELECT chapter_number WHERE post_id=:post_id"
        result = db.session.execute(sql, {"post_id":post_id})
        chapter_numbers = result.fetchall()

        if chapter_numbers == None:
            return None

        return chapter_numbers
    except Exception as e:
        print(e)
        return None




    
    