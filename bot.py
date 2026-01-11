import telebot

TOKEN = '8115346441:AAFsNtu23eDXKfStxYzZJF3D1x6ZF7Cba0Q'
ADMIN_ID = 8186244653

bot = telebot.TeleBot(TOKEN)

user_data = {}
attempts = {}

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Вітаю!\n"
        "Це бот для подачі заявки в PUBG-клан.\n\n"
        "Щоб почати — напиши /apply"
    )

# /apply
@bot.message_handler(commands=['apply'])
def apply(message):
    user_data[message.chat.id] = {}
    attempts[message.chat.id] = {"age": 0}
    bot.send_message(message.chat.id, "🎮 Напиши свій нік у PUBG:")
    bot.register_next_step_handler(message, get_nick)

def reset_application(chat_id):
    user_data.pop(chat_id, None)
    attempts.pop(chat_id, None)

def get_nick(message):
    user_data[message.chat.id]['nick'] = message.text
    bot.send_message(message.chat.id, "📅 Скільки тобі років?")
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    chat_id = message.chat.id
    attempts[chat_id]["age"] += 1

    if not message.text.isdigit():
        return age_error(message)

    age = int(message.text)

    if age < 13 or age > 50:
        return age_error(message)

    user_data[chat_id]['age'] = age
    bot.send_message(chat_id, "🔥 Напиши свій KD (тільки цифри, можна з крапкою):")
    bot.register_next_step_handler(message, get_kd)

def age_error(message):
    chat_id = message.chat.id
    if attempts[chat_id]["age"] >= 2:
        bot.send_message(
            chat_id,
            "❌ Два рази неправильний вік.\n"
            "Заявку скинуто. Напиши /apply щоб почати знову."
        )
        reset_application(chat_id)
    else:
        bot.send_message(
            chat_id,
            "❗ Помилка.\n"
            "Вік має бути від 13 до 50 років.\n"
            "Спробуй ще раз:"
        )
        bot.register_next_step_handler(message, get_age)

def get_kd(message):
    text = message.text.replace(".", "", 1)

    if not text.isdigit():
        bot.send_message(
            message.chat.id,
            "❗ Помилка.\n"
            "KD має містити ТІЛЬКИ цифри.\n"
            "Спробуй ще раз:"
        )
        bot.register_next_step_handler(message, get_kd)
        return

    user_data[message.chat.id]['kd'] = message.text
    bot.send_message(message.chat.id, "⏱ Скільки годин на день граєш? (тільки цифри)")
    bot.register_next_step_handler(message, get_hours)

def get_hours(message):
    if not message.text.isdigit():
        bot.send_message(
            message.chat.id,
            "❗ Помилка.\n"
            "Кількість годин — тільки цифри.\n"
            "Спробуй ще раз:"
        )
        bot.register_next_step_handler(message, get_hours)
        return

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

    bot.send_message(ADMIN_ID, text)

    bot.send_message(
        message.chat.id,
        "✅ Заявку відправлено!\n"
        "Адміністратор розгляне її найближчим часом."
    )

    reset_application(message.chat.id)

# запуск
bot.polling(none_stop=True)
