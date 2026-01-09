from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Updater, Dispatcher, CommandHandler, ConversationHandler, MessageHandler, Filters
from conf import TOKEN, ADMIN, PASSWORD
import sqlite3
import random
import string

MENU_STATE, SEND_STATE, FORWARD_STATE, ADMIN_STATE = range(4)

def start(update, context):
	context.bot.sendChatAction(chat_id=update.message.from_user.id, action="typing")
	
	args = context.args
	rid = ''.join(args)
	
	if len(rid) == 0:
		user_id = update.message.from_user.id
		username = update.message.from_user.username
		
		connect = sqlite3.connect("user.db")
		cursor = connect.cursor()
		cursor.execute("""CREATE TABLE IF NOT EXISTS user_db(id INTEGER, username TEXT, random_id TEXT)""")
		
		data = cursor.execute("SELECT id FROM user_db WHERE id = ?", (user_id, )).fetchone()
		random_data = cursor.execute("SELECT random_id FROM user_db").fetchall()
		
		length = 7
		string_ = string.ascii_lowercase
		random_id = ''.join(random.choice(string_) for i in range(length))
		
		while random_id in random_data:
			random_id = ''.join(random.choice(string_) for i in range(length))
		
		if data is None:
			cursor.execute("INSERT INTO user_db(id, username, random_id) VALUES(?,?,?)", (user_id, username, random_id, ))
			context.bot.send_message(chat_id=ADMIN, text=f"🧾<b>Diqqat</b> <a href = 'tg://user?id={update.message.from_user.id}'>{update.message.from_user.first_name}</a> Botga🤖 /start Bosdi!\n<b>📡 Username:</b> @{update.message.from_user.username}\n<b>🆔️ Raqami:</b> <code>{update.message.from_user.id}</code>", parse_mode="HTML")
			connect.commit()
			
		user_data = cursor.execute("SELECT random_id FROM user_db WHERE id = ?", (user_id, )).fetchone()
		
		url = f"https://t.me/{context.bot.username}?start={user_data[0]}"
		update.message.reply_html(f"<b>Salom</b> <a href = 'tg://user?id={update.message.chat_id}'>{update.message.from_user.first_name}</a>👋!\n\n<b>Bu havola orqali sizga foydalanuvchilar anonim xabar yuborishi mumkin bo'ladi!</b>👇\n\n<b>Havola:</b> <pre>{url}</pre>\n\n<i>Agar botdan foydalanishni bilmasangiz yordam bo'limidan kerakli ma'lumotlar olishingiz mumkin</i> --> /help",
			reply_markup=InlineKeyboardMarkup([
					[
						InlineKeyboardButton("Ulashish♻️", url=f"https://t.me/share/url?url={url}"),
					],
			])
		)
		return MENU_STATE
		
	else:
		try:
			connect = sqlite3.connect("user.db")
			cursor = connect.cursor()
			
			global forid
			forid = cursor.execute("SELECT id FROM user_db WHERE random_id = ?", (rid, )).fetchone()
			
			update.message.reply_html("<b>Havola tasdiqlandi</b>, <i>hohlagan turdagi xabarlarni yuboringiz mumkin!</i>")
			
			return SEND_STATE
		except Exception:
			pass
	
def feedback(update, context):
	context.bot.sendChatAction(chat_id=update.message.from_user.id, action="typing")
	text = update.message.text
	
	connect = sqlite3.connect("user.db")
	cursor = connect.cursor()
	
	user_data = cursor.execute("SELECT random_id FROM user_db WHERE id = ?", (update.message.from_user.id, )).fetchone()
	url = f"https://t.me/{context.bot.username}?start={user_data[0]}"
	
	if text is None:
		context.bot.copyMessage(
			chat_id=forid[0],
			from_chat_id=update.message.from_user.id,
			message_id=update.message.message_id,
			caption=f"<b>Sizda yangi anonim xabar bor:</b>\n\n<b>{update.message.caption}</b>",
			parse_mode="HTML",
			reply_markup=InlineKeyboardMarkup([
				[
					InlineKeyboardButton("Javob yuborish♻️", url=f"{url}"),
				],
			])
		)

		update.message.reply_html("<b>Bajarildi</b>, <i>xabar yuborildi!</i>")
		update.message.reply_html(f"<i>Bu havola orqali sizga ham foydalanuvchilar anonim xabarlar yuborishi mumkin.</i>\n\n<b>Havola:</b> <pre>{url}</pre>",
			reply_markup=InlineKeyboardMarkup([
					[
						InlineKeyboardButton("Ulashish♻️", url=f"https://t.me/share/url?url={url}"),
					],
				])
		)
		return MENU_STATE
		
	else:
		context.bot.send_message(
			chat_id=forid[0],
			text=f"<b>Sizda yangi anonim xabar bor:</b>\n\n<b>{text}</b>",
			parse_mode="HTML",
			reply_markup=InlineKeyboardMarkup([
				[
					InlineKeyboardButton("Javob yuborish♻️", url=f"{url}"),
				],
			])
		)
			
		update.message.reply_html("<b>Bajarildi</b>, <i>xabar yuborildi!</i>")
		update.message.reply_html(f"<i>Bu havola orqali sizga ham foydalanuvchilar anonim xabarlar yuborishi mumkin.</i>\n\n<b>Havola:</b> <pre>{url}</pre>",
			reply_markup=InlineKeyboardMarkup([
				[
					InlineKeyboardButton("Ulashish♻️", url=f"https://t.me/share/url?url={url}"),
				],
			])
		)
		return MENU_STATE
	
