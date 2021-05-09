from app import app
from db import *
from chapters_db import *
from comments_db import *

def save_the_post(user_id, visible, general_comments_on, name, misc):
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
           return -3
        
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
        return -2

def remove_the_post(user_id,name):
    try:
        sql = "SELECT id,user_id FROM posts WHERE name=:name"
        result = db.session.execute(sql, {"name":name})
        check = result.fetchone()
        
        post_id = check[0]
        username_id = check[1]

        if check == None:
            return -1
        
        if not username_id == user_id:
            return -3
        
        check_number = remove_the_chapters(post_id)

        if check_number == -1:
            return -1

        if check_number == -2:
            return -2

        check_number = remove_the_comments(post_id)
        
        if check_number == -2:
            return -2

        sql = "DELETE FROM posts WHERE id=:id"
        db.session.execute(sql, {"id":post_id})
        db.session.commit()

        return 0
    except Exception as e:
        print(e)
        return -2

def check_if_post_exists(post_id):
    try:
        sql = "SELECT id FROM posts WHERE id=:post_id"
        result = db.session.execute(sql, {"post_id":post_id})
        post = result.fetchone()
        
        if post == None:
           return -1

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

def get_posts():
    try:
        sql = "SELECT id,user_id,visible,general_comments_on,name,misc FROM posts"
        result = db.session.execute(sql)
        posts = result.fetchall()

        if posts == None:
            return None

        return posts
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