CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    role INTEGER
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id integer REFERENCES users,
    visible BOOLEAN NOT NULL,
    general_comments_on BOOLEAN NOT NULL,
    name TEXT,
    misc TEXT
);

CREATE TABLE chapters (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts,
    public BOOLEAN NOT NULL,
    row_comments_on BOOLEAN NOT NULL,
    inquiry_on BOOLEAN NOT NULL,
    chapter_number INTEGER,
    text_rows INTEGER,
    text_content TEXT,
    misc TEXT
);

CREATE TABLE comments (
     id SERIAL PRIMARY KEY,
     user_id INTEGER REFERENCES users,
     post_id INTEGER REFERENCES posts,
     row_id INTEGER,
     general_comment BOOLEAN NOT NULL,
     row_comment BOOLEAN NOT NULL,
     chapter_number_on BOOLEAN NOT NULL,
     chapter_number INTEGER,
     comment TEXT
);

CREATE TABLE queries (
   id SERIAL PRIMARY KEY,
   user_id INTEGER REFERENCES users,
   chapter_id INTEGER REFERENCES chapters,
   question TEXT,
   misc TEXT
);

CREATE TABLE answers (
   id SERIAL PRIMARY KEY,
   user_id INTEGER REFERENCES users,
   query_id INTEGER REFERENCES queries,
   answer TEXT,
   misc TEXT
);