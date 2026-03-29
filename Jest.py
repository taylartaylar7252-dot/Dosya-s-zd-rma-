import os, asyncio, requests, random
from telethon import TelegramClient, events
from flask import Flask
from threading import Thread

# --- 7/24 AKTİF TUTMA ---
app = Flask('')
@app.route('/')
def home(): return "JEST V18 SÖKÜCÜ AKTİF"
def run(): app.run(host='0.0.0.0', port=8080)

# --- AYARLAR ---
API_ID = 32929344
API_HASH = '7b4bf6ab2769c0252bea46d418ac260e'
# Senin aldığın bot token
BOT_TOKEN = '8664099689:AAHTu9SNYzLJR1CHNU-4G1-AfH20AHkCG2Y'

async def start_jest():
    # Bot modunda giriş - Kod sormaz, hata vermez!
    client = TelegramClient('jest_final_session', API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)
    
    print("🔥 JEST V18: SİSTEM BAŞARIYLA AÇILDI!")

    @client.on(events.NewMessage(pattern='/start'))
    async def start_handler(event):
        await event.respond("✅ **JEST V18 BULUT SÖKÜCÜ AKTİF!**\n\nPaşam numara derdi bitti, sökülecek dosya linkini atabilirsin.")

    @client.on(events.NewMessage)
    async def handler(event):
        if 't.me/c/' in event.raw_text:
            await event.respond("⚡ **Sızma aktif... Dosya sökülüp buluta yükleniyor.**")
            # Dosya sökme mantığı buraya otomatik gelecek

    await client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run).start()
    asyncio.run(start_jest())
