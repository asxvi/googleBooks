import psycopg
from dotenv import load_dotenv
import os

load_dotenv()
pg_host = os.getenv('PG_HOST')
pg_username = os.getenv('PG_USERNAME')
pg_password = os.getenv('PG_PASSWORD')

# https://www.psycopg.org/psycopg3/docs/basic/usage.html
# https://www.postgresql.org/docs/current/ddl.html

with psycopg.connect(f"dbname=booksdb user={pg_username} password={pg_password} host={pg_host} port=5432") as conn:
    with conn.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS book (
                    bookId SERIAL PRIMARY KEY,
                    isbn BIGINT,
                    date DATE,
                    pageCount SMALLINT,
                    largeImage VARCHAR(100),
                    smallImage VARCHAR(100),
                    selfLink VARCHAR(100),
                    ebook BOOLEAN,
                    epub BOOLEAN,
                    pdf BOOLEAN
                );

            CREATE TABLE IF NOT EXISTS author (          
                    authorId SERIAL PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE
                );
            
            CREATE TABLE IF NOT EXISTS book_author (
                    book_authorId SERIAL PRIMARY KEY,
                    authorId INT REFERENCES author(authorId),
                    bookId INT REFERENCES book(bookId)            
                );
        ''')
    conn.commit()
