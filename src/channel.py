import json
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.getenv("API_KEY_YOUTUBE")


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self._channel_id = channel_id
        self._youtube = build('youtube', 'v3', developerKey=API_KEY)
        self._channel_info = self._youtube.channels().list(id=self._channel_id, part='snippet,statistics').execute()

    @staticmethod
    def _print_json(data: dict) -> None:
        return json.dumps(data, indent=2, ensure_ascii=False)

    @property
    def channel_id(self):
        return self._channel_id

    @property
    def url(self):
        return f"https://www.youtube.com/{self._channel_info['items'][0]['snippet']['customUrl']}"

    @property
    def description(self):
        return self._channel_info['items'][0]['snippet']['description']

    @property
    def title(self):
        return self._channel_info['items'][0]['snippet']['title']

    @property
    def video_count(self):
        return self._channel_info['items'][0]['statistics']['videoCount']

    @property
    def subscriber_count(self):
        return self._channel_info['items'][0]['statistics']['subscriberCount']

    @property
    def view_count(self):
        return self._channel_info['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self._channel_info
        return Channel._print_json(channel)

    def get_service(self):
        return self._youtube

    def to_json(self):
        data = self._channel_info
        with open("moscowpython.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
