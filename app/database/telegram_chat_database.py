import json
import asyncpg
from datetime import datetime

from app.database.constants import connection_string_async
from app.models.tg_chat_model import TgChatModel


class ChatDatabase:
    def __init__(self):
        self.connection_string = connection_string_async

    async def init_table(self):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS guju_chats (
                id SERIAL PRIMARY KEY,
                title TEXT,
                chat_id BIGINT UNIQUE,
                joined_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                language TEXT,
                badwords TEXT,
                actions TEXT,
                data JSONB
            );
            '''
            await conn.execute(create_table_query)
            print("Table 'guju_chats' initialized successfully")
        except Exception as error:
            print(f"Error while initializing table: {error}")
        finally:
            if conn:
                await conn.close()

    async def create_chat(self, chat: TgChatModel):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            insert_query = '''
            INSERT INTO guju_chats (title, chat_id, joined_time, language, badwords, actions, data)
            VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING id
            '''
            chat_id = await conn.fetchval(insert_query, chat.title, chat.chat_id, datetime.now(),
                                          chat.language, chat.badwords, chat.actions, json.dumps(chat.data))
            print("Chat created successfully with id:", chat_id)
            return chat_id
        except Exception as error:
            print(f"Error while creating chat: {error}")
            return None
        finally:
            if conn:
                await conn.close()

    async def get_chat_by_id(self, chat_id):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            select_query = "SELECT * FROM guju_chats WHERE chat_id = $1"
            chat_data = await conn.fetchrow(select_query, chat_id)

            if chat_data:
                return TgChatModel(
                    chat_id=chat_data["chat_id"],
                    title=chat_data["title"],
                    joined_time=str(chat_data["joined_time"]),
                    language=chat_data["language"],
                    badwords=chat_data["badwords"],
                    actions=chat_data["actions"],
                    data=eval(chat_data["data"]) if chat_data["data"] else {}
                )
            else:
                return None
        except Exception as error:
            print(f"Error while fetching chat by chat_id: {error}")
            return None
        finally:
            if conn:
                await conn.close()

    async def get_all_chats(self, page: int, page_size: int):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            query = "SELECT * FROM guju_chats ORDER BY joined_time DESC LIMIT $1 OFFSET $2"
            chats_data = await conn.fetch(query, page_size, (page - 1) * page_size)
            return [TgChatModel(*chat) for chat in chats_data]
        except Exception as error:
            print(f"Error while fetching chats: {error}")
            return []
        finally:
            if conn:
                await conn.close()

    async def update_chat(self, chat: TgChatModel):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            update_query = '''
            UPDATE guju_chats
            SET title = $1, language = $2, badwords = $3, actions = $4, data = $5
            WHERE chat_id = $6
            '''
            await conn.execute(update_query, chat.title, chat.language, chat.badwords, chat.actions, json.dumps(chat.data), chat.chat_id)
            print("Chat updated successfully")
        except Exception as error:
            print(f"Error while updating chat: {error}")
        finally:
            if conn:
                await conn.close()

    async def delete_chat(self, chat_id):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            delete_query = "DELETE FROM guju_chats WHERE chat_id = $1"
            await conn.execute(delete_query, chat_id)
            print("Chat deleted successfully")
        except Exception as error:
            print(f"Error while deleting chat: {error}")
        finally:
            if conn:
                await conn.close()
