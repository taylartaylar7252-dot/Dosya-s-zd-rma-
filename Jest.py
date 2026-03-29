import os, asyncio, requests, random
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread

# --- 7/24 AKTİF TUTMA (RENDER İÇİN) ---
app = Flask('')
@app.route('/')
def home(): return "JEST V18 SÖKÜCÜ MOTOR AKTİF"
def run(): app.run(host='0.0.0.0', port=8080)

# --- AYARLAR ---
API_ID = 32929344
API_HASH = '7b4bf6ab2769c0252bea46d418ac260e'

# DİKKAT: Bilgisayarındaki Python'dan aldığın o uzun kodu buraya yapıştır!
# Bu kod sayesinde bot Render'da senden numara/kod istemez, 7/24 senin hesabınla sızar.
STRING_SESSION = 'BURAYA_BILGISAYARDAN_ALDIGIN_KODU_YAZ'

# Bulut Yükleme Motoru
def bulut_yukle(dosya_yolu):
    try:
        with open(dosya_yolu, 'rb') as f:
            r = requests.post('https://bashupload.com/', files={'file': f}, timeout=120)
            return r.text.strip() if 'https://' in r.text else "❌ Yükleme hatası!"
    except: return "❌ Bulut hatası!"

async def start_jest():
    # StringSession ile giriş: Kesin çözüm, bypass budur!
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    await client.start()
    
    print("🔥 JEST V18: MOTOR 7/24 RENDER ÜZERİNDE AKTİF!")

    @client.on(events.NewMessage)
    async def handler(event):
        if 't.me/c/' in event.raw_text:
            try:
                status = await event.respond("⚡ **Sızma başarılı... Dosya sökülüyor...**")
                
                parts = event.raw_text.split('/')
                kanal_id = int("-100" + parts[-2])
                mesaj_id = int(parts[-1])
                
                mesaj = await client.get_messages(kanal_id, ids=mesaj_id)
                
                if mesaj and mesaj.media:
                    await status.edit("🛡️ **Bypass Tamam! Dosya buluta aktarılıyor...**")
                    yol = await client.download_media(mesaj.media)
                    link = bulut_yukle(yol)
                    
                    await status.edit(f"✅ **Dosya Söküldü!**\n\n📥 **İndirme Linki:** {link}")
                    if os.path.exists(yol): os.remove(yol)
                else:
                    await status.edit("❌ **Hata:** Dosya bulunamadı.")
            except Exception as e:
                await event.respond(f"⚠️ **Hata:** {str(e)}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    # Web sunucusunu arka planda başlat (7/24 uyumaz)
    Thread(target=run).start()
    # Botu çalıştır
    asyncio.run(start_jest())
