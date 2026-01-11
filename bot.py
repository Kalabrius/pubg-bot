import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = telebot.TeleBot(TOKEN)

user_data = {}

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Вітаю!\n"
        "Це бот для подачі заявки в PUBG-клан.\n\n"
        "Щоб подати заявку — напиши /apply"
    )

# /apply
@bot.message_handler(commands=['apply'])
def apply(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "🎮 Напиши свій нік у PUBG:")
    bot.register_next_step_handler(message, get_nick)

def get_nick(message):
    user_data[message.chat.id]['nick'] = message.text
    bot.send_message(message.chat.id, "📅 Скільки тобі років?")
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    user_data[message.chat.id]['age'] = message.text
    bot.send_message(message.chat.id, "🔥 Напиши свій KD:")
    bot.register_next_step_handler(message, get_kd)

def get_kd(message):
    user_data[message.chat.id]['kd'] = message.text
    bot.send_message(message.chat.id, "⏱ Скільки годин на день граєш?")
    bot.register_next_step_handler(message, get_hours)

def get_hours(message):
    user_data[message.chat.id]['hours'] = message.text

    data = user_data[message.chat.id]

    text = (
        "📥 НОВА ЗАЯВКА В PUBG-КЛАН\n\n"
        f"👤 Користувач: @{message.from_user.username}\n"
        f"🎮 Нік: {data['nick']}\n"
        f"📅 Вік: {data['age']}\n"
        f"🔥 KD: {data['kd']}\n"
        f"⏱ Годин/день: {data['hours']}"
    )

    # надсилаємо заявку тобі
    bot.send_message(ADMIN_ID, text)

    # відповідь гравцю
    bot.send_message(
        message.chat.id,
        "✅ Заявку відправлено!\n"
        "Адміністратор розгляне її найближчим часом."
    )

    # очищаємо дані
    user_data.pop(message.chat.id, None)

# запуск
bot.polling(none_stop=True)

