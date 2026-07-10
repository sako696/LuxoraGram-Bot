import telebot
import json
import random
from telebot import types


TOKEN = "8898498557:AAFhfOwx6ouTwoL598shd4fqVEUTb0BYd04"

CHANNEL = "https://t.me/V1beGram"


bot = telebot.TeleBot(
    TOKEN,
    parse_mode="HTML"
)


with open("numbers.json", "r", encoding="utf-8") as f:
    numbers = json.load(f)



def save_numbers():
    with open(
        "numbers.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            numbers,
            f,
            indent=4,
            ensure_ascii=False
        )



@bot.message_handler(commands=["start"])
def start(message):

    keyboard = types.InlineKeyboardMarkup()

    channel = types.InlineKeyboardButton(
        "📢 Официальный канал V1beGram",
        url=CHANNEL
    )

    keyboard.add(channel)


    bot.send_message(
        message.chat.id,
        """
👋 <b>Добро пожаловать в V1beGram!</b>

🔐 Бот для получения номера и кода входа.

Команды:

📱 /getnumber — получить номер
🔐 /getcode — получить код

После получения данных войдите в приложение V1beGram.

        """,
        reply_markup=keyboard
    )



@bot.message_handler(commands=["getnumber"])
def get_number(message):

    user_id = str(message.chat.id)


    # Проверяем есть ли номер
    for num in numbers:

        if num["user"] == user_id:

            bot.send_message(
                message.chat.id,
                f"""
⚠️ У вас уже есть номер:

📱 <code>{num['number']}</code>
"""
            )

            return



    free = [
        n for n in numbers
        if n["user"] is None
    ]


    if not free:

        bot.send_message(
            message.chat.id,
            "❌ Свободных номеров нет."
        )

        return



    number = random.choice(free)


    number["user"] = user_id

    number["code"] = str(
        random.randint(10000,99999)
    )


    save_numbers()



    bot.send_message(
        message.chat.id,
        f"""
✅ <b>Ваш V1beGram номер:</b>

📱 <code>{number['number']}</code>

Сохраните этот номер.
Используйте его для входа в LuxoraGram.
"""
    )





@bot.message_handler(commands=["getcode"])
def get_code(message):

    user_id = str(message.chat.id)


    for num in numbers:


        if num["user"] == user_id:


            bot.send_message(
                message.chat.id,
                f"""
🔐 <b>Ваш код подтверждения:</b>

<code>{num['code']}</code>

Введите этот код в приложении V1beGram.
"""
            )

            return



    bot.send_message(
        message.chat.id,
        """
❌ У вас нет номера.

Сначала используйте:
 /getnumber
"""
    )





bot.infinity_polling()
