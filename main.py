from telebot import types
import telebot
from os import getenv
from datetime import datetime

from create_environment import create_environment
from db_creation import first_db_creation
from all_models import User, Order

from swear_words import russian_swear_words

swearings = russian_swear_words()

# from russian_word_db import RussianDataset

print("bbbb")
# rd = RussianDataset()
# rd.download()
print("aaaaaa")

from ml_methods import activity_time_rating, meaning_rating

create_environment()

TOKEN = getenv("TOKEN")
print(TOKEN, "TOKEN")
DBNAME = getenv("DBNAME")
print(DBNAME, "DBNAME")

first_db_creation()

bot = telebot.TeleBot(TOKEN)

employer_flag, mixed_flag, create_order, find_worker, find_work = False, False, False, False, False
flags = [employer_flag, mixed_flag, create_order, find_worker, find_work]

categories = {
    "Дизайн": False,
    "Моделирование": False,
    "Геймдев": False,
    "Веб": False,
    "Эпдев": False,
    "Базы данных": False,
    "Аналитика": False,
    "VR/AR": False
}


def censor_checker(phrase):
    for word in phrase.split():
        if word in swearings:
            return f"В заявке присутствует нецензурнач лексика: {word}"


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

    if len(sentence) == 2 or len(sentence) == 4:
        if status == "user not found":
            global employer_flag, mixed_flag
            start_date = 0
            registration = {"tg_id": message.from_user.id, "tg_nickname": message.from_user.username}

            if not sentence[0].isalpha():
                return "Имя должно состоять только из букв"
            censor_checker(sentence[0])

            if not sentence[1].isalpha():
                return "Фамилия должна состоять только из букв"
            censor_checker(sentence[1])

            if employer_flag:
                registration["qualification"] = "работодатель"
                registration["category"] = "работодатель"
                start_date = 1960

            elif mixed_flag:
                start_date = sentence[2]
                if len(start_date) == 4 and start_date.isdigit():
                    print(1960 < int(start_date), int(start_date) > datetime.today().year)
                    if 1960 > int(start_date) or int(start_date) > datetime.today().year:
                        return f"Год начала работв не может быт меньшк 1960 и больше {datetime.today().year}"

                censor_checker(sentence[2])
                registration["qualification"] = sentence[3]

                for i in range(len(list(categories.keys()))):
                    if list(categories.values())[i]:
                        print(list(categories.keys())[i])
                        registration["category"] = list(categories.keys())[i]

            registration["experience"] = int(start_date)
            registration["name"] = sentence[0]
            registration["surname"] = sentence[1]

            status = user.add_user(registration)["status"]
            if status == "ok":
                employer_flag = False
                mixed_flag = False

                for i in list(categories.keys()):
                    categories[i] = False

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


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id,
                     "Здравствуйте!\n"
                     "Я Mr. Din (Do It Now) - сервис, где начинающие фрилансеры могут "
                     "наработать себе партфолио, а заказчики получить работу "
                     "абсолютно бесплатно.\n"
                     "Чтобы узнать больше обо мне воспользуйтесь /help")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id,
                     "Я, Mr Din (Do It Now) - сервис, который поможет вам, как начинающим фрилансерам наработать портфолио из работ и получить опыт, чтобы в дальнейшем вы смогли стать опытными работниками.\n"
                     "Ключевой особенностью является то, что работы будут "
                     "выполняться абсолютно бесплатно, но условия взаимодействия "
                     "работника с заказчиком будут максимально приближенны к реальным.\n"
                     "Если вы являетесь заказчиком, то при помощи нашего сервиса ваша работа будет выполнена абсолютно бесплатно.\n\n"
                     "Команды по работе со мной:\n"
                     "/register - регистрация нового пользователя\n"
                     "/cabinet - просмотр вашего профиля\n"
                     "/my_orders - просмотр ваших заказов\n"
                     "/my_tasks - просмотр ваших работ\n"
                     "/add_orders - добавление нового заказа\n"
                     "/find_worker - поиск работника\n"
                     "/add_feedback - добавление отзыва и  оценка выполненной работы\n\n"
                     "Правила:\n"
                     "1. Чтобы завершить заказ заказчик должен вызвать /my_orders и ответить '+' (без ковычек) на соощение с нужным заказом.\n"
                     "2. При поиске работников/заказов для выбора закза/работника вам нужно ответьть '+' (без ковычек) на выбранное сообщение\n")


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

        if user.get_qualification()["out"] == "работодатель":

            name = user.get_name()["out"]
            surname = user.get_surname()["out"]

            output = f"Имя - {name}\nФамилия - {surname}"

            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
            button_my_orders = types.KeyboardButton(text="/my_orders")
            button_worker = types.KeyboardButton(text="/find_worker")
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
            qualification = user.get_qualification()["out"]

            output = f"Имя - {name}\nФамилия - {surname}\nОпыт работы - с {experience} года\nСпециализация - {qualification}\n"

            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
            button_my_orders = types.KeyboardButton(text="/my_orders")
            button_my_works = types.KeyboardButton(text="/my_works")
            button_find_work = types.KeyboardButton(text="/find_work")
            button_worker = types.KeyboardButton(text="/find_worker")
            button_create_order = types.KeyboardButton(text="/add_order")
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
        keyboard.add(types.InlineKeyboardButton("ДИЗАЙН", callback_data="Дизайн"),
                     types.InlineKeyboardButton("МОДЕЛТРОВАНИЕ", callback_data="Моделирование"),
                     types.InlineKeyboardButton("РАЗРАБОТКА ИГР", callback_data="Геймдев"),
                     types.InlineKeyboardButton("WEB", callback_data="Веб"),
                     types.InlineKeyboardButton("РАЗРАБОТКА ПРИЛОЖЕНИЙ", callback_data="Эпдев"),
                     types.InlineKeyboardButton("БАЗЫ ДАННЫХ", callback_data="Базы данных"),
                     types.InlineKeyboardButton("АНАЛИТИКА", callback_data="Аналитика"),
                     types.InlineKeyboardButton("AR/VR", callback_data="VR/AR"))

        bot.send_message(message.from_user.id,
                         "Выберите категорию:", reply_markup=keyboard)

    elif status == "user not found":
        bot.send_message(message.from_user.id,
                         "Сначала Вам нужно зарегистрироваться!\nВоспользуйтесь /register")


