from telebot import types
import telebot
from os import getenv
import time
from datetime import datetime

from create_environment import create_environment
from db_creation import first_db_creation
from all_models import User, Order

# from swear_words import russian_swear_words
# from russian_word_db import RussianDataset

# from ml_methods import activity_payment_rating, meaning_rating

create_environment()

TOKEN = getenv("TOKEN")
print(TOKEN, "TOKEN")
DBNAME = getenv("DBNAME")
print(DBNAME, "DBNAME")

first_db_creation()

# swearings = russian_swear_words()
# rd = RussianDataset()
# rd.download()

bot = telebot.TeleBot(TOKEN)

employer_flag, mixed_flag, create_order, find_worker, find_work = False, False, False, False, False
flags = [employer_flag, mixed_flag, create_order, find_worker, find_work]

CATEGORIES = {"design", "modeling", "gamedev", "web", "appdev", "db", "analisys", "arvr"}


def user_in_db(message):
    id = message.from_user.id
    user = User()
    status = user.get_from_tg_id(id)["status"]
    print(status)
    return status


def registration_reply(message):
    status = user_in_db(message)
    sentence = message.text.split("\n")
    user = User()

    if len(sentence) == 2 or len(sentence) == 5:
        if status == "user not found":
            global employer_flag, mixed_flag
            start_date = 0
            registration = {"tg_id": message.from_user.id, "tg_nickname": message.from_user.username}
            if not sentence[0].isalpha():
                return "Имя должно состоять только из букв"
            if not sentence[1].isalpha():
                return "Фамилия должна состоять только из букв"

            if employer_flag:
                registration["qualification"] = "работодатель"
                registration["qualities"] = "работодатель"
                start_date = 1960

            elif mixed_flag:
                registration["qualification"] = sentence[3]
                registration["qualities"] = sentence[4]

                start_date = sentence[5]
                if len(start_date) == 4 and start_date.isdigit():
                    if 1960 < int(start_date) or int(start_date) > datetime.today().year:
                        return f"Год начала работв не может быт меньшк 1960 и больше {datetime.today().year}"

            registration["experience"] = int(start_date)
            registration["name"] = sentence[0]
            registration["surname"] = sentence[1]
            status = user.add_user(registration)["status"]

            if status == "ok":
                employer_flag = False
                mixed_flag = False
                return "Вы успешно зарегистрированы!\nДля дальнейших действий передите в /cabinet"

        elif status == "ok":
            employer_flag = False
            mixed_flag = False
            return "Вы уже зарагестрированны"
        else:
            "Произошла ошибка, пожалуйста попробуйте позже"
    else:
        return "Проверьте, что ввели все данные"


@bot.message_handler(commands=["try_help"])
def try_help(message):
    # Эти параметры для клавиатуры необязательны, просто для удобства
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_my_orders = types.KeyboardButton(text="Мои заказы")
    button_my_works = types.KeyboardButton(text="Мои работы")
    button_find_work = types.KeyboardButton(text="Искать работу")
    button_worker = types.KeyboardButton(text="Искать работника")
    button_create_order = types.KeyboardButton(text="Создать заказ")
    keyboard.add(button_my_orders, button_my_works, button_find_work, button_worker, button_create_order)
    bot.send_message(message.from_user.id,
                     "Выберете одну из следующих команд",
                     reply_markup=keyboard)


@bot.message_handler(commands=['echo'])
def echo(message):
    ref_user = message.text
    bot.send_message(message.from_user.id, ref_user + " Связь с ботом установлена :)")


@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.from_user.id,
                     "Vavacancy bot - поможет вам, как начинающим фрилансерам наработать портфолио из работ и получить опыт, чтобы в дальнейшем вы смогли стать опытным работником.\n\n"
                     "Ключеваой особенностью является то, что работы будут выполняться абсолютно бесплатно, но условия взаимодействия работника с заказчиком будут максимально приближенны к реальным.\n\n"
                     "Если вы являетесь заказчиком, то припомощи нашего сервиса ваша работа будет выполнена абсолютно бесплатно.\n\n"
                     "Для того, чтобы посмотреть возможности бота передите в /help. \n\n"
                     "Перейдя в /rules вы познакомитесь с правилами пользования сервисом")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id,
                     "Здравствуйте!\n"
                     "Я Vavacancy Bot - сервис, где начинающие фрилансеры могут\n"
                     "наработать себе партфолио, а заказчики получить работу\n"
                     "абсолютно бесплатно. \n"
                     "Чтобы узнать больше обо мне воспользуйтесь /help")


