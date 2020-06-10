from telebot import types, apihelper
import telebot
from os import getenv
import time
from datetime import datetime
import random

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
employer_only_flag = True


@bot.message_handler(commands=['echo'])
def echo(message):
    ref_user = message.text
    bot.send_message(message.from_user.id, ref_user + " Связь с ботом установлена :)")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id,
                     "Здравствуйте!\nЯ Vavacancy Bot, ваш личный помощник на рынке труда\nЧтобы ознакомиться с моим функционалом воспользуйтесь /help")


@bot.message_handler(commands=['fuck_me'])
def fuck_me(message):
    sent = random.choice(list(swearings))
    bot.send_message(message.from_user.id, f"{sent} ты")


@bot.message_handler(commands=['help'])
def help(message):
    status = user_in_db(message)
    if status == "user not found":
        bot.send_message(message.from_user.id,
                         "Cначала Вам нужно зарегистрироваться!\nДля этого воспользуйтесть /register\n\n")
    elif status == "ok":
        bot.send_message(message.from_user.id, "/find_work\n/post_order\n/find_worker\n/view_tasks\n/view_orders")
    else:
        bot.send_message(message.from_user.id,
                         "Приносим извенения! Произошли неполадки! Мы уже работаем над их устранением")


@bot.message_handler(commands=['register'])
def register(message):
    status = user_in_db(message)
    if status == "user not found":
        keyboard = types.InlineKeyboardMarkup(True)
        keyboard.add(types.InlineKeyboardButton("РАБОТОДАТЕЛЬ", callback_data="employer"),
                     types.InlineKeyboardButton("РАБОТОДАТЕЛЬ И РАБОТНИК", callback_data="mixed"))
        bot.send_message(message.from_user.id,
                         "Если если вы хотите иметь только права работодателя (Ваш профиль не будет рекомендоваться при поиске работников)",
                         reply_markup=keyboard)
    elif status == "ok":
        bot.send_message(message.from_user.id, "Вы уже зарегестрированны!")


@bot.message_handler(commands=["cabinet"])
def cabinet(message):
    print(message.text)
    status = user_in_db(message)
    print(status)
    if status == "user not found":
        bot.send_message(message.from_user.id,
                         "Cначала Вам нужно зарегистрироваться!\nДля этого воспользуйтесть /register\n\n")
    elif status == "ok":
        print(employer_only_flag, 11111111111)
        if employer_only_flag:
            user = User()
            user.get_from_tg_id(message.from_user.id)
            name = user.get_name()["out"]
            surname = user.get_surname()["out"]
            city = user.get_city()["out"]
            orders_status = user.watch_my_orders()["status"]
            if orders_status == "ok":
                orders = user.watch_my_orders()["out"]
                orders_str = f"Заказы({len(orders)}):"
                orders_str2 = [
                    f'{order_x.get_title()["out"]} ({"активный" if order_x.get_active()["out"] else "не активный"})' for
                    order_x in orders]
                orders_str2 = "\n".join(orders_str2)
                orders = f"{orders_str}\n{orders_str2}"
            elif orders_status == "no orders found":
                orders = "У вас ещё нет заказов"
            output = f"Имя - {name}\nФамилия - {surname}\nГород проживания - {city}\n{orders}"
            bot.send_message(message.from_user.id, output)
        else:
            user = User()
            user.get_from_tg_id(message.from_user.id)
            name = user.get_name()["out"]
            surname = user.get_surname()["out"]
            city = user.get_city()["out"]
            experience = user.get_experience()["out"]
            qulification = user.get_qualification()["out"]
            qualities = user.get_qualities()["out"]
            orders_status = user.watch_my_orders()["status"]
            if orders_status == "ok":
                orders = user.watch_my_orders()["out"]
                orders_str = f"Заказы({len(orders)}):"
                orders_str2 = [
                    f'{order_x.get_title()["out"]} ({"активный" if order_x.get_active()["out"] else "не активный"})' for
                    order_x in orders]
                orders_str2 = "\n".join(orders_str2)
                orders = f"{orders_str}\n{orders_str2}"
            if orders_status == "no orders found":
                orders = "У вас ещё нет заказов"
            works_status = user.watch_my_works()["status"]
            if works_status == "ok":
                works = user.watch_my_works()["out"]
                works_str = f"Работы({len(orders)}):"
                works_str2 = [
                    f'{work_x.get_title()["out"]} ({"активная" if work_x.get_active()["out"] else "не активная"})' for
                    work_x in works]
                works_str2 = "\n".join(works_str2)
                works = f"{works_str}\n{works_str2}"
            if works_status == "no works found":
                works = "У вас ещё нет работ"
            output = f"Имя - {name}\nФамилия - {surname}\nГород проживания - {city}\nОпыт работы - с {experience} года\nСпециализация - {qulification}\nЛичностные качества - {qualities}\n{orders}\n{works}"
            bot.send_message(message.from_user.id, output)

    else:
        bot.send_message(message.from_user.id,
                         "Приносим извенения! Произошли неполадки! Мы уже работаем над их устранением")


