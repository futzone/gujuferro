import asyncpg
from datetime import datetime
from app.database.constants import connection_string_async
from app.models.record_model import RecordModel


class RecordDB:
    def __init__(self):
        self.connection_string = connection_string_async

    async def init_table(self):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS guju_records (
                id SERIAL PRIMARY KEY,
                chat_id BIGINT,
                user_id BIGINT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                type TEXT,
                data TEXT,
                source TEXT
            );
            '''
            await conn.execute(create_table_query)
            print("Table 'guju_records' initialized successfully")
        except Exception as error:
            print(f"Error while initializing table: {error}")
        finally:
            if conn:
                await conn.close()

    async def create_record(self, record: RecordModel):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            insert_query = '''
            INSERT INTO guju_records (chat_id, user_id, created_date, type, data, source)
            VALUES ($1, $2, $3, $4, $5, $6) RETURNING id
            '''
            record_id = await conn.fetchval(insert_query, record.chat_id, record.user_id, datetime.now(),
                                            record.type, record.data, record.source)
            print("Record created successfully with id:", record_id)
            return record_id
        except Exception as error:
            print(f"Error while creating record: {error}")
            return None
        finally:
            if conn:
                await conn.close()

    async def get_record_by_id(self, record_id):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            select_query = "SELECT * FROM guju_records WHERE id = $1"
            record_data = await conn.fetchrow(select_query, record_id)
            if record_data:
                return RecordModel(*record_data)
            else:
                return None
        except Exception as error:
            print(f"Error while fetching record by id: {error}")
            return None
        finally:
            if conn:
                await conn.close()

    async def get_user_records(self, chat_id, user_id, record_type):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            query = "SELECT * FROM guju_records WHERE chat_id = $1 AND user_id = $2 AND type = $3 ORDER BY created_date DESC"
            records_data = await conn.fetch(query, chat_id, user_id, record_type)
            return [RecordModel(*record) for record in records_data]
        except Exception as error:
            print(f"Error while fetching user records: {error}")
            return []
        finally:
            if conn:
                await conn.close()

    async def update_record(self, record: RecordModel):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            update_query = '''
            UPDATE guju_records
            SET chat_id = $1, user_id = $2, type = $3, data = $4, source = $5
            WHERE id = $6
            '''
            await conn.execute(update_query, record.chat_id, record.user_id, record.type, record.data, record.source, record.id)
            print("Record updated successfully")
        except Exception as error:
            print(f"Error while updating record: {error}")
        finally:
            if conn:
                await conn.close()

    async def delete_record(self, record_id):
        conn = None
        try:
            conn = await asyncpg.connect(self.connection_string)
            delete_query = "DELETE FROM guju_records WHERE id = $1"
            await conn.execute(delete_query, record_id)
            print("Record deleted successfully")
        except Exception as error:
            print(f"Error while deleting record: {error}")
        finally:
            if conn:
                await conn.close()
