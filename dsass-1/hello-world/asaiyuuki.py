import flet as ft
import json
import os

# 正しいファイル名 'region.json' を指定
json_path = os.path.join(os.path.dirname(__file__), 'region.json')

# JSON ファイルを読み込む
try:
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    raise FileNotFoundError(f"JSON ファイル '{json_path}' が見つかりません。")

def main(page: ft.Page):
    page.title = "地域選択と情報表示"
    page.theme_mode = "light"

    # 選択情報を表示するテキスト
    selected_item = ft.Text("No item selected", size=20)
    selected_index = None  # 選択されたアイテムのインデックス

    # リストアイテムを作成する関数
    def create_list_tile(center, index):
        is_selected = selected_index == index  # 現在のアイテムが選択されているか確認

        return ft.ListTile(
            leading=ft.Icon(
                ft.icons.LOCATION_ON,
                color=ft.colors.RED if is_selected else ft.colors.BLACK
            ),
            title=ft.Text(
                center['name'],
                weight=ft.FontWeight.BOLD if is_selected else ft.FontWeight.NORMAL
            ),
            subtitle=ft.Text(center.get('enName', '')),
            on_click=lambda e: update_selected(index, center['name'])
        )

    # 選択状態を更新する関数
    def update_selected(index, name):
        nonlocal selected_index
        selected_index = index
        selected_item.value = f"Selected: {name}"  # 選択されたアイテム名を表示
        page.update()  # ページを更新して状態を反映

    # リストアイテムを作成
    list_items = []
    for category in ['centers', 'offices', 'class10s', 'class15s', 'class20s']:
        for index, (key, center) in enumerate(data.get(category, {}).items()):
            list_items.append(create_list_tile(center, index))

    # スクロール可能なListViewを作成
    list_view = ft.ListView(
        controls=list_items,
        expand=True
    )

    # ページにリストと選択情報を追加
    page.add(
        ft.Row(
            [
                list_view,
                ft.VerticalDivider(width=1),
                ft.Column([selected_item], alignment=ft.MainAxisAlignment.START, expand=True),
            ],
            expand=True,
        )
    )

ft.app(main)