import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
ps = os.getenv("PASSWORD_DB")


async def connection():
    try:
        conn = await asyncpg.connect(
            database="bot7_db",
            host="localhost",
            user = "postgres",
            port = 5432,
            password=ps
        )
        print("Connection OK")
        return conn
    except Exception as error:
        print(f"Connection Error: {error}")
        
async def create_table():
    conn = await connection()
    try:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(100),
            full_name VARCHAR(100),
            telegram_id VARCHAR UNIQUE,
            created_at TIMESTAMP DEFAULT NOW(),
            is_active BOOLEAN DEFAULT TRUE
    );

    CREATE TABLE IF NOT EXISTS tasks(
            task_id SERIAL PRIMARY KEY,
            telegram_id VARCHAR REFERENCES users(telegram_id),
            task_text VARCHAR NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            status BOOLEAN DEFAULT TRUE
    );
""")
    
        print("Table created!")
    except Exception as error:
        print(f"Create table Error: {error}")
    finally:
        await conn.close()