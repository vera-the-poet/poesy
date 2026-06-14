import os, requests

token = os.environ['BOT_TOKEN']

url = f"https://api.telegram.org/bot{token}/getUpdates"
r = requests.get(url)
data = r.json()

if data['ok'] and data['result']:
    last_id = data['result'][-1]['update_id']
    print(f"Последний update_id: {last_id}")
    
    clear_url = f"https://api.telegram.org/bot{token}/getUpdates?offset={last_id + 1}"
    requests.get(clear_url)
    print("✅ Кеш бота очищен")
else:
    print("Нет обновлений для очистки")