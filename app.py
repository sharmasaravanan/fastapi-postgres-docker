import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2  #pymysql
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Get database connection parameters from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "testdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=RealDictCursor
    )

# Initialize database table on startup
@app.on_event("startup")
def startup():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

class ItemCreate(BaseModel):
    name: str
    description: str  = None

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with PostgreSQL and Docker Volumes!"}

@app.post("/items/")
def create_item(item: ItemCreate):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id, name, description;",
        (item.name, item.description)
    )
    new_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Item created successfully!", "item": new_item}

@app.get("/items/")
def get_items():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM items;")
    items = cur.fetchall()
    cur.close()
    conn.close()
    return {"items": items}