@bot.message_handler(commands=["my_orders"])
def my_orders(message):
    status = user_in_db(message)
    print(status)
    if status == "ok":
        user = User()
        user.get_from_tg_id(message.from_user.id)
        orders = user.watch_my_orders()
        print(orders)
        if orders["status"] == "ok":
            for i in orders["out"]:
                active = "да" if i.get_active()['out'] else "нет"
                if not i.get_active()['out']:
                    user = User()
                    id = i.get_worker_id()
                    user.get_user_by_id(id)
                    worker = f"\nНикнейм Работника: @{user.get_tg_nickname()}"
                else:
                    worker = ""
                bot.send_message(message.from_user.id,
                                 f"Название: {i.title}\nОписание: {i.get_description()['out']}\nПродолжительность: {i.get_time()['out']} дня\nАктивно: {active}{worker}")
                print(i)
        elif orders["status"] == "no orders found":
            bot.send_message(message.from_user.id, "У вас пока нет заказов.")
    else:
        bot.send_message(message.from_user.id, "Сначала Вам нужно зарегистрироваться!\nВоспользуйтесь /register")


@bot.message_handler(commands=["my_works"])
def my_works(message):
    status = user_in_db(message)
    print(status)
    if status == "ok":
        user = User()
        user.get_from_tg_id(message.from_user.id)
        if user.get_qualification() != "работодатель":
            orders = user.watch_my_works()
            if orders["status"] == "ok":
                for i in orders["out"]:
                    active = "да" if i.get_active()['out'] else "нет"
                    if not i.get_active()['out']:
                        if i.get_mark()["status"] == "ok":
                            mark = f"\nОценка: {i.get_mark()['out']}"
                            feedback = f"\nОтзыв: {i.get_feedback()['out']}"
                        else:
                            mark = ""
                            feedback = ""
                    else:
                        mark = ""
                        feedback = ""
                    user = User()
                    employer_id = i.get_employer_id()
                    user.get_user_by_id(employer_id)
                    employer = f"\nНикнейм Работодателя: @{user.get_tg_nickname()}"
                    bot.send_message(message.from_user.id,
                                     f"Название: {i.title}\nОписание: {i.get_description()['out']}\nПродолжительность: {i.get_time()['out']} дня\nАктивно: {active}{employer}\nКатегория: {i.get_category()['out']}{mark}{feedback}")
                    print(i)
            elif orders["status"] == "no works found":
                bot.send_message(message.from_user.id, "У вас пока нет работы.")
        else:
            bot.send_message(message.from_user.id,
                             "Вы не мождете просмотриеть свои работы, так как Вы зарегистрированы, как заказчик.")
    else:
        bot.send_message(message.from_user.id, "Сначала Вам нужно зарегистрироваться!\nВоспользуйтесь /register")


@bot.message_handler(commands=["find_work"])
def find_work(message):
    status = user_in_db(message)
    print(status)
    if status == "ok":
        user = User()
        user.get_from_tg_id(message.from_user.id)
        if user.get_qualification() != "работодатель":
            order = Order()
            print(order.get_all_orders())
        else:
            bot.send_message(message.from_user.id, "Вы не можете искать работу, так как вы являетесь работодателем.")
    else:
        bot.send_message(message.from_user.id, "Сначала Вам нужно зарегистрироваться!\nВоспользуйтесь /register")


