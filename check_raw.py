import json, os, requests

token = os.environ['BOT_TOKEN']

url = f"https://api.telegram.org/bot{token}/getUpdates"
r = requests.get(url)
data = r.json()

print("="*60)
print("📡 СЫРЫЕ ДАННЫЕ ОТ TELEGRAM API")
print("="*60)
print(f"OK: {data['ok']}")
print(f"Количество обновлений: {len(data['result'])}")

if not data['result']:
    print("\n❌ Бот не получил ни одного сообщения!")
    print("   Перешли стих из канала боту и запусти проверку снова.")
else:
    for i, update in enumerate(data['result']):
        print(f"\n{'='*60}")
        print(f"📨 Обновление #{i+1}")
        print(f"   Ключи: {list(update.keys())}")
        
        if 'message' in update:
            msg = update['message']
            print(f"   Тип: личное сообщение")
            print(f"   От кого: {msg['from']['first_name']} (@{msg['from'].get('username', 'нет')})")
            print(f"   Текст: {'✅ ДА' if 'text' in msg else '❌ НЕТ'}")
            if 'text' in msg:
                print(f"   Содержимое: {msg['text'][:200]}")
            print(f"   Переслано из канала: {'✅ ДА' if 'forward_from_chat' in msg else '❌ НЕТ'}")
            if 'forward_from_chat' in msg:
                chat = msg['forward_from_chat']
                print(f"   Канал: {chat.get('title', '')} (ID: {chat['id']})")
                
        elif 'channel_post' in update:
            msg = update['channel_post']
            print(f"   Тип: пост из канала")
            print(f"   Канал: {msg['chat'].get('title', '')} (ID: {msg['chat']['id']})")
            print(f"   Текст: {msg.get('text', '❌')[:200]}")
            
        else:
            print(f"   Неизвестный тип: {json.dumps(update, ensure_ascii=False)[:300]}")

print(f"\n{'='*60}")
print("💡 Если сообщений нет:")
print("   1. Перешли пост из канала боту @vera_the_poet_bot")
print("   2. Запусти эту проверку снова")
print(f"{'='*60}")