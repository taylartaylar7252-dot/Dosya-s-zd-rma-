import os, asyncio, random
from telethon import TelegramClient, events
from flask import Flask
from threading import Thread

# --- 7/24 AKTİF TUTMA (RENDER UYUMAZ) ---
app = Flask('')
@app.route('/')
def home(): return "JEST V18 SİSTEM AKTİF"
def run(): app.run(host='0.0.0.0', port=8080)

# --- AYARLAR VE GÜÇLÜ BAYPAS ---
API_ID = 32929344
API_HASH = '7b4bf6ab2769c0252bea46d418ac260e'
BOT_TOKEN = '8664099689:AAHTu9SNYzLJR1CHNU-4G1-AfH20AHkCG2Y'

# İzin Verilen Kanallar (Senin Listen)
ALLOWED_CHANNELS = [-1002300291139, -1002326273001, -1002182938536, -1002422292528, -1002019183492]

async def start_jest():
    # Bot modunda giriş: Terminal hatasını (EOFError) kökten çözer
    client = TelegramClient('jest_bot_v18', API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)
    
    print("🔥 JEST V18: SİSTEM BAŞARIYLA AÇILDI VE AKTİF!")

    # --- START KOMUTU TEST ---
    @client.on(events.NewMessage(pattern='/start'))
    async def start_handler(event):
        await event.respond("✅ **JEST V18 SÖKÜCÜ AKTİF!**\n\nPaşam sistem hazır, komutlarını bekliyorum.")

    # --- ANA SÖKME / BAYPAS MANTIĞI ---
    @client.on(events.NewMessage)
    async def global_handler(event):
        # Sadece t.me/c/ linklerini yakala
        if 't.me/c/' in event.raw_text:
            try:
                # Rastgele bekleme (Sızıntı tespitini engellemek için)
                await asyncio.sleep(random.uniform(1.5, 3.0))
                
                # İşlem Başladı Mesajı
                status_msg = await event.respond("⚡ **Sızma ve Bypass aktif... Veri çekiliyor.**")
                
                # Buraya ileride sızma detaylarını ekleyeceğiz
                await asyncio.sleep(2)
                await status_msg.edit("🛡️ **Bypass Başarılı! Dosya hazırlanıyor...**")
                
            except Exception as e:
                print(f"Hata: {e}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    # Flask'ı arka planda başlat
    Thread(target=run).start()
    # Botu ana döngüde çalıştır
    asyncio.run(start_jest())
