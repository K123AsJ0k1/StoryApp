from app import app

def rows(text):
    return len(text.split("\r\n"))

def check_title_requirements(title):
    text_lenght == len(title)

    if text_lenght == 0:
        return False
    
    if text_lenght > 50:
        return False

    return True
       

def check_text_requirements(text):
    text_lenght = len(text)
    
    if text_lenght == 0:
       return False
    
    if text_lenght <= 100:
       return True
    
    if text.find("\r\n") == -1:
       return False
    
    line_size = 0
    for letter in text:
        if letter == "\r":
            if line_size > 100:
                return False
            line_size = 0
            continue
        if letter == "\n":
            continue
        line_size = line_size + 1
        if line_size > 100:
            return False
    
    return True
        

def get_source_text(text):
    text_rows = text.split("\r\n")
    return "|".join(text_row for text_row in text_rows)

def get_source_text_array(source_text):
    return source_text.split("|")


