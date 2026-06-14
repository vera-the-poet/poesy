import json, os, requests
from datetime import datetime, timezone

token = os.environ['BOT_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']
GITHUB_TOKEN = os.environ.get('GH_TOKEN', '')

def load_posts():
    try:
        with open('posts.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_posts(posts):
    with open('posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

def process_updates():
    posts = load_posts()
    posts_dict = {(p['chat_id'], p['message_id']): p for p in posts}

    new_posts = 0
    updated_posts = 0

    url = f"https://api.telegram.org/bot{token}/getUpdates"
    r = requests.get(url)
    data = r.json()

    if not data['ok']:
        print("❌ Ошибка получения обновлений")
        return posts, False

    for update in data['result']:
        msg = None
        if 'channel_post' in update:
            msg = update['channel_post']
        if not msg or 'text' not in msg:
            continue
        if str(msg['chat']['id']) != CHANNEL_ID:
            continue

        key = (msg['chat']['id'], msg['message_id'])
        text = msg['text']
        date = datetime.fromtimestamp(msg['date'], tz=timezone.utc).isoformat()

        if key in posts_dict:
            existing = posts_dict[key]
            if existing['text'] != text:
                existing['text'] = text
                updated_posts += 1
                print(f"🔄 Обновлён пост {msg['message_id']}")
        else:
            posts.append({
                'message_id': msg['message_id'],
                'chat_id': msg['chat']['id'],
                'text': text,
                'date': date
            })
            posts_dict[key] = posts[-1]
            new_posts += 1
            print(f"➕ Новый пост {msg['message_id']}")

    print(f"✅ Новых: {new_posts}, обновлено: {updated_posts}")
    changed = (new_posts > 0) or (updated_posts > 0)
    return posts, changed

def trigger_deploy():
    if not GITHUB_TOKEN:
        return
    url = f"https://api.github.com/repos/vera-the-poet/poesy/pages/builds"
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

if __name__ == '__main__':
    print("📥 Проверяю посты из канала...")
    posts, changed = process_updates()
    save_posts(posts)
    if changed:
        trigger_deploy()
    else:
        print("💤 Нет изменений")