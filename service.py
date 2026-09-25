from connection import connection


async def get_user(telegram_id):
    conn = None

    try:
        conn = await connection()

        user = await conn.fetchrow("""
            SELECT *
            FROM users
            WHERE telegram_id = $1
        """, str(telegram_id))

        return user

    except Exception as error:
        print(f"Error in get user: {error}")
        return None

    finally:
        if conn:
            await conn.close()


async def save_user(telegram_id, username, firstname, lastname):
    conn = None

    try:
        conn = await connection()

        full_name = f"{firstname} {lastname or ''}".strip()

        await conn.execute("""
            INSERT INTO users(telegram_id, username, full_name)
            VALUES ($1, $2, $3)
        """, str(telegram_id), username, full_name)

        print("User saved")

    except Exception as error:
        print(f"Error in save users: {error}")

    finally:
        if conn:
            await conn.close()


async def show_users():
    conn = None
    
    try:
        conn = await connection()

        users = await conn.fetch("""
            SELECT telegram_id, username, full_name
            FROM users
        """)

        return users

    except Exception as error:
        print(f"Error in get users: {error}")
        return []

    finally:
        if conn:
            await conn.close()

async def save_task(telegram_id, task_text):
    conn = None

    try:
        conn = await connection()

        await conn.execute("""
            INSERT INTO tasks(telegram_id, task_text)
            VALUES ($1, $2)
        """, str(telegram_id), task_text)

        return True

    except Exception as error:
        print(f"Error in save task: {error}")
        return False

    finally:
        if conn:
            await conn.close()

async def show_tasks(telegram_id):
    conn = None

    try:
        conn = await connection()
        tasks = await conn.fetch("""
            SELECT * FROM tasks WHERE telegram_id = $1
        """, str(telegram_id))
        return tasks

    except Exception as error:
        print(f"Error in get tasks: {error}")
        return []

    finally:
        if conn:
            await conn.close()
