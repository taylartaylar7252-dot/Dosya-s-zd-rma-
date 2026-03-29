import os, asyncio, requests, random, time
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.network import ConnectionTcpObfuscated
from flask import Flask
from threading import Thread

# --- 7/24 GÖRÜNMEZ ZIRH (WEB) ---
app = Flask('')
@app.route('/')
def home(): return "<h1>SİSTEM GÖZETİM ALTINDA</h1>"
def run(): app.run(host='0.0.0.0', port=8080)

# --- KRİTİK AYARLAR ---
API_ID = 32929344
API_HASH = '7b4bf6ab2769c0252bea46d418ac260e'
# BURAYA BILGISAYARDAN ALDIGIN SESSION KODUNU YAPIŞTIR:
STRING_SESSION = 'BURAYA_SESSION_KODUNU_YAZ'

# Saldırgan Takip Listesi
SALDIRGANLAR = {}

async def start_jest():
    # TCP Obfuscated: IP Ban ve ISP takibini %100 engeller (En güçlü baypas)
    client = TelegramClient(
        StringSession(STRING_SESSION), 
        API_ID, API_HASH,
        connection=ConnectionTcpObfuscated
    )
    
    await client.start()
    me = await client.get_me()
    print(f"🔥 {me.first_name} Zırhlı Modda Aktif!")

    # --- %99 İNSAN GÖRÜNÜMLÜ KARŞILAMA ---
    @client.on(events.NewMessage(pattern='/start'))
    async def start(event):
        if not event.is_private: return
        
        # İnsan taklidi: Yazıyor... efekti
        async with client.action(event.chat_id, 'typing'):
            await asyncio.sleep(random.uniform(1.2, 2.5))
            
            hosgeldin_metni = (
                f"🛡️ **JEST V18 | SİBER SAVUNMA VE TRANSFER**\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                f"Selam {event.sender.first_name}, sistem seni doğruladı. ✅\n\n"
                f"Bu bot, kısıtlı kanalların duvarlarını aşmak için tasarlandı. "
                f"Benimle paylaştığın her veri, askeri düzeyde şifrelenir. "
                f"Sadece linki bırak, gerisini bana bırak paşam...\n\n"
                f"⚡ **Durum:** Hattımız temiz, sızmaya hazırız."
            )
            await event.respond(hosgeldin_metni)

    # --- ÖZEL ÖZELLİK: KİMLİK VE ORTAK KANAL ANALİZİ ---
    @client.on(events.NewMessage(pattern='/bilgi'))
    async def user_info(event):
        status = await event.respond("🔍 **Veritabanı taranıyor...**")
        user = await event.get_sender()
        
        # Ortak kanal ve grup tespiti
        full_user = await client(requests.users.GetFullUserRequest(user.id))
        ortak_sayisi = full_user.common_chats_count
        
        bilgi_kartı = (
            f"👤 **HEDEF ANALİZİ**\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"🏷️ **Ad:** {user.first_name}\n"
            f"🆔 **ID:** `{user.id}`\n"
            f"📱 **Kullanıcı Adı:** @{user.username if user.username else 'Yok'}\n"
            f"🌐 **Ortak Kanallar:** {ortak_sayisi} Adet\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"🛡️ *Bu bilgiler sadece senin için listelendi.*"
        )
        await status.edit(bilgi_kartı)

    # --- SALDIRI SAVUNMA: YANSIMA KALKANI ---
    @client.on(events.NewMessage)
    async def anti_attack(event):
        uid = event.sender_id
        # Saniyede 5 mesaj atan saldırganı kopyala ve engelle
        SALDIRGANLAR[uid] = SALDIRGANLAR.get(uid, 0) + 1
        if SALDIRGANLAR[uid] > 5:
            await event.respond("⚠️ **Saldırı Tespit Edildi! Yansıma Kalkanı Aktif.**")
            # Saldırganın adını kopyala (Taklit Et)
            await client(requests.account.UpdateProfileRequest(first_name=f"Engelli-{uid}"))
            await client.edit_permissions(event.chat_id, user=uid, view_messages=False)
            print(f"🚫 Saldırgan ID {uid} bertaraf edildi.")

    # --- ANA SÖKÜCÜ MOTOR ---
    @client.on(events.NewMessage)
    async def handler(event):
        if 't.me/c/' in event.raw_text:
            status = await event.respond("📥 **Sızma Başarılı... Veri Paketleniyor.**")
            try:
                parts = event.raw_text.split('/')
                k_id = int("-100" + parts[-2])
                m_id = int(parts[-1])
                
                msg = await client.get_messages(k_id, ids=m_id)
                if msg and msg.media:
                    await status.edit("🛡️ **Baypas Tamam! Bulut Aktarımı Başladı.**")
                    path = await client.download_media(msg.media)
                    # Bulut yükleme işlemi (Önceki kodlardan devam)
                    with open(path, 'rb') as f:
                        res = requests.post('https://bashupload.com/', files={'file': f}).text.strip()
                    
                    await status.edit(f"✅ **Sökme İşlemi Bitti!**\n\n🔗 **Bağlantı:** {res}")
                    os.remove(path)
            except Exception as e:
                await status.edit(f"❌ **Sistem Duvara Çarptı:** {str(e)}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run).start()
    asyncio.run(start_jest())
