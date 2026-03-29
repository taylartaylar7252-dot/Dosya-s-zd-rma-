import os, asyncio, requests, random
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread

# --- 7/24 UYANIK TUTMA (WEB SUNUCUSU) ---
app = Flask('')
@app.route('/')
def home(): return "<h1>JEST V18 SÖKÜCÜ MOTOR AKTİF</h1>"
def run(): app.run(host='0.0.0.0', port=8080)

# --- AYARLAR ---
API_ID = 32929344
API_HASH = '7b4bf6ab2769c0252bea46d418ac260e'
# BURAYA BILGISAYARDAN ALDIGIN O COK UZUN KODU YAPIŞTIR:
STRING_SESSION = 'BURAYA_ALDIĞIN_SESSION_KODUNU_YAPIŞTIR'

# Bulut Yükleme Motoru
def bulut_yukle(yol):
    try:
        with open(yol, 'rb') as f:
            r = requests.post('https://bashupload.com/', files={'file': f}, timeout=120)
            return r.text.strip() if 'https://' in r.text else "❌ Yükleme hatası!"
    except: return "❌ Bulut servisi yanıt vermiyor!"

async def start_jest():
    # StringSession ile giriş: Numara/Kod/Yönetici derdini bitiren Bypass budur!
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    
    try:
        await client.start()
        me = await client.get_me()
        print(f"🔥 JEST V18: {me.first_name} HESABIYLA SİSTEM AKTİF!")
    except Exception as e:
        print(f"❌ SESSION HATASI: {e}")
        return

    # --- ŞIK KARŞILAMA VE AÇIKLAMA ---
    @client.on(events.NewMessage(pattern='/start'))
    async def start(event):
        if not event.is_private: return
        mesaj = (
            "🚀 **JEST V18 | KISITLI KANAL SÖKÜCÜ**\n"
            "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            "👋 **Hoş geldin Paşam!**\n\n"
            "🛡️ **Bu Bot Ne Yapar?**\n"
            "Kısıtlı, indirme yasağı olan veya gizli kanallardaki dosyaları "
            "senin adına sızıp söker ve bulut linki olarak teslim eder.\n\n"
            "⚠️ **Uyarı:** Saniyede birden fazla link atma, sistem banlayabilir.\n\n"
            "📥 **Kullanım:** Sadece `t.me/c/123/456` şeklindeki linki buraya at!"
        )
        await event.respond(mesaj)

    # --- ANA SÖKÜCÜ MOTOR ---
    @client.on(events.NewMessage)
    async def handler(event):
        if not event.is_private or '/start' in event.raw_text: return
        
        if 't.me/c/' in event.raw_text:
            status = await event.respond("⚡ **Sızma işlemi başlatıldı... Veri sökülüyor.**")
            try:
                # Link Analizi
                parts = event.raw_text.split('/')
                k_id = int("-100" + parts[-2])
                m_id = int(parts[-1])
                
                # Dosyayı senin yetkinle çek (Yönetici olmana gerek yok!)
                msg = await client.get_messages(k_id, ids=m_id)
                
                if msg and msg.media:
                    await status.edit("🛡️ **Bypass Başarılı! Dosya buluta aktarılıyor...**")
                    yol = await client.download_media(msg.media)
                    link = bulut_yukle(yol)
                    
                    await status.edit(f"✅ **Dosya Söküldü!**\n\n🔗 **İndirme Bağlantısı:**\n`{link}`\n\n⌛ *Link ömrü: 24 Saat*")
                    if os.path.exists(yol): os.remove(yol)
                else:
                    await status.edit("❌ **Hata:** Linkte indirilebilir bir medya bulunamadı.")
            except Exception as e:
                await status.edit(f"⚠️ **Sökme Başarısız:** {str(e)}\n\n*Not: Linkin doğruluğunu ve kanalda üye olup olmadığını kontrol et paşam.*")

    await client.run_until_disconnected()

if __name__ == "__main__":
    # Tek bir thread başlatarak mükerrer mesajı engelliyoruz
    t = Thread(target=run)
    t.daemon = True
    t.start()
    asyncio.run(start_jest())
