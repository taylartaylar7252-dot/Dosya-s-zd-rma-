import os, asyncio, requests, time, re
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.network import ConnectionTcpObfuscated
from flask import Flask
from threading import Thread

# Sunucunun kapanmaması için gerekli web paneli
app = Flask('')
@app.route('/')
def home(): return "YaXY SIZDIRMA BOTU AKTİF"
def run(): app.run(host='0.0.0.0', port=10000)

# --- SENİN GÜNCEL BİLGİLERİN ---
API_ID = 32929344
API_HASH = '7b4bf6ab2769c0252bea46d418ac260e'
STRING_SESSION = '8551541188' # Senin verdiğin ID/Session

# --- KANAL VE ADMİN AYARLARI ---
KANAL_1 = "https://t.me/kanalv1v1v1"
KANAL_2 = "https://t.me/jest1v8"
ADMIN_USER = "@Vhwk3"

async def start_bot():
    # Bağlantıyı Obfuscated (Gizli) protokol ile kurarız
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH, connection=ConnectionTcpObfuscated)
    await client.start()
    
    await client.send_message('me', "🚀 **YaXY SIZDIRMA SİSTEMİ BAŞLATILDI!**\n\nKısıtlı kanal linkini gönder, saniyeler içinde sızdırayım.")

    @client.on(events.NewMessage)
    async def sökücü(event):
        # Sadece kısıtlı kanal linklerini (t.me/c/...) yakalar
        if event.is_private and 't.me/c/' in event.raw_text:
            status = await event.respond("🛡️ **Veri Sızdırılıyor... Lütfen Bekleyin.**")
            try:
                parts = event.raw_text.split('/')
                k_id, m_id = int("-100" + parts[-2]), int(parts[-1])
                msg = await client.get_messages(k_id, ids=m_id)
                
                if msg and msg.media:
                    # Dosyayı sunucuya indirir (Kendi internetini yemez)
                    path = await client.download_media(msg.media)
                    file_name = os.path.basename(path)
                    
                    # Açıklamayı sök ve şablona bular
                    original_desc = msg.text if msg.text else "Özellik Belirtilmemiş"
                    lines = original_desc.split('\n')
                    formatted_features = ""
                    for line in lines:
                        clean = line.strip()
                        if clean:
                            # Diğer reklamları senin adınla (@Vhwk3) değiştirir
                            clean = re.sub(r'@\w+', ADMIN_USER, clean)
                            formatted_features += f"╠❰ {clean}\n"

                    # Buluta Yükle
                    with open(path, 'rb') as f:
                        res = requests.post('https://transfer.sh/', files={file_name: f})
                        link = res.text.strip()

                    # --- SENİN ÖZEL YaXY ŞABLONUN ---
                    final_msg = (
                        f"• **Dosya Adı:** `{file_name}`\n\n"
                        f"╔═════════════╕\n"
                        f"╠❰ Özellikler❱═❍\n"
                        f"{formatted_features}"
                        f"╠═❍ HER DOSYA RİSK TAŞIR \n"
                        f"╚═════════════╛\n"
                        f"╔━━━━━━━━━━━━╕\n"
                        f"╠❰ YaXY Bot Sızdırma Başarılı \n"
                        f"╚━━━━━━━━━━━━╛\n"
                        f"╔═════════════╕\n"
                        f"╠🗣️ ONIVER: {ADMIN_USER}\n"
                        f"╠👣 Katıl: {KANAL_1}\n"
                        f"╠👣 Katıl: {KANAL_2}\n"
                        f"╚═════════════╛\n\n"
                        f"🔗 **Bulut Linki:** {link}\n"
                        f"━━━━━━━━━━━\n"
                        f"Dosya çalıntıdır Ban riskini taşır\n"
                        f"━━━━━━━━━━━"
                    )
                    
                    await status.delete()
                    await event.respond(final_msg)
                    if os.path.exists(path): os.remove(path)
                else:
                    await status.edit("❌ Linkte dosya bulunamadı.")
            except Exception as e:
                await status.edit(f"⚠️ **Hata:** {str(e)}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run, daemon=True).start()
    asyncio.run(start_bot())
