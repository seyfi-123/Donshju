#!/usr/bin/env python3
import os
import telebot
from omnimind import OmniMind

TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN muhit o'zgaruvchisi topilmadi!")

bot = telebot.TeleBot(TOKEN)
app = OmniMind(db_path="omnimind.db")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    app.set_student(str(message.from_user.id))
    bot.reply_to(message, f"Salom! OmniMind AI botiga xush kelibsiz. Sizning Chat ID raqamingiz: {chat_id}\nSavolingizni yozishingiz mumkin.")

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "🤖 **OmniMind Bot Buyruqlari:**\n"
        "/start - Botni ishga tushirish\n"
        "/help - Yordam olish\n"
        "Shunchaki istalgan savolingizni yozing, AI javob beradi!"
    )
    bot.reply_to(message, help_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = str(message.from_user.id)
    text = message.text
    app.set_student(user_id)
    
    try:
        answer, task = app.lesson(text)
        bot.reply_to(message, answer)
    except Exception as e:
        bot.reply_to(message, f"Xato yuz berdi: {e}")

if __name__ == "__main__":
    print("Telegram bot ishga tushmoqda...")
    # SQLite xatosini oldini olish uchun threaded=False qo'shildi
    bot.infinity_polling(threaded=False)
