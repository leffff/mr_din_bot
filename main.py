from telebot import types, apihelper
import telebot
from create_environment import create_environment
from os import getenv

# from db_creation import first_db_creation
# from all_models import User
from swear_words import russian_swear_words
from russian_word_db import RussianDataset

# first_db_creation()
create_environment()
rd = RussianDataset()
rd.download()

swearing = russian_swear_words()

TOKEN = getenv("TOKEN")
print(TOKEN)
PROXY = getenv("PROXY")
DBNAME = getenv("DBNAME")
USER = getenv("USER")
PASSWORD = getenv("PASSWORD")
PORT = getenv("PORT")
HOST = getenv("HOST")

apihelper.proxy = {
    'https': "socks5://167.172.55.204:1080"
}

status = {"tg_id": 0,
          "tg_nickname": "",
          "name": "",
          "surname": "",
          "qualification": "",
          "qualities": "",
          "experience": 0,
          "city": ""}

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['echo'])
def echo(message):
    ref_user = message.text
    print(message.from_user)
    bot.send_message(message.from_user.id, ref_user + " Связь с ботом установлена :)")


@bot.message_handler(commands=['start'])
def startMessage(message):
    bot.send_message(message.from_user.id, "Здравствуйте!\nЯ Vavacancy Bot, ваш личный помощник на рынке труда\nЧтобы ознакомиться с моим функционалом воспользуйтесь /help")


@bot.message_handler(commands=['help'])
def startMessage(message):
    id = message.from_user.id
    # user = User()
    # status = user.get_from_tg_id(id)
    print(status)
    bot.send_message(message.from_user.id,
                     "Я пока что ничего не умею, уж простите, но скоро навигация будет доступна")

    # if status == "user not found":
    #     bot.send_message(message.from_user.id, "Я много чего умею, но сначала Вам нужно зарегистрироваться!\nДля этог воспользуйтесть /register")
    # if status == "ok":
    #     bot.send_message(message.from_user.id, "/find_work\n/post_order\n/find_worker\n/view_tasks\nview_orders")


# @bot.message_handler(commands=['register'])
# def startMessage(message):
#     global status
#     status["tg_id"] = message.from_user.id
#     status["tg_nickname"] = message.from_user.username
#     status["name"] = message.from_user.name
#     status["surname"] = message.from_user.surname
#
#     print(status)
#
#
# @bot.message_handler(content_types=["text"])
# def buttons(message):
#     if message.text.lower() == "котики":
#         doc = open('котята.jpg', 'rb')
#         bot.send_photo(message.chat.id, doc, 'Какие красивые котята.')
#     elif message.text.lower() == "щенки":
#         doc = open('щенки.jpg', 'rb')
#         bot.send_photo(message.chat.id, doc, 'Какие красивые щенки.')
#     elif message.text == "Как дела?":
#         bot.send_message(message.chat.id, "Я - бот, у меня нет настроения.")
#     else:
#         keyboard = types.InlineKeyboardMarkup(True)
#         keyboard.add(types.InlineKeyboardButton("Котики", callback_data="kittens"),
#                      types.InlineKeyboardButton("Щенки", callback_data="puppies"))
#         bot.send_message(message.chat.id, "Управление ботом.", reply_markup=keyboard)
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def callbackButtons(call):
#     if call.data[:7] == 'kittens':
#         doc = open('котята.jpg', 'rb')
#         bot.send_photo(call.message.chat.id, doc, 'Какие красивые котята. Только с колбэком')
#     if call.data[:7] == 'puppies':
#         doc = open('щенки.jpg', 'rb')
#         bot.send_photo(call.message.chat.id, doc, 'Какие красивые щенки. Только с колбэком')

bot.polling(none_stop=True, timeout=123)

# try:
#     bot.infinity_polling(True)
# except Exception as e:
#     print(e)
