import json, os, requests
from datetime import datetime

token = os.environ['BOT_TOKEN']

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
            if 'message' in update:
                msg = update['message']
            elif 'channel_post' in update:
                msg = update['channel_post']
            
            if msg and 'text' in msg:
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

# main
print("📥 Проверяю посты...")
new, total = save_posts()
print(f"✅ Всего: {total}, 🆕 Новых: {new}")