@bot.message_handler(commands=["find_worker"])
def find_worker(message):
    status = user_in_db(message)
    print(status)
    if status == "ok":
        user = User()
        print(user.get_all_users())
    else:
        bot.send_message(message.from_user.id, "Сначала Вам нужно зарегистрироваться!\nВоспользуйтесь /register")


@bot.message_handler(content_types=["text"])
def text(message):
    global employer_flag, mixed_flag, create_order, find_worker, find_work
    if employer_flag or mixed_flag:
        print("REGISTRATION")
        out = registration_reply(message)
        bot.send_message(message.from_user.id, out)
        employer_flag, mixed_flag = False, False

    elif create_order:
        print("CREATE ORDER")
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
            keyboard = types.InlineKeyboardMarkup(True)
            keyboard.add(types.InlineKeyboardButton("ДИЗАЙН", callback_data="Дизайн"),
                         types.InlineKeyboardButton("МОДЕЛТРОВАНИЕ", callback_data="Моделирование"),
                         types.InlineKeyboardButton("РАЗРАБОТКА ИГР", callback_data="Геймдев"),
                         types.InlineKeyboardButton("WEB", callback_data="Веб"),
                         types.InlineKeyboardButton("РАЗРАБОТКА ПРИЛОЖЕНИЙ", callback_data="Эпдев"),
                         types.InlineKeyboardButton("БАЗЫ ДАННЫХ", callback_data="Базы данных"),
                         types.InlineKeyboardButton("АНАЛИТИКА", callback_data="Аналитика"),
                         types.InlineKeyboardButton("AR/VR", callback_data="VR/AR"))
            bot.send_message(call.message.chat.id,
                             "Выберите категорию своей специализации:", reply_markup=keyboard)

            for i in range(len(flags)):
                flags[i] = False
            mixed_flag = True

        elif call.data in list(categories.keys()):
            bot.send_message(call.message.chat.id,
                             "Для завершения регистрации отправьте сообщение в формате:\n\nИМЯ\nФАМИЛИЯ\nДАТА НАЧАЛА РАБОТЫ (ГГГГ)\nНАВЫКИ, ТЕХНОГОЛИИ И УМЕНИЯ")
            bot.send_message(call.message.chat.id, 'Вы будете зарегистрированы, как работник')
            categories[call.data] = True

    if status == "ok":
        if call.data in list(categories.keys()):
            bot.send_message(call.message.chat.id,
                             "Для создания заказа отправьте сообщение в формате:\n\nНАЗВАНИЕ ЗАКАЗА\nДЛИТЕЛЬНОСТЬ ВЫПОЛНЕНИЯ В ДНЯХ\nОПИСАНИЕ ЗАКАЗА\nТРЕБУЕМЫЕ КАЧЕСТВА И КВОЛИФИКАЦИИ ОТ РАБОТНИКА")
            categories[call.data] = True
            for i in range(len(flags)):
                flags[i] = False
            create_order = True


def add_order_reply(message):
    status = user_in_db(message)
    sentence = message.text.split("\n")
    print(status, "add_order_reply")
    if status == "ok":
        order = Order()
        if len(sentence) == 4:
            user = User()
            user.get_from_tg_id(message.from_user.id)
            order_creation = {"employer_id": user.get_user_id()["out"]}
            sentence[2] = "".join(sentence[2:])

            if len(sentence[0]) > 40 or len(sentence[0]) < 5:
                return "Длина названия должна быть больше 5 и меньше 40 символов"
            censor_checker(sentence[0])
            if not sentence[1].isdigit():
                return "Длитеольность выполнения заказа должна састоять только из цифр"
            censor_checker(sentence[1])
            if len(sentence[2]) < 30:
                return "Слишком короткое описание заказа(оно должно быть больше 30 символов)"
            censor_checker(sentence[2])

            order_creation["title"] = sentence[0]
            order_creation["time"] = int(sentence[1])
            order_creation["description"] = sentence[2]

            for i in range(len(list(categories.keys()))):
                if list(categories.values())[i]:
                    print(list(categories.keys())[i])
                    order_creation["category"] = list(categories.keys())[i]

            censor_checker(sentence[3])
            order_creation["worker_skills"] = sentence[3]

            status = order.add_order(order_creation)["status"]
            print(status, "get od status")
            if status == "ok":
                return "Заказ успешно добавлен"

            for i in list(categories.keys()):
                categories[i] = False
        else:
            return "Провьрьте, указали ли вы все требуемые данные!"


try:
    print("BOT UP", str(datetime.now()).split(".")[0], sep="\t")
    bot.polling(none_stop=True)
except Exception as e:
    bot.stop_bot()
    print("BOT DOWN", str(datetime.now()).split(".")[0], sep="\t")