@bot.message_handler(content_types=["text"])
def text(message):
    if employer_flag or mixed_flag:
        out = registration_reply(message)
        bot.send_message(message.from_user.id, out)


@bot.callback_query_handler(func=lambda call: True)
def callback_buttons(call):
    id = call.message.chat.id
    user = User()
    status = user.get_from_tg_id(id)["status"]
    if status == "user not found":
        global employer_flag, mixed_flag, employer_only_flag

        if call.data == 'employer':
            bot.send_message(call.message.chat.id,
                             "Для завершения регистрации отправьте сообщение в формате:\n\nИМЯ\nФАМИЛИЯ\nГОРОД ПРОЖИВАНИЯ")
            bot.send_message(call.message.chat.id, 'Работодатель')
            employer_flag = True
            mixed_flag = False
            employer_only_flag = True

        elif call.data == 'mixed':
            bot.send_message(call.message.chat.id,
                             "Для завершения регистрации отправьте сообщение в формате:\n\nИМЯ\nФАМИЛИЯ\nГОРОД ПРОЖИВАНИЯ\nСПЕЦИАЛИЗАЦИЯ\nЛИЧНОСТНЫЕ КАЧЕСТВА\nДАТА НАЧАЛА РАБОТЫ (ГГГГ)")
            bot.send_message(call.message.chat.id, 'Работодатель и работник')
            mixed_flag = True
            employer_flag = False
            employer_only_flag = False


def registration_reply(message):
    status = user_in_db(message)
    sentence = message.text.split("\n")
    user = User()
    if len(sentence) == 3 or len(sentence) == 6:
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
                registration["qualification"] = sentence[3]
                registration["qualities"] = sentence[4]

                start_date = sentence[5]
                print(start_date)
                print(start_date.isdigit())
                if len(start_date) == 4 and start_date.isdigit():
                    print("ok 1")

                    if 1960 <= int(start_date) <= datetime.today().year:
                        registration["experience"] = int(start_date)
                else:
                    registration["experience"] = None
                print(registration["experience"])
            status = user.add_user(registration)["status"]
            print(status)
            error = ""
            if status == "invalid type for tg_nickname":
                error = "У вас нет имени пользователя.\n Перейдите в Setting, Edit profile и измените Username"
            if status == "invalid type for name":
                error = "Некорректно указано имя.\n Проверьте его написание (возномжно в нём присутствуют цифры)"
            if status == "invalid type for surname":
                error = "Некорректно указана фамилия.\n Проверьте её написание (возномжно в ней присутствуют цифры)"
            if status == "invalid type for city":
                error = "Некорректно указан город.\n Проверьте его написание (возномжно в нем присутствуют цифры)"
            if status == "invalid type for experience":
                error = "Убедитесь в том, что вы корректно указали год начала работы"

            if status == "ok":
                employer_flag = False
                mixed_flag = False
                return "Вы успешно зарегистрированы!\nДля дальнейших действий передите в /cabinet"
            else:
                return f"Введены некорректные данные!\n{error}"
        elif status == "ok":
            employer_flag = False
            mixed_flag = False
            return "Вы уже зарагестрированны"
        else:
            "Произошла ошибка, пожалуйста попробуйте позже"
    else:
        return "Проверьте, что ввели все данные"


def user_in_db(message):
    id = message.from_user.id
    user = User()
    status = user.get_from_tg_id(id)["status"]
    return status


if __name__ == '__main__':
    while True:
        try:
            print(datetime.now(), "UP")
            bot.polling(none_stop=True)
        except Exception as e:
            bot.stop_bot()
            print("RESTARTING BOT")
            time.sleep(10)
