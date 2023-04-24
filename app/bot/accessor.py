from logging import getLogger
import aiosqlite

from app.bot.config import Config
from app.bot.dataclasses import Chat


# базовый аксессор
# регистрация чатов нужна для отправки опросов
class DatabaseAccessor:
    """осуществление доступа к базе данных"""

    def __init__(self, config: Config):
        self.logger = getLogger("MainDBAccessor")
        self.dbname: str = config.db.name

    async def create_tables(self):
        """создание файла и таблиц бд, если нет"""

        async with aiosqlite.connect(self.dbname) as db:
            await db.execute(
                """CREATE TABLE IF NOT EXISTS chat 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                UNIQUE(tg_id) ON CONFLICT REPLACE);"""
            )
            await db.commit()

    async def add_chat(self, chat: Chat) -> None:
        """сохраняет новый чат в базе"""

        async with aiosqlite.connect(self.dbname) as db:
            query = f"""INSERT INTO chat (tg_id, title) 
                VALUES ("{chat.tg_id}", "{chat.title}")"""

            await db.execute(query)
            await db.commit()

    async def delete_chat(self, chat: Chat) -> None:
        """удаляет чат из базы"""

        async with aiosqlite.connect(self.dbname) as db:
            query = f'DELETE FROM chat WHERE chat.id="{chat.id}";'
            await db.execute(query)
            await db.commit()

    async def is_chat_exist(self, chat: Chat) -> bool:
        """предикат существования чата в базе"""

        async with aiosqlite.connect(self.dbname) as db:
            query = f'SELECT EXISTS(SELECT 1 FROM chat WHERE tg_id="{chat.tg_id}" LIMIT 1);'
            cursor = await db.execute(query)
            data = await cursor.fetchone()

        result = bool(data[0])
        return result

    async def get_chats(self) -> list[Chat]:
        """возвращает список всех чатов из базы"""

        async with aiosqlite.connect(self.dbname) as db:
            query = f"SELECT id, tg_id, title FROM chat;"
            cursor = await db.execute(query)
            data = await cursor.fetchall()

        result = []
        for chat in data:
            result.append(
                Chat(
                    id=chat[0],
                    tg_id=chat[1],
                    title=chat[2],
                )
            )

        return result
