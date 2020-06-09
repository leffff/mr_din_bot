from telebot import types, apihelper
import telebot
from os import getenv
import time
from datetime import datetime

from create_environment import create_environment
from db_creation import first_db_creation
from all_models import User, Order
from swear_words import russian_swear_words
from russian_word_db import RussianDataset

create_environment()

TOKEN = getenv("TOKEN")
print(TOKEN, "TOKEN")
DBNAME = getenv("DBNAME")
print(DBNAME, "DBNAME")

first_db_creation()

swearings = russian_swear_words()

rd = RussianDataset()
rd.download()

bot = telebot.TeleBot(TOKEN)

employer_flag = False
mixed_flag = False


@bot.message_handler(commands=['echo'])
def echo(message):
    ref_user = message.text
    print(message.from_user)
    bot.send_message(message.from_user.id, ref_user + " Связь с ботом установлена :)")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id,
                     "Здравствуйте!\nЯ Vavacancy Bot, ваш личный помощник на рынке труда\nЧтобы ознакомиться с моим функционалом воспользуйтесь /help")


@bot.message_handler(commands=['help'])
def help(message):
    id = message.from_user.id
    user = User()
    status = user.get_from_tg_id(id)["status"]
    print(status)
    if status == "user not found":
        bot.send_message(message.from_user.id,
                         "Cначала Вам нужно зарегистрироваться!\nДля этог воспользуйтесть /register\n\n")
    elif status == "ok":
        bot.send_message(message.from_user.id, "/find_work\n/post_order\n/find_worker\n/view_tasks\n/view_orders")
    else:
        bot.send_message(message.from_user.id,
                         "Приносим извенения! Произошли неполадки! Мы уже работаем над их устранением")


@bot.message_handler(commands=['register'])
def register(message):
    keyboard = types.InlineKeyboardMarkup(True)
    keyboard.add(types.InlineKeyboardButton("РАБОТОДАТЕЛЬ", callback_data="employer"),
                 types.InlineKeyboardButton("РАБОТОДАТЕЛЬ И РАБОТНИК", callback_data="mixed"))
    bot.send_message(message.from_user.id,
                     "Если если вы хотите иметь только права работодателя (Ваш профиль не будет рекомендоваться при поиске работников)",
                     reply_markup=keyboard)


@bot.message_handler(content_types=["cabinet"])
def cabinet(message):
    pass


@bot.message_handler(content_types=["text"])
def text(message):
    id = message.from_user.id
    user = User()
    status = user.get_from_tg_id(id)["status"]
    sentence = message.text.split("\n")

    if status == "user not found":
        global employer_flag, mixed_flag
        registration = {"tg_id": message.from_user.id, "tg_nickname": message.from_user.username,
                        "name": sentence[0] if sentence[0].isalpha() else None,
                        "surname": sentence[1] if sentence[0].isalpha() else None,
                        "city": sentence[2] if sentence[0].isalpha() else None}

        if employer_flag:
            registration["qualification"] = "работодатель"
            registration["qualities"] = "работодатель"
            registration["experience"] = 0

        elif mixed_flag:
            registration["qualification"] = sentence[4]
            registration["qualities"] = sentence[5]

            start_date = sentence[6]
            if len(start_date) and start_date.isdigit() == 4:
                if int(start_date) > 1960 < datetime.today().year:
                    experience = f"01-01-{start_date} 00:00:00"
                    experience = time.strptime(experience, "%Y-%m-%d %H:%M:%S")
                    experience = int(time.mktime(experience))
                    registration["experience"] = experience
            else:
                registration["experience"] = None

        status = user.add_user(registration)["status"]
        print(status)
        error = ""
        if status == "invalid type for tg_nickname":
            error = "У вас нет имени пользователя.\n Перейдите в Setting, Edit profile и измените Usrname"
        if status == "invalid type for name":
            error = "Некорректно указано имя.\n Проверьте его написание (возномжно в нём присутствуют цифры)"
        if status == "invalid type for surname":
            error = "Некорректно указана фамилия.\n Проверьте её написание (возномжно в ней присутствуют цифры)"
        if status == "invalid type for city":
            error = "Некорректно указан город.\n Проверьте его написание (возномжно в нем присутствуют цифры)"
        if status == "invalid type for experience":
            error = "Убедитесь в том, что вы корректно указали год начала работы"

        if status == "ok":
            bot.send_message(message.chat.id, "Вы успешно зарегистрированы!")
        else:
            bot.send_message(message.chat.id, f"Введены некорректные данные!\n{error}")

    elif status == "ok":
        bot.send_message(message.chat.id, "Вы уже зарегистрированы!")

    else:
        bot.send_message(message.chat.id, "Возникли неполадки! Мы уеж работаем над их устранением!")


@bot.callback_query_handler(func=lambda call: True)
def callback_buttons(call):
    id = call.message.chat.id
    user = User()
    status = user.get_from_tg_id(id)["status"]
    if status == "user not found":
        global employer_flag, mixed_flag

        if call.data == 'employer':
            bot.send_message(call.message.chat.id,
                             "Для завершения регистрации отправьте сообщение в формате:\n\nИМЯ\nФАМИЛИЯ\nГОРОД ПРОЖИВАНИЯ")
            bot.send_message(call.message.chat.id, 'Работодатель')
            employer_flag = True
            mixed_flag = False

        elif call.data == 'mixed':
            bot.send_message(call.message.chat.id,
                             "Для завершения регистрации отправьте сообщение в формате:\n\nИМЯ\nФАМИЛИЯ\nГОРОД ПРОЖИВАНИЯ\nСПЕЦИАЛИЗАЦИЯ\nЛИЧНОСТНЫЕ КАЧЕСТВА\nДАТА НАЧАЛА РАБОТЫ (ГГГГ)")
            bot.send_message(call.message.chat.id, 'Работодатель и работник')
            mixed_flag = True
            employer_flag = False


if __name__ == '__main__':
    while True:
        try:
            print(datetime.now(), "UP")
            bot.polling(none_stop=True)
        except Exception as e:
            bot.stop_bot()
            print("RESTARTING BOT")
            time.sleep(10)