def error(update, context):
	context.bot.sendChatAction(chat_id=update.message.from_user.id, action="typing")
	
	connect = sqlite3.connect("user.db")
	cursor = connect.cursor()
	
	user_data = cursor.execute("SELECT random_id FROM user_db WHERE id = ?", (update.message.from_user.id, )).fetchone()
	url = f"https://t.me/{context.bot.username}?start={user_data[0]}"
	
	update.message.reply_html(f"<b>Salom</b> <a href = 'tg://user?id={update.message.chat_id}'>{update.message.from_user.first_name}</a>👋!\n\n<b>Bu havola orqali sizga foydalanuvchilar anonim xabar yuborishi mumkin bo'ladi!</b>👇\n\n<b>Havola:</b> <pre>{url}</pre>\n\n<i>Agar botdan foydalanishni bilmasangiz yordam bo'limidan kerakli ma'lumotlar olishingiz mumkin</i> --> /help")

def stat(update, context):
	connect = sqlite3.connect("user.db")
	cursor = connect.cursor()
	
	data = cursor.execute("SELECT id FROM user_db").fetchall()
	user = len(data)
	update.message.reply_html(f"<b>📊 Statistika bo'limi:</b>\n\n<i>👤Activ:</i> <b>{user}</b> ta")
	
def help(update, context):
	context.bot.sendChatAction(chat_id=update.message.from_user.id, action="typing")
	update.message.reply_html("<b>Havoladan foydalanish:</b>\n\n<i>Havoladan foydalanish uchun havolani hohlagan ijtimoiy tarmoqlaringizga havolani joylashtiring havola orqali insonlar sizga o'z savollarini yuborishi mumkin bo'ladi.</i>\n\n<b>(Javob yuborish)</b> <i>tugmasi bilan esa sizga savol bergan odamga javob berishni bosib hohlagan tarzdagi xabarlarni yuborishingiz mumkin bo'ladi</i>")
	
def admin(update, context):
	args = context.args
	code = ''.join(args)
	
	if ADMIN == update.message.from_user.id or code == PASSWORD:
		update.message.reply_html("Xush kelibsiz admin!", 
		reply_markup=ReplyKeyboardMarkup([
			[
				KeyboardButton("📨Xabar yuborish"),
				KeyboardButton("📊Statistika"),
			],
			[
				KeyboardButton("🔝Bosh menu")
			],
		],resize_keyboard=True))
		return ADMIN_STATE
	else:
		return error(update, context)
	
def admin_text(update, context):
	text = update.message.text
	
	if text == "📨Xabar yuborish":
		update.message.reply_html("<i>Foylanuvchilarga hohlagan tarzdagi xabarni yuborishngiz mumkin!</i>", 
			reply_markup=ReplyKeyboardMarkup([
				[
					KeyboardButton("❌️Bekor qilish")
				],
				], resize_keyboard=True))
		return FORWARD_STATE
	
	elif text == "📊Statistika":
		return stat(update, context)
	
	elif text == "🔝Bosh menu":
		update.message.reply_html("<i>Bosh menudasiz!</i>", reply_markup=ReplyKeyboardRemove())
		return MENU_STATE
		
def forward(update, context):
	text = update.message.text
	
	connect = sqlite3.connect("user.db")
	cursor = connect.cursor()
	data = cursor.execute("SELECT id FROM login_id").fetchall()
	
	if text == "❌️Bekor qilish":
		return admin(update, context)
	else:
		for s in data:
			user = s[0]
			try:
				context.bot.copyMessage(
					chat_id=user,
					from_chat_id=ADMIN,
					message_id=update.message.message_id
				)
			except Exception as e:
				cursor.execute(f"DELETE FROM login_id WHERE id = {user}")
				connect.commit()
				
		update.message.reply_html("<i>Xabar yuborildi!</i>", reply_markup=ReplyKeyboardMarkup([
			[
				KeyboardButton("📨Xabar yuborish"),
				KeyboardButton("📊Statistika"),
			],
			[
				KeyboardButton("🔝Bosh menu")
			],
		],resize_keyboard=True))
			
		return ADMIN_STATE
	
def main():
	updater = Updater(TOKEN, use_context=True)
	
	updater.dispatcher.add_handler(ConversationHandler(
		entry_points = [
			CommandHandler("start", start),
			CommandHandler("help", help),
			CommandHandler("admin", admin),
		],
		states = {
			MENU_STATE: [
				CommandHandler("start", start),
				CommandHandler("stat", stat),
				CommandHandler("help", help),
				CommandHandler("admin", admin),
				MessageHandler(Filters.all, error),
			],
			SEND_STATE: [
				CommandHandler("start", start),
				MessageHandler(Filters.all, feedback),
			],
			ADMIN_STATE: [
				CommandHandler("start", start),
				MessageHandler(Filters.text, admin_text),
			],
			FORWARD_STATE: [
				MessageHandler(Filters.all, forward),
			]
		},
		fallbacks = [
			CommandHandler("start", start),
		],
	))
	
	updater.start_polling()
	updater.idle()
	
if __name__ == "__main__":
	main()