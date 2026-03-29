import os, asyncio, requests
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread

# --- 7/24 AKTİF TUTMA (RENDER İÇİN ŞART) ---
app = Flask('')
@app.route('/')
def home(): return "SİSTEM AKTİF"
def run(): app.run(host='0.0.0.0', port=10000)

# --- AYARLAR ---
API_ID = 32929344
API_HASH = '7b4bf6ab2769c0252bea46d418ac260e'
# Render Paneli -> Settings -> Environment Variables -> 'OTURUM' adıyla session ekle
STRING_SESSION = os.environ.get('OTURUM')

async def start_bot():
    if not STRING_SESSION:
        print("❌ HATA: 'OTURUM' değişkeni Render panelinde bulunamadı!")
        return

    # Userbot girişi: Kısıtlı kanallara sızmanın tek yolu
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    
    try:
        await client.start()
        print("✅ SÖKÜCÜ MOTOR ÇALIŞTI!")
    except Exception as e:
        print(f"❌ GİRİŞ HATASI: {e}")
        return

    @client.on(events.NewMessage)
    async def sökücü(event):
        # Sadece özel mesajda ve kısıtlı link gelince çalış
        if event.is_private and 't.me/c/' in event.raw_text:
            status = await event.respond("⚡ **Sızılıyor...**")
            try:
                # Linkten ID ve Mesaj No çekme
                parts = event.raw_text.split('/')
                k_id = int("-100" + parts[-2])
                m_id = int(parts[-1])
                
                # Mesajı çek
                msg = await client.get_messages(k_id, ids=m_id)
                
                if msg and msg.media:
                    await status.edit("🛡️ **Bypass yapıldı. Dosya sökülüyor...**")
                    path = await client.download_media(msg.media)
                    
                    # Buluta Yükleme (BashUpload - Hızlı ve Kayıtsız)
                    await status.edit("☁️ **Buluta yükleniyor...**")
                    with open(path, 'rb') as f:
                        res = requests.post('https://bashupload.com/', files={'file': f}).text.strip()
                    
                    # Sonuç Linki
                    await status.edit(f"✅ **Sökme Başarılı!**\n\n🔗 **Link:** `{res}`")
                    if os.path.exists(path): os.remove(path)
                else:
                    await status.edit("❌ **Hata:** Linkte dosya yok.")
            except Exception as e:
                await status.edit(f"⚠️ **Sistem Hatası:** {str(e)}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    # Flask sunucusunu arka planda başlat
    Thread(target=run).start()
    # Botu ana döngüde başlat
    asyncio.run(start_bot())
