import flet as ft
import requests
import sqlite3
from datetime import datetime
from typing import Dict

# 地域コードをキーにして地域名を取得できるようにする
area_cache: Dict[str, Dict] = {}

class WeatherDB:
    def __init__(self, db_path="weather.db"):
        # DBファイルのパスを指定
        self.db_path = db_path
        self.init_db()