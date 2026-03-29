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
BOT_TOKEN = '8664099689:AAHTu9SNYzLJR1CHNU-4G1-AfH20AHkCG2Y'

# --- DOSYA YÜKLEME MOTORU ---
def bulut_yukle(dosya_yolu):
    try:
        with open(dosya_yolu, 'rb') as f:
            r = requests.post('https://bashupload.com/', files={'file': f}, timeout=60)
            return r.text.strip() if 'https://' in r.text else "❌ Yükleme başarısız!"
    except: return "❌ Bulut hatası!"

async def start_jest():
    client = TelegramClient('jest_v18_final', API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)
    print("🔥 JEST V18: SÖKÜCÜ MOTOR ÇALIŞTI!")

    @client.on(events.NewMessage(pattern='/start'))
    async def start(event):
        await event.respond("✅ **JEST V18 SÖKÜCÜ HAZIR!**\n\nPaşam linki at, saniyeler içinde dosyanı söküp getireyim.")

    @client.on(events.NewMessage)
    async def handler(event):
        if 't.me/c/' in event.raw_text:
            try:
                # Linki parçala
                link = event.raw_text.split('/')
                kanal_id = int("-100" + link[-2])
                mesaj_id = int(link[-1])
                
                status = await event.respond("⚡ **Sızma başarılı... Dosya sökülüyor...**")
                
                # DOSYAYI ÇEK (BOT KANALDA OLMALIDIR)
                mesaj = await client.get_messages(kanal_id, ids=mesaj_id)
                
                if mesaj and mesaj.media:
                    await status.edit("🛡️ **Bypass yapıldı! Dosya buluta aktarılıyor...**")
                    yol = await client.download_media(mesaj.media)
                    link_sonuc = bulut_yukle(yol)
                    
                    await status.edit(f"✅ **Dosya Söküldü!**\n\n📥 **Link:** {link_sonuc}")
                    if os.path.exists(yol): os.remove(yol)
                else:
                    await status.edit("❌ **Hata:** Dosya bulunamadı! Botun o kanalda olduğundan emin ol paşam.")
            except Exception as e:
                await event.respond(f"⚠️ **Sistem Hatası:** Bot bu kanalı göremiyor. Kanalda yetkili miyim paşam?")

    await client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run).start()
    asyncio.run(start_jest())
