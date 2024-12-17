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

def save_forecast(self, area_code: str, area_name: str, forecast_date: str,
                     weather_code: str, temp_min: int, temp_max: int):
        # 予報データをDBに保存。既存のデータがあれば上書きする
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO weather_forecasts
                (area_code, area_name, forecast_date, weather_code, temp_min, temp_max)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (area_code, area_name, forecast_date, weather_code, temp_min, temp_max))

def get_forecast_history(self, area_code: str = None, start_date: str = None, end_date: str = None):
        # 過去の予報データを指定された条件で取得する
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT * FROM weather_forecasts WHERE 1=1"
            params = []

            if area_code:
                query += " AND area_code = ?"
                params.append(area_code)
            if start_date:
                query += " AND forecast_date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND forecast_date <= ?"
                params.append(end_date)

            query += " ORDER BY forecast_date DESC"
            return conn.execute(query, params).fetchall()