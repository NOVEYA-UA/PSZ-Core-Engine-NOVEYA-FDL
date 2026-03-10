import requests

URL = 'https://script.google.com/macros/s/AKfycbzYRPTWPWC0GUUQfFv7QM5PQGBKq_cwotJBM3u2F2ZX3xHvjedkq5MYb1k5AcLA31d8/exec'

data_to_seed = [
    {"id": "TH-01", "initiator": "Andrew", "thesis": "Единство цели", "antithesis": "Рассеяние внимания", "synthesis": "Концентрация на Σ-FDL", "tr": 15},
    {"id": "TH-02", "initiator": "Andrew", "thesis": "Снятие дискретности", "antithesis": "Разрыв меридианов", "synthesis": "Биологическая нормализация", "tr": 14},
    {"id": "PRO-01", "initiator": "Metatron", "thesis": "Metatron-8 запущен", "antithesis": "Ошибки 404 и JSON", "synthesis": "Стабильный шлюз КУБ v1", "tr": 10}
]

print("⛪ Наполнение Собора тезисов...")
try:
    response = requests.post(URL, json={"action": "write", "data": data_to_seed}, timeout=15)
    print(f"✅ Результат: {response.json().get('msg')}")
except Exception as e:
    print(f"❌ ШУМ: {e}")