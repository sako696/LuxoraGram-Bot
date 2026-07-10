import telebot
import random
from telebot import types

TOKEN = "8898498557:AAFhfOwx6ouTwoL598shd4fqVEUTb0BYd04"
CHANNEL = "https://t.me/V1beGram"

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Пайдаланушылардың нөмірлері мен кодтарын уақытша сақтау
user_data = {}

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 <b>Добро пожаловать в V1beGram!</b>\n\n📱 /getnumber — получить номер\n🔐 /getcode — получить код"
    )

@bot.message_handler(commands=["getnumber"])
def get_number(message):
    user_id = message.chat.id
    
    # Жаңа нөмір мен код генерациялау
    random_part = "".join([str(random.randint(0, 9)) for _ in range(8)])
    new_number = f"+888{random_part}"
    new_code = str(random.randint(10000, 99999))
    
    # Деректерді есте сақтау
    user_data[user_id] = {"number": new_number, "code": new_code}
    
    bot.send_message(
        message.chat.id,
        f"✅ <b>Ваш номер:</b> <code>{new_number}</code>\n\n"
        "Теперь введите этот номер в приложении V1beGram и нажмите /getcode"
    )

@bot.message_handler(commands=["getcode"])
def get_code(message):
    user_id = message.chat.id
    
    # Егер адам әлі нөмір алмаған болса
    if user_id not in user_data:
        bot.send_message(message.chat.id, "❌ Сначала получите номер через /getnumber")
        return
    
    # Сақталған кодты көрсету
    code = user_data[user_id]["code"]
    bot.send_message(
        message.chat.id,
        f"🔐 <b>Ваш код подтверждения:</b> <code>{code}</code>\n\n"
        "Введите этот код в V1beGram."
    )

print("Бот V1beGram запущен!")
bot.infinity_polling()
