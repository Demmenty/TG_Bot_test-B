import json
from logging import getLogger
import aiosqlite

from app.bot.accessor import DatabaseAccessor as BaseAccessor
from .config import Config
from .dataclasses import Poll


class DatabaseAccessor(BaseAccessor):
    """управление опросами в базе данных"""

    def __init__(self, config: Config):
        self.logger = getLogger("PollsDBAccessor")
        self.dbname: str = config.db.name

    async def create_tables(self):
        """создание файла и таблиц бд, если нет"""

        async with aiosqlite.connect(self.dbname) as db:
            await db.execute(
                """CREATE TABLE IF NOT EXISTS poll 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                options TEXT NOT NULL,
                anonymous BOOLEAN NOT NULL CHECK (anonymous IN (0, 1)),
                multiple BOOLEAN NOT NULL CHECK (multiple IN (0, 1)),
                UNIQUE(question) ON CONFLICT REPLACE);"""
            )
            await db.commit()

    async def save_poll(self, poll: Poll) -> None:
        """сохраняет новый опрос в базе"""

        async with aiosqlite.connect(self.dbname) as db:
            options = json.loads(json.dumps(poll.options))

            query = f"""INSERT INTO poll (question, options, anonymous, multiple) 
                VALUES ("{poll.question}", "{options}",
                "{int(poll.is_anonymous)}", "{int(poll.multiple_answers)}")"""

            await db.execute(query)
            await db.commit()

    async def get_poll_by_question(self, question: str) -> Poll | None:
        """возвращает опрос из базы по его вопросу"""

        async with aiosqlite.connect(self.dbname) as db:
            query = f"""SELECT question, options, anonymous, 
                multiple FROM poll WHERE question="{question}" LIMIT 1;"""
            cursor = await db.execute(query)
            data = await cursor.fetchone()

        if not data:
            return

        poll = Poll(
            question=data[0],
            options=[option.strip("[']") for option in data[1].split("', '")],
            is_anonymous=bool(data[2]),
            multiple_answers=bool(data[3]),
        )

        return poll

    async def is_poll_exist(self, poll: Poll) -> bool:
        """предикат существования опроса в базе (по вопросу)"""

        async with aiosqlite.connect(self.dbname) as db:
            query = f"""SELECT EXISTS(
                SELECT 1 FROM poll WHERE question="{poll.question}" LIMIT 1);"""

            cursor = await db.execute(query)
            data = await cursor.fetchone()

        result = bool(data[0])
        return result

    async def get_polls(self) -> list[Poll]:
        """возвращает список всех опросов из базы"""

        async with aiosqlite.connect(self.dbname) as db:
            query = f"SELECT question, options, anonymous, multiple FROM poll;"
            cursor = await db.execute(query)
            data = await cursor.fetchall()

        result = []

        for poll in data:
            result.append(
                Poll(
                    question=poll[0],
                    options=[
                        option.strip("[']") for option in poll[1].split("', '")
                    ],
                    is_anonymous=bool(poll[2]),
                    multiple_answers=bool(poll[3]),
                )
            )

        return result

    async def delete_poll(self, question: str) -> None:
        """удаляет опрос из базы"""

        async with aiosqlite.connect(self.dbname) as db:
            query = f'DELETE FROM poll WHERE question="{question}";'

            await db.execute(query)
            await db.commit()
