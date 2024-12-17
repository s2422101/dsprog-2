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
        
def get_forecast_by_date(self, area_code: str, selected_date: str):
        # 特定の日付の予報データを取得する
     with sqlite3.connect(self.db_path) as conn:
         return conn.execute("""
                SELECT * FROM weather_forecasts
                WHERE area_code = ? AND date(forecast_date) = date(?)
                ORDER BY forecast_date
            """, (area_code, selected_date)).fetchall()

def main(page: ft.Page):
    # アプリケーションのページ設定
    page.title = "地域ごとの天気予報"
    page.theme_mode = "light"

    # WeatherDBインスタンスを作成
    db = WeatherDB()
    current_region_code = None

    # プログレスバーの初期設定
    progress_bar = ft.ProgressBar(visible=False)

    # エラーメッセージを表示する関数
    def show_error(message: str):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            action="閉じる",
            bgcolor=ft.colors.ERROR,
        )
        page.snack_bar.open = True

        page.update()# 地域一覧を表示するListView
    region_list_view = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
    )

    # 天気予報表示用のビュー
    forecast_view = ft.Column(
        expand=True,
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
    )

    # 過去の天気予報を表示するビュー
    history_view = ft.Column(
        visible=False,
        expand=True,
    )

    # 日付が選択されたときに過去の天気予報を表示する関数
    def on_date_selected(e):
        if e.date:
            selected_date = e.date.strftime("%Y-%m-%d")
            if current_region_code:
                show_forecast_for_date(current_region_code, selected_date)
        page.update()

    # 過去の天気予報を表示する関数
    def show_forecast_for_date(region_code: str, selected_date: str):
        # DBから過去の天気予報を取得して表示する
        history_data = db.get_forecast_by_date(region_code, selected_date)
        if history_data:
            history_view.visible = True
            history_view.controls = [
                ft.Column(
                    controls=[
                        ft.Text(f"{area_cache[region_code]['name']}の{selected_date}の予報",
                               size=20,
                               weight="bold"),
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("日付")),
                                ft.DataColumn(ft.Text("天気")),
                            ],
                            rows=[
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text(format_date(row[3]))),
                                        ft.DataCell(ft.Text(f"{get_weather_icon(row[4])} {get_weather_text(row[4])}")),
                                    ]
                                ) for row in history_data
                            ],
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,
                )
            ]
        else:
            history_view.visible = True
            history_view.controls = [
                ft.Text(f"選択された日付（{selected_date}）の予報データは見つかりませんでした。",
                       color=ft.colors.ERROR)
            ]
        page.update()

         # APIからデータを取得する関数
    def fetch_data(url: str) -> Dict:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            show_error(f"データ取得エラー: {str(e)}")
            return {}

    # 地域リストを読み込む関数
    def load_region_list():
        try:
            progress_bar.visible = True
            page.update()

            # 気象庁のAPIから地域データを取得
            data = fetch_data("http://www.jma.go.jp/bosai/common/const/area.json")
            if "offices" in data:
                area_cache.update(data["offices"])
                update_region_menu()
            else:
                show_error("地域データの形式が予期したものと異なります。")
        except Exception as e:
            show_error(f"地域データの読み込みに失敗しました: {str(e)}")
        finally:
            progress_bar.visible = False
            page.update()