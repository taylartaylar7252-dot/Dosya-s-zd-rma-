import os, asyncio, requests, random, time
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.network import ConnectionTcpObfuscated
from flask import Flask
from threading import Thread

# --- GÖRÜNMEZ SİBER KALKAN (7/24) ---
app = Flask('')
@app.route('/')
def home(): return "<h1>SİSTEM GÖZETİM ALTINDA...</h1>"
def run(): app.run(host='0.0.0.0', port=8080)

# --- KRİTİK VERİLER ---
API_ID = 32929344
API_HASH = '7b4bf6ab2769c0252bea46d418ac260e'
# Bilgisayardan aldığın o uzun kodu buraya yapıştır:
STRING_SESSION = 'BURAYA_SESSION_KODUNU_YAPIŞTIR'

async def start_jest():
    # En güçlü baypas: ISP ve IP engellerini aşan TCP Obfuscated bağlantı
    client = TelegramClient(
        StringSession(STRING_SESSION), 
        API_ID, API_HASH,
        connection=ConnectionTcpObfuscated
    )
    
    try:
        await client.start()
        me = await client.get_me()
        print(f"🔥 SİSTEM ÇALIŞTI: {me.first_name} OPERASYONA HAZIR!")
    except Exception as e:
        print(f"❌ KRİTİK HATA: {e}")
        return

    # --- %99 İNSAN GÖRÜNÜMLÜ ELİT KARŞILAMA ---
    @client.on(events.NewMessage(pattern='/start'))
    async def start_handler(event):
        if not event.is_private: return
        
        # İnsan taklidi: Yazıyor efekti
        async with client.action(event.chat_id, 'typing'):
            await asyncio.sleep(random.uniform(1.5, 3.0))
            
            ana_mesaj = (
                f"🛡️ **JEST V18 | SİBER SIZMA VE TRANSFER ÜSSÜ**\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                f"Hoş geldin Operatör {event.sender.first_name}. ✅\n\n"
                f"Şu an Telegram'ın en derin kısıtlı kanallarına sızabilen "
                f"ve veri sökebilen **Gölge Protokolü** altındasın. "
                f"Sistem, kimliğini %99 oranında gizler ve gerçek bir kullanıcı "
                f"gibi davranarak filtreleri uyutur.\n\n"
                f"📡 **Durum:** Bağlantı şifreli, IP Korunuyor.\n"
                f"📥 **Görev:** İndirme yasağı olan kanal linkini gönder."
            )
            await event.respond(ana_mesaj)

    # --- ÖZEL ÖZELLİK: HEDEF KİMLİK ANALİZİ ---
    @client.on(events.NewMessage(pattern='/analiz'))
    async def analyze(event):
        status = await event.respond("🔍 **Veritabanı taranıyor, hedef analiz ediliyor...**")
        await asyncio.sleep(1.5)
        user = await event.get_sender()
        
        # Ortak kanal/grup tespiti (Askeri rapor formatı)
        from telethon.tl.functions.users import GetFullUserRequest
        full = await client(GetFullUserRequest(user.id))
        
        rapor = (
            f"👤 **HEDEF KİMLİK KARTI**\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"🔹 **İsim:** {user.first_name}\n"
            f"🔹 **ID:** `{user.id}`\n"
            f"🔹 **Siber Ad:** @{user.username if user.username else 'Gizli'}\n"
            f"🔹 **Ortak Alanlar:** {full.common_chats_count} Kanal/Grup\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"🛡️ *Bu veri sadece operatör yetkisiyle çekilmiştir.*"
        )
        await status.edit(rapor)

    # --- SALDIRI SAVUNMA (YANSIMA KALKANI) ---
    flood_check = {}
    @client.on(events.NewMessage)
    async def mirror_shield(event):
        uid = event.sender_id
        current_time = time.time()
        
        # Saniyede 3 mesajdan fazlası saldırı kabul edilir
        user_history = flood_check.get(uid, [])
        user_history = [t for t in user_history if current_time - t < 5]
        user_history.append(current_time)
        flood_check[uid] = user_history
        
        if len(user_history) > 4:
            await event.respond("⚠️ **SALDIRI TESPİT EDİLDİ!**\nYansıma Kalkanı aktif. Erişim engelleniyor...")
            await client.edit_permissions(event.chat_id, user=uid, view_messages=False)
            print(f"🚫 Saldırgan bertaraf edildi: {uid}")

    # --- ANA KISITLI VERİ SÖKÜCÜ ---
    @client.on(events.NewMessage)
    async def download_handler(event):
        if 't.me/c/' in event.raw_text:
            status = await event.respond("⚡ **Kısıtlı alana sızılıyor... Güvenlik baypas ediliyor.**")
            try:
                parts = event.raw_text.split('/')
                k_id = int("-100" + parts[-2])
                m_id = int(parts[-1])
                
                msg = await client.get_messages(k_id, ids=m_id)
                if msg and msg.media:
                    await status.edit("🛡️ **Veri Söküldü! Buluta şifreli aktarım yapılıyor...**")
                    path = await client.download_media(msg.media)
                    
                    # Bulut Yükleme (Hızlı ve Güvenli)
                    with open(path, 'rb') as f:
                        res = requests.post('https://bashupload.com/', files={'file': f}).text.strip()
                    
                    await status.edit(f"✅ **Operasyon Başarılı!**\n\n🔗 **İndirme Linki:**\n`{res}`\n\n⌛ *Link 24 saat içinde imha edilecektir.*")
                    if os.path.exists(path): os.remove(path)
                else:
                    await status.edit("❌ **Hata:** Hedef noktada sökülecek veri bulunamadı.")
            except Exception as e:
                await status.edit(f"⚠️ **Sistem Duvara Çarptı:** {str(e)}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run).start()
    asyncio.run(start_jest())
