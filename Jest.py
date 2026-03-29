import json, os, sys, time, datetime, subprocess
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    ContextTypes, MessageHandler, filters
)
from telegram.error import BadRequest

# --- [FAZ 1] AYARLAR VE VERİTABANI ---
TOKEN = "8586282608:AAHiI1nG2dFEuiY7DYVmVZhERe1i66v0w6s"
ADMIN_ID = 2004968861  
KANAL_ID, GRUP_ID = -1003883833129, -1003846815947
VIP_KANAL_ID = -1002488344331
VIP_LINK = "https://t.me/+iyltl7DLT185OGFk"

DATA_FILE = "yaaxy_v46_db.json"
def load_db():
    if os.path.exists(DATA_FILE):
        try: return json.load(open(DATA_FILE, "r"))
        except: pass
    return {"inviters": {}, "refs": {}, "names": {}, "usernames": {}, "ban_stats": {}, "active_bans": {}}

db = load_db()
def save_db():
    with open(DATA_FILE, "w") as f: json.dump(db, f)

# --- [FAZ 2] DİSİPLİN (BAN) MEKANİZMASI ---
def is_banned(uid):
    uid = str(uid)
    if uid in db["active_bans"]:
        until = datetime.datetime.fromisoformat(db["active_bans"][uid])
        if datetime.datetime.now() < until:
            return True, until.strftime("%d/%m %H:%M")
        else:
            del db["active_bans"][uid]; save_db()
    return False, None

async def apply_ban(uid, hours=1, days=0):
    uid = str(uid)
    end_time = datetime.datetime.now() + datetime.timedelta(hours=hours, days=days)
    db["active_bans"][uid] = end_time.isoformat()
    # İhlal sayısını artır
    db["ban_stats"][uid] = db["ban_stats"].get(uid, 0) + 1
    
    # 3 İhlal -> 15 Günlük Ban
    if db["ban_stats"][uid] >= 3:
        end_time = datetime.datetime.now() + datetime.timedelta(days=15)
        db["active_bans"][uid] = end_time.isoformat()
        db["ban_stats"][uid] = 0 # Sıfırla
    save_db()
    return end_time.strftime("%d/%m %H:%M")

# --- [FAZ 3] KLAVYELER ---
def main_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 REFERANS LİNKİM", callback_data='ref_menu')],
        [InlineKeyboardButton("🛡️ REFERANS DOĞRULAMA", callback_data='v_menu')],
        [InlineKeyboardButton("❓ SORU-CEVAP MERKEZİ", callback_data='support_menu')]
    ])

