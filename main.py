import telebot
import json
import random
import os
from telebot import types

# ТОКЕН-ді осы жерге қой немесе Render Environment Variables-ке қосасың
TOKEN = "8898498557:AAFhfOwx6ouTwoL598shd4fqVEUTb0BYd04"
CHANNEL = "https://t.me/V1beGram"

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# JSON файлын оқу
def load_numbers():
    if not os.path.exists("numbers.json"):
        return []
    with open("numbers.json", "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

numbers = load_numbers()

def save_numbers():
    with open("numbers.json", "w", encoding="utf-8") as f:
        json.dump(numbers, f, indent=4, ensure_ascii=False)

@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    channel = types.InlineKeyboardButton("📢 Официальный канал V1beGram", url=CHANNEL)
    keyboard.add(channel)

    bot.send_message(
        message.chat.id,
        """
👋 <b>Добро пожаловать в V1beGram!</b>

🔐 Бот для получения номера и кода входа.

Команды:
📱 /getnumber — получить номер
🔐 /getcode — получить код
        """,
        reply_markup=keyboard
    )

@bot.message_handler(commands=["getnumber"])
def get_number(message):
    global numbers
    user_id = str(message.chat.id)

    # Жаңартып оқимыз
    numbers = load_numbers()

    for num in numbers:
        if num["user"] == user_id:
            bot.send_message(message.chat.id, f"⚠️ У вас уже есть номер:\n\n📱 <code>{num['number']}</code>")
            return

    free = [n for n in numbers if n["user"] is None]

    if not free:
        bot.send_message(message.chat.id, "❌ Свободных номеров нет.")
        return

    number = random.choice(free)
    number["user"] = user_id
    number["code"] = str(random.randint(10000, 99999))
    save_numbers()

    bot.send_message(
        message.chat.id,
        f"✅ <b>Ваш V1beGram номер:</b>\n\n📱 <code>{number['number']}</code>\n\nСохраните этот номер."
    )

@bot.message_handler(commands=["getcode"])
def get_code(message):
    user_id = str(message.chat.id)
    numbers = load_numbers()
    
    for num in numbers:
        if num["user"] == user_id:
            bot.send_message(message.chat.id, f"🔐 <b>Ваш код:</b> <code>{num['code']}</code>")
            return

    bot.send_message(message.chat.id, "❌ У вас нет номера. Используйте /getnumber")

print("Бот V1beGram запущен!")
bot.infinity_polling()
