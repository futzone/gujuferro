import psycopg2

from app.database.constants import connection_string
from app.database.telegram_chat_database import ChatDatabase
from app.database.user_database import UserDB


async def init_db():
    tg_db = UserDB()
    await tg_db.init_table()

    chat_db = ChatDatabase()
    await chat_db.init_table()


def delete_table(table_name):
    cur = None
    conn = None
    try:
        conn = psycopg2.connect(connection_string)
        cur = conn.cursor()
        drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
        cur.execute(drop_table_query)
        conn.commit()

        print(f"Table {table_name} deleted successfully.")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
