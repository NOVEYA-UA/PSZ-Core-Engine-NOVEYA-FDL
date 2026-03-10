import os, time, requests

URL = 'https://script.google.com/macros/s/AKfycbz6tHTaMcC7DdTenttcl7iAuexrHeCKLsA3UASlAIK7Tqqibf5f9ycLtDzDP9bYbeZN/exec'
TOKEN = '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'
DB_ID = '75e40059cd1d48d3bd474663fac48f5a'

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def run_sync():
    print(f"\n--- [Цикл инициации: {time.strftime('%H:%M:%S')}] ---")
    try:
        # 1. Запрос к Google
        print("📡 Запрос к Google КУБ v1...")
        res = requests.post(URL, json={'action': 'read'}, timeout=15)
        
        if res.status_code != 200:
            print(f"❌ Ошибка шлюза Google: {res.status_code}")
            return

        data = res.json()
        records = data.get('records', [])
        print(f"📊 Получено из Google: {len(records)} записей.")

        for r in records:
            # Приводим ключи к одному регистру (удаляем шум)
            clean_r = {str(k).lower(): v for k, v in r.items()}
            rec_id = str(clean_r.get('id', ''))
            thesis = clean_r.get('thesis', 'Без названия')
            actor = clean_r.get('initiator', 'Система')

            if not rec_id or rec_id == 'None': continue

            # 2. Проверка в Notion
            query_payload = {"filter": {"property": "Джерело", "rich_text": {"equals": rec_id}}}
            check = requests.post(f"https://api.notion.com/v1/databases/{DB_ID}/query", headers=HEADERS, json=query_payload)
            
            if check.status_code == 200:
                if not check.json().get("results"):
                    print(f"✨ Материализация: {rec_id} -> {thesis[:30]}...")
                    payload = {
                        "parent": {"database_id": DB_ID},
                        "properties": {
                            "Суть": {"title": [{"text": {"content": str(thesis)}}]},
                            "Джерело": {"rich_text": [{"text": {"content": rec_id}}]},
                            "Актор": {"rich_text": [{"text": {"content": str(actor)}}]}
                        }
                    }
                    create = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
                    if create.status_code == 200:
                        print(f"  ✅ Успешно зафиксировано в Соборе.")
                    else:
                        print(f"  ❌ Ошибка Notion: {create.text[:100]}")
                else:
                    print(f"💤 ID {rec_id} уже в базе.")
            else:
                print(f"⚠️ Ошибка проверки Notion: {check.status_code}")

    except Exception as e:
        print(f"❌ КРИТИЧЕСКИЙ ШУМ: {e}")

if __name__ == "__main__":
    print("🚀 Metatron-8: Агент-Аналитик запущен в режиме мониторинга.")
    while True:
        run_sync()
        print("\n⏳ Ожидание следующего цикла (60 сек)... Ctrl+C для остановки.")
        time.sleep(60)