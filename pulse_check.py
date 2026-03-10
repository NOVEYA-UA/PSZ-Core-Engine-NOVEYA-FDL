import os
import requests
import sys
sys.path.append(os.path.join(os.getcwd(), 'modules', 'psz_engine', 'logic', 'Algorithms'))
try:
    from PSZ_Legal_Vector import LegalVector
    print('✅ СИСТЕМА: Логика Σ-FDL подтянута.')
except Exception as e:
    print(f'❌ ОШИБКА ИМПОРТА: {e}')

gateway_url = 'https://script.google.com/macros/s/AKfycbwzTHFgbGRVIQIkXgp0D5PoqYh_zytH_mhazvmJTGrgARwZ_xH9jYE3Dej7Ph2Rex6D/exec'
print(f'📡 СЕНСОР: Стучимся в Шлюз Google...')
try:
    response = requests.post(gateway_url, json={'test': 'ping'}, timeout=10)
    print(f'✅ СЕНСОР: Ответ получен! Код: {response.status_code}')
    if response.status_code == 200:
        print('🚀 МЕТАТРОН-8: ПЕРВЫЙ ВЗДОХ СДЕЛАН.')
except Exception as e:
    print(f'❌ СЕНСОР: Ошибка: {e}')