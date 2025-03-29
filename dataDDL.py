import psycopg
import os
from dotenv import load_dotenv
from apiClean import fetchData

load_dotenv()
pg_host = os.getenv('PG_HOST')
pg_username = os.getenv('PG_USERNAME')
pg_password = os.getenv('PG_PASSWORD')

# https://www.psycopg.org/psycopg3/docs/basic/usage.html
# https://www.postgresql.org/docs/current/ddl.html

def connectDB():
    return (psycopg.connect(f"dbname=booksdb user={pg_username} password={pg_password} host={pg_host} port=5432"))


def createTables():
    conn = connectDB()
    cursor = conn.cursor()     
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS book (
                bookId SERIAL PRIMARY KEY,
                isbn BIGINT UNIQUE NOT NULL,
                date DATE,
                pageCount SMALLINT,
                largeImage VARCHAR(100),
                smallImage VARCHAR(100),
                selfLink VARCHAR(100) NOT NULL,
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
                authorId INT REFERENCES author(authorId) ON DELETE CASCADE,
                bookId INT REFERENCES book(bookId) ON DELETE CASCADE            
            );
                
        CREATE TABLE IF NOT EXISTS category (
                categoryId SERIAL PRIMARY KEY,
                name TEXT NOT NULL UNIQUE     
            );
                
        CREATE TABLE IF NOT EXISTS book_category (
                book_categoryId SERIAL PRIMARY KEY,     
                bookId INT REFERENCES book(bookId) ON DELETE CASCADE,
                categoryId INT REFERENCES category(categoryId) ON DELETE CASCADE
            );
    ''')
    conn.commit()

def insertData(data=[]):
    conn = connectDB()
    cursor = conn.cursor()     
    
    cursor.execute('''
        


    ''')


    
