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

# --- DOSYA YÜKLEME MOTORU (Bulut Aktarımı) ---
def bulut_yukle(dosya_yolu):
    try:
        with open(dosya_yolu, 'rb') as f:
            # Bashupload kullanarak 24 saatlik link oluşturur
            r = requests.post('https://bashupload.com/', files={'file': f}, timeout=120)
            return r.text.strip() if 'https://' in r.text else "❌ Bulut yükleme başarısız!"
    except:
        return "❌ Bulut servisi yanıt vermiyor!"

async def start_jest():
    client = TelegramClient('jest_v18_final_engine', API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)
    print("🔥 JEST V18: SÖKÜCÜ MOTOR BAŞARIYLA ATEŞLENDİ!")

    @client.on(events.NewMessage(pattern='/start'))
    async def start(event):
        await event.respond("✅ **JEST V18 SÖKÜCÜ MOTOR HAZIR!**\n\nPaşam linki at, söküp buluta uçurayım.")

    @client.on(events.NewMessage)
    async def handler(event):
        if 't.me/c/' in event.raw_text:
            try:
                # Linki analiz et (Kanal ID ve Mesaj ID)
                link_parts = event.raw_text.split('/')
                kanal_id = int("-100" + link_parts[-2])
                mesaj_id = int(link_parts[-1])
                
                status = await event.respond("⚡ **Sızma başarılı... Dosya sökülüyor...**")
                
                # DOSYAYI ÇEK (Botun kanalda olması şarttır!)
                mesaj = await client.get_messages(kanal_id, ids=mesaj_id)
                
                if mesaj and mesaj.media:
                    await status.edit("🛡️ **Bypass yapıldı! Dosya buluta aktarılıyor...**")
                    
                    # Dosyayı sunucuya indir
                    indirilen_yol = await client.download_media(mesaj.media)
                    
                    # Buluta yükle
                    bulut_linki = bulut_yukle(indirilen_yol)
                    
                    await status.edit(f"✅ **Dosya Başarıyla Söküldü!**\n\n📥 **Bulut Linki:** {bulut_linki}\n\n⚠️ *Not: Link 24 saat sonra silinir.*")
                    
                    # Sunucuda yer kaplamasın diye temizle
                    if os.path.exists(indirilen_yol):
                        os.remove(indirilen_yol)
                else:
                    await status.edit("❌ **Hata:** Linkte indirilebilir bir dosya yok veya botun yetkisi yetersiz.")
            
            except Exception as e:
                await event.respond(f"⚠️ **Sistem Hatası:** Bot bu kanala erişemiyor.\n\n**Çözüm:** Botu (@Kisitlitiransferrobot) o kanala yönetici olarak ekle paşam.")

    await client.run_until_disconnected()

if __name__ == "__main__":
    Thread(target=run).start()
    asyncio.run(start_jest())
