import os, asyncio, requests, random, time
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.network import ConnectionTcpObfuscated
from flask import Flask
from threading import Thread

# --- 7/24 KESİNTİSİZ HAT (RENDER) ---
app = Flask('')
@app.route('/')
def home(): return "<h1>JEST V18: SİSTEM GÖZETİMİ AKTİF</h1>"
def run(): app.run(host='0.0.0.0', port=8080)

# --- SİBER AYARLAR ---
API_ID = 32929344
API_HASH = '7b4bf6ab2769c0252bea46d418ac260e'
# Render -> Settings -> Environment Variables kısmına 'OTURUM_KODU' olarak ekle!
STRING_SESSION = os.environ.get('OTURUM_KODU')

async def start_jest():
    if not STRING_SESSION:
        print("❌ KRİTİK HATA: OTURUM_KODU ayarlanmamış!")
        return

    # TCP Obfuscated: IP Ban koruması ve siber gizlilik
    client = TelegramClient(
        StringSession(STRING_SESSION), API_ID, API_HASH,
        connection=ConnectionTcpObfuscated
    )
    
    await client.start()
    me = await client.get_me()
    print(f"🔥 Operatör {me.first_name} sahada!")

    # --- %99 İNSAN GÖRÜNÜMLÜ ELİT KARŞILAMA ---
    @client.on(events.NewMessage(pattern='/start'))
    async def start(event):
        if not event.is_private: return
        async with client.action(event.chat_id, 'typing'):
            await asyncio.sleep(random.uniform(1.5, 3.0)) # İnsan taklidi
            msg = (
                f"🛡️ **JEST V18 | GÖLGE PROTOKOLÜ**\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                f"Selam Operatör {event.sender.first_name}. ✅\n\n"
                f"Kısıtlı kanalların duvarlarını aşmak için sistem hazır. "
                f"Girdiğin linkler askeri düzeyde baypas edilerek sökülür.\n\n"
                f"📡 **Durum:** Bağlantı şifreli, sızmaya hazır.\n"
                f"📥 **Görev:** Kısıtlı kanal linkini buraya bırak."
            )
            await event.respond(msg)

    # --- HEDEF ANALİZİ (ID, Kullanıcı Adı, Ortak Kanallar) ---
    @client.on(events.NewMessage(pattern='/analiz'))
    async def analyze(event):
        status = await event.respond("🔍 **Hedef taranıyor...**")
        user = await event.get_sender()
        from telethon.tl.functions.users import GetFullUserRequest
        full = await client(GetFullUserRequest(user.id))
        
        rapor = (
            f"👤 **HEDEF KİMLİK ANALİZİ**\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"🔹 **Ad:** {user.first_name}\n"
            f"🔹 **ID:** `{user.id}`\n"
            f"🔹 **Kullanıcı Adı:** @{user.username if user.username else 'Gizli'}\n"
            f"🔹 **Ortak Alanlar:** {full.common_chats_count} Grup/Kanal\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"🛡️ *Veri sızdırıldı.*"
        )
        await status.edit(rapor)

    # --- SALDIRI SAVUNMA (YANSIMA KALKANI) ---
    flood_cache = {}
    @client.on(events.NewMessage)
    async def mirror_shield(event)
        uid = event.sender_id
        now = time.time()
        flood_cache[uid] = [t for t in flood_cache.get(uid, []) if now - t < 5]
        flood_cache[uid].append(now)
        
        if len(flood_cache[uid]) > 5: # Saldırı tespiti
            await event.respond("⚠️ **Saldırı Engellendi! Yansıma Kalkanı Devrede.**")
            await client.edit_permissions(event.chat_id, user=uid, view_messages=False)
            print(f"🚫 Saldırgan bertaraf: {uid}")

    # --- ANA VERİ SÖKÜCÜ MOTOR ---
    @client.on(events.NewMessage)
    async def sökücü(event):
        if 't.me/c/' in event.raw_text:
            status = await event.respond("📥 **Sızılıyor... Veri sökülüyor.**")
            try:
                parts = event.raw_text.split('/')
                k_id, m_id = int("-100" + parts[-2]), int(parts[-1])
                msg = await client.get_messages(k_id, ids=m_id)
                
                if msg and msg.media:
                    await status.edit("🛡️ **Baypas başarılı! Buluta aktarılıyor...**")
                    path = await client.download_media(msg.media)
                    # Dosya transferi
                    with open(path, 'rb') as f:
                        link = requests.post('https://bashupload.com/', files={'file': f}).text.strip()
                    
                    await status.edit(f"✅ **Sökme Başarılı!**\n\n🔗 **Link:** `{link}`\n\n⌛ *İmha süresi: 24 Saat*")
                    os.remove(path)
                else:
                    await status.edit("❌ **Hata:** Veri bulunamadı.")
            except Exception as e:
                await status.edit(f"⚠️ **Sistem Hatası:** {str(e)}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run, daemon=True).start()
    asyncio.run(start_jest())
