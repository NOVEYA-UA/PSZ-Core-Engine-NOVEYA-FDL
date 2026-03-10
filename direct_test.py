import requests

HEADERS = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def direct_test():
    print("🚀 Инициация прямого проброса в Notion...")
    payload = {
        "parent": {"database_id": "75e40059cd1d48d3bd474663fac48f5a"},
        "properties": {
            "Суть": {"title": [{"text": {"content": "Тестовый Тезис: Прямая Материализация"}}]},
            "Джерело": {"rich_text": [{"text": {"content": "TEST-999"}}]},
            "Актор": {"rich_text": [{"text": {"content": "Metatron_Direct"}}]}
        }
    }
    res = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
    
    if res.status_code == 200:
        print("✅ ПОБЕДА! Запись появилась в Notion.")
    else:
        print(f"❌ КОНФЛИКТ: {res.text}")

if __name__ == '__main__':
    direct_test()