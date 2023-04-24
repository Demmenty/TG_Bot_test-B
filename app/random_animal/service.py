from logging import getLogger
from typing import Optional
import openai
from aiohttp import TCPConnector
from aiohttp.client import ClientSession

from .config import Config
from .dataclasses import AnimalRequest


class RandomAnimalService:
    """сервис получения случайных картинок животных"""

    def __init__(self):
        self.logger = getLogger("RandomAnimalService")
        self.session: Optional[ClientSession] = None

    async def connect(self, config: Config):
        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))
        self.cat_api_key = config.thecatapi.api_key
        openai.api_key = config.openai.api_key

    def prepare_request(self, msg_text: str) -> AnimalRequest:
        """подготавливает текст сообщения с командой к обработке"""

        msg_text_lst = [word.strip(" ,.!?;:") for word in msg_text.split(" ")]

        request = AnimalRequest(
            type="".join(msg_text_lst[1:2]),
        )
        return request

    async def paint_pic(self) -> str | None:
        """вовзращает ссылку на картинку животных от нейросети DALLE"""

        try:
            response = await openai.Image.acreate(
                prompt="high-quality high-detailed beautiful picture with cute animal",
                n=1,
                size="512x512",
                response_format="url",
            )

            pic_url = response.data[0].url

            return pic_url

        except Exception:
            return None

    async def get_cat(self) -> str | None:
        """возвращает ссылку на фото случайной кошки от сторонних API"""

        url1 = "https://cataas.com/cat?json=true"
        url2 = f"https://api.thecatapi.com/v1/images/search?api_key={self.cat_api_key}"
        pic_url = None

        try:
            async with self.session.get(url1) as response:
                data = await response.json()
                pic_url = "https://cataas.com" + data["url"]

        except Exception:
            async with self.session.get(url2) as response:
                data = await response.json()
                pic_url = data[0]["url"]

        finally:
            return pic_url

    async def get_bigcat(self) -> str | None:
        """возвращает ссылку на фото случайной большой кошки от публичного API"""

        url = "https://randombig.cat/roar.json"

        try:
            async with self.session.get(url) as response:
                data = await response.json()
                pic_url = data.get("url")

            return pic_url

        except Exception:
            return None

    async def get_dog(self) -> str | None:
        """возвращает ссылку на фото случайной собаки от публичного API"""

        url = "https://random.dog/woof.json"

        try:
            async with self.session.get(url) as response:
                data = await response.json()
                pic_url = data.get("url")

            return pic_url

        except Exception:
            return None

    async def get_fox(self) -> str | None:
        """возвращает ссылку на фото случайной лисы от публичного API"""

        url = "https://randomfox.ca/floof/"

        try:
            async with self.session.get(url) as response:
                data = await response.json()
                pic_url = data.get("image")

            return pic_url

        except Exception:
            return None
