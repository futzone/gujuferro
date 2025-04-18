import asyncpg
from datetime import datetime
from app.database.constants import connection_string_async
from app.models.tg_user_model import TgUserModel


class UserDB:
    def __init__(self):
        self.connection_string = connection_string_async

    async def init_table(self):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS guju_users (
                telegram_id BIGINT PRIMARY KEY,
                user_id BIGINT,
                fullname TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                state TEXT,
                chat_id BIGINT,
                status TEXT,
                language TEXT
            );
            '''
            await conn.execute(create_table_query)
            print("Table 'guju_users' initialized successfully")
        except Exception as error:
            print(f"Error while initializing table: {error}")
        finally:
            if conn:
                await conn.close()

    async def create_user(self, user: TgUserModel):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            insert_query = '''
            INSERT INTO guju_users (telegram_id, user_id, fullname, created_date, state, chat_id, status, language)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING telegram_id
            '''
            user_id = await conn.fetchval(insert_query, user.telegram_id, user.user_id, user.fullname, datetime.now(),
                                          user.state, user.chat_id, user.status, user.language)
            print("Telegram user created successfully with id:", user_id)
            return user_id
        except Exception as error:
            print(f"Error while creating telegram user: {error}")
            return None
        finally:
            if conn:
                await conn.close()

    async def get_by_telegram_id(self, telegram_id):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            select_query = "SELECT * FROM guju_users WHERE telegram_id = $1"
            user_data = await conn.fetchrow(select_query, telegram_id)
            if user_data:
                return TgUserModel(*user_data)
            else:
                return None
        except Exception as error:
            print(f"Error while fetching telegram user by telegram_id: {error}")
            return None
        finally:
            if conn:
                await conn.close()

    async def get_by_user_id(self, user_id):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            select_query = "SELECT * FROM guju_users WHERE user_id = $1"
            user_data = await conn.fetchrow(select_query, user_id)
            if user_data:
                return TgUserModel(*user_data)
            else:
                return None
        except Exception as error:
            print(f"Error while fetching telegram user by user_id: {error}")
            return None
        finally:
            if conn:
                await conn.close()

    async def get_by_chat_id(self, chat_id):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            select_query = "SELECT * FROM guju_users WHERE chat_id = $1"
            user_data = await conn.fetchrow(select_query, chat_id)
            if user_data:
                return TgUserModel(*user_data)
            else:
                return None
        except Exception as error:
            print(f"Error while fetching telegram user by chat_id: {error}")
            return None
        finally:
            if conn:
                await conn.close()

    async def get_language(self, telegram_id):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            select_query = "SELECT language FROM guju_users WHERE telegram_id = $1"
            language = await conn.fetchval(select_query, telegram_id)
            if language:
                return language
            else:
                return None
        except Exception as error:
            print(f"Error while fetching language by telegram_id: {error}")
            return None
        finally:
            if conn:
                await conn.close()

    async def change_language(self, telegram_id, language):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            update_query = '''
            UPDATE guju_users
            SET language = $1
            WHERE telegram_id = $2
            '''
            await conn.execute(update_query, language, telegram_id)
            print(f"Language updated successfully to {language}")
        except Exception as error:
            print(f"Error while updating language: {error}")
        finally:
            if conn:
                await conn.close()

    async def update_user(self, user):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            update_query = '''
            UPDATE guju_users
            SET user_id = $1, fullname = $2, state = $3, chat_id = $4, status = $5, language = $6
            WHERE telegram_id = $7
            '''
            await conn.execute(update_query, user.user_id, user.fullname, user.state, user.chat_id, user.status, user.language, user.telegram_id)
            print("Telegram user updated successfully")
        except Exception as error:
            print(f"Error while updating telegram user: {error}")
        finally:
            if conn:
                await conn.close()

    async def update_state(self, telegram_id, state):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            update_query = '''
            UPDATE guju_users
            SET state = $1
            WHERE telegram_id = $2
            '''
            await conn.execute(update_query, state, telegram_id)
            print("State updated successfully")
        except Exception as error:
            print(f"Error while updating state: {error}")
        finally:
            if conn:
                await conn.close()

    async def update_status(self, telegram_id, status):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            update_query = '''
            UPDATE guju_users
            SET status = $1
            WHERE telegram_id = $2
            '''
            await conn.execute(update_query, status, telegram_id)
            print("Status updated successfully")
        except Exception as error:
            print(f"Error while updating status: {error}")
        finally:
            if conn:
                await conn.close()

    async def delete_user(self, telegram_id):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            delete_query = "DELETE FROM guju_users WHERE telegram_id = $1"
            await conn.execute(delete_query, telegram_id)
            print("Telegram user deleted successfully")
        except Exception as error:
            print(f"Error while deleting telegram user: {error}")
        finally:
            if conn:
                await conn.close()

    async def get_users(self, page: int, page_size: int):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            query = "SELECT * FROM guju_users ORDER BY created_date DESC LIMIT $1 OFFSET $2"
            users_data = await conn.fetch(query, page_size, (page - 1) * page_size)
            return [TgUserModel(*user) for user in users_data]
        except Exception as error:
            print(f"Error while fetching users: {error}")
            return []
        finally:
            if conn:
                await conn.close()
