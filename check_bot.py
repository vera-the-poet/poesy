import json, os, requests
from datetime import datetime

token = os.environ['BOT_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']
GITHUB_TOKEN = os.environ.get('GH_TOKEN', '')

def save_posts():
    try:
        with open('posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
    except:
        posts = []

    url = f"https://api.telegram.org/bot{token}/getUpdates"
    r = requests.get(url)
    data = r.json()

    existing_keys = {(p['message_id'], p['chat_id']) for p in posts}
    new_posts = 0

    if data['ok']:
        for update in data['result']:
            msg = None
            if 'channel_post' in update:
                msg = update['channel_post']
            elif 'message' in update:
                msg = update['message']
            
            if msg and 'text' in msg and str(msg['chat']['id']) == CHANNEL_ID:
                key = (msg['message_id'], msg['chat']['id'])
                if key not in existing_keys:
                    posts.append({
                        'message_id': msg['message_id'],
                        'chat_id': msg['chat']['id'],
                        'text': msg['text'],
                        'date': datetime.fromtimestamp(msg['date']).isoformat()
                    })
                    existing_keys.add(key)
                    new_posts += 1

    with open('posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    
    return new_posts, len(posts)

def trigger_deploy():
    if not GITHUB_TOKEN:
        return
    url = "https://api.github.com/repos/vera-the-poet/poesy/pages/builds"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    try:
        r = requests.post(url, headers=headers)
        if r.status_code == 201:
            print("🚀 Деплой запущен")
        else:
            print(f"⚠️ Ошибка деплоя: {r.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

# main
print("📥 Проверяю посты из канала...")
new, total = save_posts()
print(f"✅ Всего: {total}, 🆕 Новых: {new}")

if new > 0:
    trigger_deploy()
else:
    print("💤 Нет новых постов")