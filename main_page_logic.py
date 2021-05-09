from app import app
from flask import redirect, render_template, request, session

from users_logic import *
from main_page_logic import *
from profile_logic import *
from workbench_logic import *
from view_logic import *
from comments_logic import *
from query_logic import *
from administration_logic import *

def main_page_proxy_init_problem():
    session["main"] = "database_error"

def main_page_other_page_session_deletion():
    sign_up_session_deletion()
    
    log_in_session_deletion()
    
    get_post_session_deletion()
    
    get_chapter_session_deletion()
    
    view_chapter_session_deletion()
    
    profile_session_deletion()
    
    workbench_session_deletion()
    
    get_post_session_deletion()
    
    get_chapter_session_deletion()
    
    comment_session_deletion()
    
    query_session_deletion()

    admin_session_deletion()