import json
import os
import datetime
import isodate

import requests
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.environ.get('API_KEY_YOUTUBE')

def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

class PlayList:
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    def __init__(self, playlist_id):
        self._playlist_id = playlist_id
        self.title = self.youtube.playlists().list(part='snippet', id=self._playlist_id).execute()['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self._playlist_id}"
        self._videos_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                           id=','.join(
                                                               [video['contentDetails']['videoId'] for video in self.youtube.playlistItems().list(
                                                                   playlistId=self._playlist_id,
                                                                   part='snippet, contentDetails'
                                                               ).execute()['items']]
                                                                       )
                                                           ).execute()

    @property
    def total_duration(self):
        total_duration = datetime.timedelta()
        for video in self._videos_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            total_duration += isodate.parse_duration(iso_8601_duration)
        return total_duration

    def show_best_video(self):
        best_video = ''
        likes_max = 0
        for video in self._videos_response['items']:
            if int(video['statistics']['likeCount']) >= likes_max:
                best_video = video['id']
                likes_max = int(video['statistics']['likeCount'])
        return f"https://youtu.be/{best_video}"
