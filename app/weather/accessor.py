import aiosqlite
from logging import getLogger

from app.bot.accessor import DatabaseAccessor as BaseAccessor
from .config import Config
from .dataclasses import WeatherRequest


class DatabaseAccessor(BaseAccessor):
    """управление опросами в базе данных"""

    def __init__(self, config: Config):
        self.logger = getLogger("UsercityDBAccessor")
        self.dbname: str = config.db.name
    
    async def create_tables(self):
        """создание таблиц бд, если нет"""

        async with aiosqlite.connect(self.dbname) as db:
            await db.execute(
                """CREATE TABLE IF NOT EXISTS usercity 
                (user_id INTEGER PRIMARY KEY,
                query TEXT NOT NULL,
                UNIQUE(user_id) ON CONFLICT REPLACE);"""
            )
            await db.commit()
    
    async def save_usercity(self, request: WeatherRequest) -> None:
        """сохраняет в базе инфо о юзере и последнем запрошенном им городе"""

        async with aiosqlite.connect(self.dbname) as db:

            query = f"""REPLACE INTO usercity (user_id, query) 
                VALUES ("{request.user_id}", "{request.city_query}")"""

            await db.execute(query)
            await db.commit()
    
    async def get_usercity(self, request: WeatherRequest) -> WeatherRequest:
        """заполняет инфу о городе запроса информацией из бд"""

        async with aiosqlite.connect(self.dbname) as db:
            query = f"""SELECT user_id, query 
                FROM usercity WHERE user_id="{request.user_id}" LIMIT 1;"""
            cursor = await db.execute(query)
            data = await cursor.fetchone()

        if data:
            request.city_query = data[1]

        return request
