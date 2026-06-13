import json, os, requests
from datetime import datetime

token = os.environ['BOT_TOKEN']
GITHUB_TOKEN = os.environ['GH_TOKEN']

def save_posts():
    try:
        with open('posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
    except:
        posts = []

    url = f"https://api.telegram.org/bot{token}/getUpdates"
    r = requests.get(url)
    data = r.json()

    existing_ids = {p['id'] for p in posts}
    new_posts = 0

    if data['ok']:
        for update in data['result']:
            if 'message' in update:
                msg = update['message']
                if 'text' in msg and 'forward_from_chat' in msg:
                    if msg['message_id'] not in existing_ids:
                        posts.append({
                            'id': msg['message_id'],
                            'text': msg['text'],
                            'date': datetime.fromtimestamp(msg['date']).isoformat()
                        })
                        new_posts += 1

    with open('posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    
    return new_posts, len(posts)

def trigger_deploy():
    url = "https://api.github.com/repos/vera-the-poet/poesy/pages/builds"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    try:
        r = requests.post(url, headers=headers)
        if r.status_code == 201:
            print("🚀 Деплой сайта запущен")
        else:
            print(f"⚠️ Ошибка деплоя: {r.status_code} {r.json()}")
    except Exception as e:
        print(f"❌ Не удалось запустить деплой: {e}")

# main
print("📥 Проверяю посты...")
new, total = save_posts()
print(f"✅ Всего: {total}, 🆕 Новых: {new}")

if new > 0:
    print("🔄 Запускаю обновление сайта...")
    trigger_deploy()
else:
    print("Нет нового контента")