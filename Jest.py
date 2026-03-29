import asyncio, os, nest_asyncio, requests, random
from flask import Flask
from threading import Thread
from telethon import TelegramClient, events
from telethon.network import ConnectionTcpObfuscated

# --- 7/24 UYANIK TUTMA SERVİSİ ---
app = Flask('')
@app.route('/')
def home(): return "JEST V18 ANTI-BAN AKTIF"
def run(): app.run(host='0.0.0.0', port=8080)

# --- SENİN BİLGİLERİN ---
API_ID = 32929344
API_HASH = '7b4bf6ab2769c0252bea46d418ac260e'
PHONE = '+905425689041'
OWNer_ID = 2004968861
ALLOWED_CHANNELS = [-1003538029199, -1002926273001, -1003182938596, -1003422292528, -1003692861861]

def cloud_upload(file_path):
    """Dosyayı buluta sızdırır ve linkini döner"""
    try:
        with open(file_path, 'rb') as f:
            res = requests.post('https://bashupload.com/', files={'file': f}, timeout=30)
            for line in res.text.split('\n'):
                if "https://bashupload.com/" in line:
                    return line.strip()
    except: return "Bulut bağlantı hatası!"
    return "Link oluşturulamadı."

async def main():
    # BYPASS: Gizlenmiş TCP bağlantısı ile Telegram filtresini aşar
    client = TelegramClient(
        'jest_final_session', 
        API_ID, 
        API_HASH,
        connection=ConnectionTcpObfuscated
    )
    
    await client.start(phone=PHONE)
    print("🔥 JEST V18: BULUT + ANTI-BAN SİSTEMİ ÇALIŞIYOR!")

    @client.on(events.NewMessage)
    async def handler(event):
        # Sadece senden gelen mesajları dinler
        if event.sender_id != OWNer_ID: return
        
        text = event.raw_text
        if "t.me/c/" in text:
            try:
                # Ban koruması için rastgele bekleme (1.5 - 3 sn)
                await asyncio.sleep(random.uniform(1.5, 3.0))
                
                status = await event.respond("🛡️ Sızma ve Bypass aktif... Veri çekiliyor.")
                
                # Linki parçalayıp ID'leri bulur
                parts = text.split('/')
                target_id = int("-100" + parts[-2])
                msg_id = int(parts[-1])

                if target_id not in ALLOWED_CHANNELS:
                    await status.edit("⚠️ Bu kanal yetki listenizde yok!")
                    return

                # Mesajı ve medyayı çeker
                msg = await client.get_messages(target_id, ids=msg_id)
                if msg and msg.media:
                    await status.edit("📥 Sunucu dosyayı çekiyor (Sıfır Kota)...")
                    path = await client.download_media(msg.media)
                    
                    await status.edit("🔗 Bulut linki sızdırılıyor...")
                    link = cloud_upload(path)
                    
                    caption = (
                        f"💎 **JEST V18 SONUÇ**\n\n"
                        f"📂 **Dosya:** `{os.path.basename(path)}` \n"
                        f"🌐 **Bulut Linki:** {link}\n\n"
                        f"⚡ Sunucu üzerinden 7/24 kesintisiz iletildi."
                    )
                    
                    await status.edit("📤 Telegram'a şifreli aktarım yapılıyor...")
                    await client.send_file(event.chat_id, path, caption=caption)
                    
                    # Temizlik (Sunucuda yer kaplamasın)
                    if os.path.exists(path): os.remove(path)
                    await status.delete()
                else:
                    await status.edit("⚠️ Medya bulunamadı!")
            except Exception as e:
                await event.respond(f"⚠️ Sistem Hatası: {str(e)}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    # Web sunucusunu yan kolda başlat (Render'ın uyumaması için)
    Thread(target=run).start()
    # Ana bot döngüsünü başlat
    asyncio.run(main())
                  
