import os
import time
import requests
from notion_client import Client
from dotenv import load_dotenv

load_dotenv('config.env')

notion = Client(auth=os.getenv("NOTION_TOKEN"))
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
GATEWAY_URL = os.getenv("GOOGLE_GATEWAY_URL")

def sync_to_notion():
    print(f"\n--- [Синхронизация с Собором: {time.strftime('%H:%M:%S')}] ---")
    try:
        # 1. Запрос к Шлюзу
        response = requests.post(GATEWAY_URL, json={'action': 'read'}, timeout=15)
        
        # 2. Проверка на "Шум" (не-JSON ответ)
        try:
            data = response.json()
        except Exception:
            print("⚠️ ШУМ: Шлюз прислал неверный формат. Сырые данные:")
            print(response.text[:300]) # Показываем начало ответа
            return

        records = data.get('records', [])
        if not records:
            print("🍀 Состояние: В КУБ v1 пусто. Нечего материализовать.")
            return

        for r in records:
            record_id = str(r.get('id', ''))
            # Поиск в Notion
            query = notion.databases.query(
                database_id=DATABASE_ID,
                filter={"property": "ID", "rich_text": {"equals": record_id}}
            )

            if not query.get("results"):
                # Материализация
                notion.pages.create(
                    parent={"database_id": DATABASE_ID},
                    properties={
                        "Name": {"title": [{"text": {"content": r.get('thesis', 'Без названия')}}]},
                        "ID": {"rich_text": [{"text": {"content": record_id}}]},
                        "Antithesis": {"rich_text": [{"text": {"content": r.get('antithesis', '')}}]},
                        "Synthesis": {"rich_text": [{"text": {"content": r.get('synthesis', '')}}]},
                        "TR": {"number": float(r.get('tr', 0)) if r.get('tr') else 0}
                    }
                )
                print(f"✅ Собор: Тезис {record_id} зафиксирован.")
            else:
                print(f"💤 В базе: ID {record_id} уже есть.")

    except Exception as e:
        print(f"❌ КРИТИЧЕСКИЙ СБОЙ: {e}")

if __name__ == "__main__":
    while True:
        sync_to_notion()
        time.sleep(60)