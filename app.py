import os, time, asyncio, requests
from dotenv import load_dotenv

load_dotenv('config.env')

# Параметры узлов
NOTION_TOKEN = "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"
DB_KUB = "75e40059cd1d48d3bd474663fac48f5a"
GOOGLE_URL = "https://script.google.com/macros/s/AKfycbz6tHTaMcC7DdTenttcl7iAuexrHeCKLsA3UASlAIK7Tqqibf5f9ycLtDzDP9bYbeZN/exec"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

async def kub_sync_loop():
    """Синхронизация Google Диск -> Notion (КУБ v1)"""
    while True:
        try:
            print(f"🔄 КУБ: Синхронизация меридианов...")
            res = requests.post(GOOGLE_URL, json={'action': 'read'}, timeout=15).json()
            records = res.get('records', [])
            
            for r in records:
                rid = str(r.get('id', ''))
                if not rid or rid == 'None': continue
                
                # Проверка дублей
                check = requests.post(f"https://api.notion.com/v1/databases/{DB_KUB}/query", 
                                     headers=HEADERS, json={"filter": {"property": "Джерело", "rich_text": {"equals": rid}}}).json()
                
                if not check.get('results'):
                    payload = {
                        "parent": {"database_id": DB_KUB},
                        "properties": {
                            "Суть": {"title": [{"text": {"content": str(r.get('thesis', 'Излучение'))}}]},
                            "Джерело": {"rich_text": [{"text": {"content": rid}}]},
                            "Актор": {"rich_text": [{"text": {"content": str(r.get('initiator', 'Andrew'))}}]}
                        }
                    }
                    requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
                    print(f"✅ КУБ: Тезис {rid} материализован.")
        except Exception as e:
            print(f"⚠️ КУБ Ожидание: {e}")
        await asyncio.sleep(60)

async def main():
    print("🚀 Metatron-8: Контур Оболочки Свет активирован.")
    # Здесь можно добавить задачи из твоих патчей (WordPress, Дайджесты)
    await asyncio.gather(
        kub_sync_loop()
    )

if __name__ == "__main__":
    asyncio.run(main())
