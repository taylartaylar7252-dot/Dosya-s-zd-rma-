import os, asyncio, requests, random, time
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread

# --- 7/24 AKTİF TUTMA ---
app = Flask('')
@app.route('/')
def home(): return "SİSTEM ÇEVRİMİÇİ"
def run(): app.run(host='0.0.0.0', port=8080)

# --- AYARLAR ---
API_ID = 32929344
API_HASH = '7b4bf6ab2769c0252bea46d418ac260e'
# Render Paneli -> Environment kısmına OTURUM_KODU adıyla ekle
OTURUM = os.environ.get('OTURUM_KODU')

async def start_jest():
    if not OTURUM:
        print("❌ HATA: OTURUM_KODU bulunamadı! Render ayarlarına ekle.")
        return

    # Userbot olarak giriş (Kısıtlı kanallara senin yetkinle sızar)
    client = TelegramClient(StringSession(OTURUM), API_ID, API_HASH)
    await client.start()
    print("🔥 JEST V18 SAHADA!")

    @client.on(events.NewMessage(pattern='/start'))
    async def start(event):
        if not event.is_private: return
        async with client.action(event.chat_id, 'typing'):
            await asyncio.sleep(1)
            await event.respond("🚀 **JEST V18 AKTİF!**\n\nPaşam linki at, saniyeler içinde sökeyim.")

    @client.on(events.NewMessage)
    async def handler(event):
        if 't.me/c/' in event.raw_text:
            status = await event.respond("⚡ **Sızılıyor...**")
            try:
                parts = event.raw_text.split('/')
                k_id, m_id = int("-100" + parts[-2]), int(parts[-1])
                msg = await client.get_messages(k_id, ids=m_id)
                
                if msg and msg.media:
                    await status.edit("🛡️ **Bypass başarılı! Buluta aktarılıyor...**")
                    path = await client.download_media(msg.media)
                    with open(path, 'rb') as f:
                        res = requests.post('https://bashupload.com/', files={'file': f}).text.strip()
                    await status.edit(f"✅ **Söküldü!**\n\n🔗 **Link:** `{res}`")
                    os.remove(path)
            except Exception as e:
                await status.edit(f"⚠️ **Hata:** {str(e)}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run, daemon=True).start()
    asyncio.run(start_jest())