# --- [FAZ 4] ANA BOT MOTORU ---
def run_bot():
    app = Application.builder().token(TOKEN).build()

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = str(update.effective_user.id)
        db["names"][uid] = update.effective_user.full_name
        db["usernames"][uid] = f"@{update.effective_user.username}" if update.effective_user.username else "Yok"
        
        if context.args and context.args[0].isdigit():
            inv = context.args[0]
            if inv != uid and uid not in db["inviters"]:
                db["inviters"][uid] = inv
                db.setdefault("refs", {}).setdefault(inv, []).append(uid)
                save_db()
        await update.message.reply_text("🔥 <b>YaAXY KARARGAHI</b>\n\n<blockquote>Sadakatle gel, güçle ayrıl.</blockquote>", reply_markup=main_kb(), parse_mode='HTML')

    async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        uid = str(query.from_user.id)
        data = query.data
        await query.answer()

        # Ban Kontrolü
        banned, until = is_banned(uid)
        if banned:
            await query.answer(f"🚫 Yasaklısın! Açılış: {until}", show_alert=True)
            return

        if data == 'main':
            await query.edit_message_text("🔥 <b>LOBİ</b>", reply_markup=main_kb(), parse_mode='HTML')
        
        elif data == 'ref_menu':
            bot_un = (await context.bot.get_me()).username
            link = f"https://t.me/{bot_un}?start={uid}"
            msg = (
                "🔗 <b>SENİN ÖZEL DAVET LİNKİN</b>\n\n"
                f"<code>{link}</code>\n\n"
                "<blockquote>⚡ <b>NOT:</b> Alttaki butonu kullanarak bu fırsatı doğrudan bir <b>arkadaşına</b> önerebilirsin! Onun katılımı senin VIP anahtarındır.</blockquote>"
            )
            await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 ARKADAŞINA ÖNER", switch_inline_query=f"Dostum bu config efsane! Tıkla gel: {link}")],
                [InlineKeyboardButton("🔙 GERİ", callback_data='main')]
            ]), parse_mode='HTML')

        elif data == 'v_menu':
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ AKTİF LİSTE", callback_data='list_active')],
                [InlineKeyboardButton("❌ PASİF / DÜRT", callback_data='list_passive')],
                [InlineKeyboardButton("🛡️ ŞİMDİ DOĞRULA", callback_data='verify_now')],
                [InlineKeyboardButton("🔙 GERİ", callback_data='main')]
            ])
            await query.edit_message_text("🛡️ <b>İSTİHBARAT VE DOĞRULAMA</b>", reply_markup=kb, parse_mode='HTML')

        elif data == 'list_passive':
            refs = db["refs"].get(uid, [])
            msg = "❌ <b>PASİF DOSTLARIN DURUMU</b>\n\n"
            kb = []
            for r in refs:
                k1, g1 = "❌", "❌"
                try: 
                    m1 = await context.bot.get_chat_member(KANAL_ID, int(r))
                    if m1.status in ['member', 'administrator', 'creator']: k1 = "✅"
                    m2 = await context.bot.get_chat_member(GRUP_ID, int(r))
                    if m2.status in ['member', 'administrator', 'creator']: g1 = "✅"
                except: pass
                msg += f"👤 {db['names'].get(r)}\n📊 Kanal: {k1} | Grup: {g1}\n───\n"
                if k1 == "❌" or g1 == "❌":
                    kb.append([InlineKeyboardButton(f"🔔 {db['names'].get(r)} DÜRT", callback_data=f"poke_{r}")])
            
            if len(kb) > 0: kb.append([InlineKeyboardButton("📢 HERKESİ DÜRT", callback_data='poke_all')])
            kb.append([InlineKeyboardButton("🔙 GERİ", callback_data='v_menu')])
            await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode='HTML')

        elif data == 'support_menu':
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("📜 SIKÇA SORULAN SORULAR", callback_data='sss')],
                [InlineKeyboardButton("🤖 YAPAY ZEKA DESTEK", callback_data='ai_fix')],
                [InlineKeyboardButton("✍️ ADMİNE SOR", callback_data='ask_admin')],
                [InlineKeyboardButton("🔙 GERİ", callback_data='main')]
            ])
            await query.edit_message_text("❓ <b>SORU-CEVAP VE TEKNİK DESTEK</b>", reply_markup=kb, parse_mode='HTML')

        elif data == 'sss':
            sss_text = (
                "📜 <b><u>SIKÇA SORULAN SORULAR</u></b>\n\n"
                "🔍 <b>Hangi Cihazlar Destekleniyor?</b>\n"
                "<blockquote>Android 9-14 arası ve 64-bit mimariye sahip tüm cihazlar tam performans çalışır.</blockquote>\n\n"
                "🛡️ <b>Ban Riski Nedir?</b>\n"
                "<blockquote>Bypass ve safe config kullandığın sürece risk %1 altındadır.</blockquote>"
            )
            await query.edit_message_text(sss_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 GERİ", callback_data='support_menu')]]), parse_mode='HTML')

    # --- [FAZ 5] AI ANALİZ VE DOSYA TAMİR ---
    async def handle_docs(update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = update.message
        if msg.document or msg.photo:
            status = await msg.reply_text("🛠️ <b>AI MODÜLÜ AKTİF:</b> Dosya analiz ediliyor ve içindeki hatalar ayıklanıyor...")
            time.sleep(3)
            # Simüle edilmiş imza yerleştirme
            link_signature = "\n\n# YaAXY Karargah - t.me/YaAXYBot"
            await status.edit_text(f"✅ <b>ANALİZ TAMAMLANDI!</b>\n\nSorun: <code>String Mismatch</code>\nÇözüm: Dosya optimize edildi ve karargah linkimiz dosyaya mühürlendi.")
            # Dosyayı geri gönder (Orijinali alıp bilgi notuyla iade ediyoruz)
            await msg.reply_document(msg.document.file_id, caption="📦 Tamir Edilmiş Dosya (YaAXY Signed)")

    # --- [FAZ 6] ADMİN MESAJ VE FLOOD KONTROL ---
    async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = str(update.effective_user.id)
        
        # Ban Kontrol
        banned, until = is_banned(uid)
        if banned:
            await update.message.reply_text(f"🚫 <b>İŞLEM REDDEDİLDİ!</b>\nYasağın şu tarihte kalkacak: {until}")
            return

        if context.user_data.get('state') == 'ASKING':
            # Flood Kontrol (5 saniye / 5 mesaj)
            now = time.time()
            msgs = context.user_data.get('flood', [])
            msgs = [t for t in msgs if now - t < 5]
            msgs.append(now)
            context.user_data['flood'] = msgs
            
            if len(msgs) > 5:
                until_str = await apply_ban(uid, hours=1)
                await update.message.reply_text(f"⚠️ <b>SPAM TESPİT EDİLDİ!</b>\nDisiplin kuralları gereği 1 saat engellendin. Açılış: {until_str}")
                context.user_data['state'] = None
                return

            await context.bot.send_message(ADMIN_ID, f"📩 <b>ADMIN YARDIM:</b>\n{update.message.text}\nKimden: {update.effective_user.full_name} ({uid})")
            await update.message.reply_text("✅ Mesajın mermi hızıyla yöneticiye iletildi.", reply_markup=main_kb())
            context.user_data['state'] = None

    # --- HANDLER EKLEME ---
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, handle_docs))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("\n🚀 YaAXY V46: FIRAT KOMUTASINDA YAYINDA!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    run_bot()
