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

def init_db(self):
        # DBがなければ新規作成し、テーブルを初期化する
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS weather_forecasts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    area_code TEXT NOT NULL,
                    area_name TEXT NOT NULL,
                    forecast_date DATE NOT NULL,
                    weather_code TEXT NOT NULL,
                    temp_min INTEGER,
                    temp_max INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(area_code, forecast_date)
                )
            """)

    