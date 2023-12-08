import telebot
from telebot import types
TOKEN = '6850746240:AAG83pP_oadyP8E0qRUBXRrqsCFyZ1RBLJA'
bot = telebot.TeleBot(TOKEN)

from questions import questions_by_category 
 

user_data = {}

def send_category_buttons(chat_id):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for category in questions_by_category.keys():
        markup.add(types.KeyboardButton(category))
    bot.send_message(chat_id, "Выберите категорию:", reply_markup=markup)

def send_question(chat_id, user_id):
    current_category = user_data[user_id]["category"]
    question_data = questions_by_category[current_category][user_data[user_id]["current_question"]]
    question_text = question_data["text"]
    options = question_data["options"]

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for option in options:
        markup.add(types.KeyboardButton(option))

    bot.send_message(chat_id, question_text, reply_markup=markup)

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    user_data[user_id] = {"current_question": 0, "score": 0}
    send_category_buttons(message.chat.id)

@bot.message_handler(func=lambda message: message.text in questions_by_category)
def handle_category(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {"current_question": 0, "score": 0}
    user_data[user_id]["category"] = message.text
    send_question(message.chat.id, user_id)

@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    user_id = message.from_user.id
    if user_id not in user_data or "category" not in user_data[user_id]:
        send_category_buttons(message.chat.id)
        return

    current_category = user_data[user_id]["category"]
    current_question = user_data[user_id]["current_question"]
    correct_option = questions_by_category[current_category][current_question]["correct_options"]

    if message.text == correct_option:
        user_data[user_id]["score"] += 1

    user_data[user_id]["current_question"] += 1
    if user_data[user_id]["current_question"] < len(questions_by_category[current_category]):
        send_question(message.chat.id, user_id)
    else:
        score = user_data[user_id]["score"]
        bot.send_message(message.chat.id, f"Игра завершена! Количество очков: {score}/{len(questions_by_category[current_category])}")

bot.polling()