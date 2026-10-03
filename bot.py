#!/usr/bin/env python3
import os
import threading
import telebot
from omnimind import OmniMind

TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN muhit o'zgaruvchisi topilmadi!")

bot = telebot.TeleBot(TOKEN)

# Baza bilan ishlash uchun qulf
db_lock = threading.Lock()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_id = str(message.from_user.id)
    
    with db_lock:
        # Har safar alohida obyekt ochamiz, shunda thread muammosi chiqmaydi
        app = OmniMind(db_path="omnimind.db")
        app.set_student(user_id)
        
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
    
    try:
        with db_lock:
            # Har bir xabar uchun yangi OmniMind ulanishi
            app = OmniMind(db_path="omnimind.db")
            app.set_student(user_id)
            answer, task = app.lesson(text)
            
        bot.reply_to(message, answer)
    except Exception as e:
        bot.reply_to(message, f"Xato yuz berdi: {e}")

if __name__ == "__main__":
    print("Telegram bot ishga tushmoqda...")
    bot.infinity_polling()