@bot.message_handler(commands=['help'])
def help(message):
    status = user_in_db(message)
    print(status)
    if status == "user not found":
        bot.send_message(message.from_user.id,
                         "Cначала Вам нужно зарегистрироваться!\nДля этого воспользуйтесть /register\n\n")

    elif status == "ok":
        bot.send_message(message.from_user.id,
                         "Вы уже зарегистрированы!\nПоследgующая работа будет происходить через /cabinet")

    else:
        bot.send_message(message.from_user.id,
                         "Приносим извенения! Произошли неполадки! Мы уже работаем над их устранением")


@bot.message_handler(commands=['register'])
def register(message):
    status = user_in_db(message)

    if status == "user not found":
        keyboard = types.InlineKeyboardMarkup(True)
        keyboard.add(types.InlineKeyboardButton("РАБОТОДАТЕЛЬ", callback_data="employer"),
                     types.InlineKeyboardButton("РАБОТНИК", callback_data="mixed"))
        bot.send_message(message.from_user.id,
                         "Если если вы хотите иметь только права работодателя (Ваш профиль не будет рекомендоваться при поиске работников)",
                         reply_markup=keyboard)

    elif status == "ok":
        bot.send_message(message.from_user.id, "Вы уже зарегестрированны!")


@bot.message_handler(commands=["cabinet"])
def cabinet(message):
    status = user_in_db(message)

    if status == "user not found":
        bot.send_message(message.from_user.id,
                         "Cначала Вам нужно зарегистрироваться!\nДля этого воспользуйтесть /register")

    elif status == "ok":
        user = User()
        user.get_from_tg_id(message.from_user.id)
        print(user.get_qualities())
        if user.get_qualities()["out"] == "работодатель":

            name = user.get_name()["out"]
            surname = user.get_surname()["out"]

            output = f"Имя - {name}\nФамилия - {surname}"

            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
            button_my_orders = types.KeyboardButton(text="Мои заказы")
            button_worker = types.KeyboardButton(text="Искать работника")
            button_create_order = types.KeyboardButton(text="/add_order")
            keyboard.add(button_my_orders, button_worker, button_create_order)
            bot.send_message(message.from_user.id,
                             "Выберете одну из следующих команд",
                             reply_markup=keyboard)

            bot.send_message(message.from_user.id, output, reply_markup=keyboard)

        else:
            name = user.get_name()["out"]
            surname = user.get_surname()["out"]
            experience = user.get_experience()["out"]
            qulification = user.get_qualification()["out"]
            qualities = user.get_qualities()["out"]

            output = f"Имя - {name}\nФамилия - {surname}\nОпыт работы - с {experience} года\nСпециализация - {qulification}\nЛичностные качества - {qualities}"

            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
            button_my_orders = types.KeyboardButton(text="Мои заказы")
            button_my_works = types.KeyboardButton(text="Мои работы")
            button_find_work = types.KeyboardButton(text="Искать работу")
            button_worker = types.KeyboardButton(text="Искать работника")
            button_create_order = types.KeyboardButton(text="Создать заказ")
            keyboard.add(button_my_orders, button_my_works, button_find_work, button_worker, button_create_order)
            bot.send_message(message.from_user.id,
                             "Выберете одну из следующих команд",
                             reply_markup=keyboard)

            bot.send_message(message.from_user.id, output, reply_markup=keyboard)

    else:
        bot.send_message(message.from_user.id,
                         "Приносим извенения! Произошли неполадки! Мы уже работаем над их устранением")


