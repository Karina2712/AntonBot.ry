import telebot
from telebot import types

# ✅ ID Антона (496910417)
ANTON_CHAT_ID = 496910417

# ✅ НОВЫЙ ТОКЕН (создайте у @BotFather!)
TOKEN = "8736224674:AAEJJNx15lVIANtSHzJApskOxC3YtGrC4ns"
bot = telebot.TeleBot(TOKEN)

user_waiting_question = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name or "Друг"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        types.KeyboardButton("🎨 Записаться на тату"),
        types.KeyboardButton("💬 Задать вопрос Антону"),
        types.KeyboardButton("ℹ️ Информация")
    )

    bot.reply_to(message, f"👋 Привет, {user_name}! Добро пожаловать!")
    bot.send_message(message.chat.id,
                     "Выбери действие снизу 😊",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name or "Пользователь"

    # Режим вопроса Антону
    if chat_id in user_waiting_question:
        question_text = f"💬 ВОПРОС ОТ {user_name} (@{message.from_user.username or 'no_username'}):\n\n{message.text}"

        try:
            bot.send_message(ANTON_CHAT_ID, question_text)
            bot.send_message(chat_id, "✅ Вопрос отправлен Антону! Скоро ответит.")
        except Exception as e:
            print(f"Ошибка отправки Антону: {e}")
            bot.send_message(chat_id,
                             "❌ Не удалось отправить Антону. "
                             "Напишите ему напрямую: @Antonkonturufa")

        del user_waiting_question[chat_id]
        return

    # Кнопки
    if message.text == "🎨 Записаться на тату":
        bot.reply_to(message, "📅 Напиши дату и время (15.03 14:00)")
    elif message.text == "💬 Задать вопрос Антону":
        user_waiting_question[chat_id] = user_name
        bot.reply_to(message, "❓ Напиши вопрос Антону:")
    elif message.text == "ℹ️ Информация":
        bot.reply_to(message,
                     "🏪 Антон - мастер тату 6+ лет\n"  # ✅ Исправлены кавычки
                     "📍 Уфа, Проспект Октября\n"
                     "   ориентир 'Семья'\n"
                     "⏰ График работы:когда душа пожелает(ваша или моя) 😏\n"
                     "💰 От 1500 руб/час")
    else:
        bot.reply_to(message, f"Ты написал: {message.text}")


if __name__ == "__main__":
    print("🚀 Бот запущен!")
    bot.infinity_polling(timeout=10)