@bot.message_handler(commands=["add_order"])
def add_order(message):
    status = user_in_db(message)
    print(status)
    if status == "ok":
        keyboard = types.InlineKeyboardMarkup(True)
        keyboard.add(types.InlineKeyboardButton("ДИЗАЙН", callback_data="design"),
                     types.InlineKeyboardButton("МОДЕЛТРОВАНИЕ", callback_data="modeling"),
                     types.InlineKeyboardButton("РАЗРАБОТКА ИГР", callback_data="gamedev"),
                     types.InlineKeyboardButton("WEB", callback_data="web"),
                     types.InlineKeyboardButton("РАЗРАБОТКА ПРИЛОЖЕНИЙ", callback_data="appdev"),
                     types.InlineKeyboardButton("БАЗЫ ДАННЫХ", callback_data="db"),
                     types.InlineKeyboardButton("АНАЛИТИКА", callback_data="analisys"),
                     types.InlineKeyboardButton("AR/VR", callback_data="arvr"))

        bot.send_message(message.from_user.id,
                         "Выберите категорию:", reply_markup=keyboard)

    elif status == "user not found":
        bot.send_message(message.from_user.id,
                         "Сначала Вам нужно зарегистрироваться!\nВоспользуйтесь /register")


@bot.message_handler(content_types=["text"])
def text(message):
    if employer_flag or mixed_flag:
        out = registration_reply(message)
        bot.send_message(message.from_user.id, out)

    elif create_order:
        out = add_order_reply(message)
        bot.send_message(message.from_user.id, out)

    elif find_worker:
        pass

    elif find_work:
        pass


@bot.callback_query_handler(func=lambda call: True)
def callback_buttons(call):
    id = call.message.chat.id
    user = User()
    status = user.get_from_tg_id(id)["status"]
    global employer_flag, mixed_flag, create_order, find_work, find_worker

    if status == "user not found":
        if call.data == 'employer':
            bot.send_message(call.message.chat.id,
                             "Для завершения регистрации отправьте сообщение в формате:\n\nИМЯ\nФАМИЛИЯ")
            bot.send_message(call.message.chat.id, 'Вы будете зарегистрированы, как работодатель')
            for i in range(len(flags)):
                flags[i] = False
            employer_flag = True


        elif call.data == 'mixed':
            bot.send_message(call.message.chat.id,
                             "Для завершения регистрации отправьте сообщение в формате:\n\nИМЯ\nФАМИЛИЯ\nСПЕЦИАЛИЗАЦИЯ\nЛИЧНОСТНЫЕ КАЧЕСТВА\nДАТА НАЧАЛА РАБОТЫ (ГГГГ)")
            bot.send_message(call.message.chat.id, 'Вы будете зарегистрированы, как работник')
            for i in range(len(flags)):
                flags[i] = False
            mixed_flag = True

    if status == "ok":
        if call.data in CATEGORIES:
            bot.send_message(call.message.chat.id,
                             "Для создания заказа отправьте сообщение в формате:\n\nНАЗВАНИЕ ЗАКАЗА\nДЛИТЕЛЬНОСТЬ ВЫПОЛНЕНИЯ В ДНЯХ\nОПИСАНИЕ ЗАКАЗА\n")

            for i in range(len(flags)):
                flags[i] = False
            create_order = True


def add_order_reply(message):
    status = user_in_db(message)
    sentence = message.text.split("\n")
    if status == "ok":
        order = Order()
        if len(sentence) >= 3:
            order_creation = {"employer_id": message.from_user.id}
            sentence[2] = sentence[2:]
            del sentence[3:]

            if len(sentence[0]) > 40 or len(sentence[0]) < 5:
                return "Длина названия должна быть больше 5 и меньше 40 символов"
            if not sentence[1].isdigit():
                return "Длитеольность выполнения заказа должна састоять только из цифр"
            if len(sentence[2]) < 30:
                return "Слишком короткое описание заказа(оно должно быть больше 30 символов)"

            order_creation["title"] = sentence[0]
            order_creation["time"] = sentence[1]
            order_creation["description"] = sentence[2]
            order_creation["category"] = ''
            status = order.add_order(order_creation)
            if status == "ok":
                return "Заказ успешно добавлен"


while True:
    try:
        print("BOT UP", str(datetime.now()).split(".")[0], sep="\t")
        bot.polling(none_stop=True)
    except Exception as e:
        bot.stop_bot()
        print("BOT DOWN", str(datetime.now()).split(".")[0], sep="\t")
