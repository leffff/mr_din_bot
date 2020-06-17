import time
from os.path import join

from gensim.models.keyedvectors import Word2VecKeyedVectors
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
from telebot import types
import telebot
from os import getenv, getcwd
from datetime import datetime

from create_environment import create_environment
from db_creation import first_db_creation
from all_models import User, Order

from swear_words import russian_swear_words

swearings = russian_swear_words()

from russian_word_db import RussianDataset

# print("Downloading datasets")
# rd = RussianDataset()
# rd.download()
# print("Downloading finished")

path = join("/".join(getcwd().split("/")) + "/ml/russian_database")
print(path)
model = Word2VecKeyedVectors.load(path)
STOPWORDS = stopwords.words("russian")
for word in STOPWORDS:
    try:
        swearings.remove(word)
    except KeyError:
        pass
index2word_set = set(model.index2word)
moprh = MorphAnalyzer()

from ml_methods import activity_time_rating, meaning_rating

create_environment()

TOKEN = getenv("TOKEN")
print(TOKEN, "TOKEN")
DBNAME = getenv("DBNAME")
print(DBNAME, "DBNAME")

first_db_creation()

# apihelper.proxy = {
#     'https': "socks5://141.101.11.188:19847"
# }

bot = telebot.TeleBot(TOKEN)

employer_flag, mixed_flag, create_order_f, find_worker_f, find_work_f, hire_f, my_orders_f = False, False, False, False, False, False, False
flags = [employer_flag, mixed_flag, create_order_f, find_worker_f, find_work_f, hire_f]
task = ""

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
        if word.lower() in swearings:
            return f'В заявке присутствует нецензурная лексика: "{word}".\nВоспользуйтесь коммандой заново.'
    return ""


# def announcement():
#     user = User()
#     ids = user.get_all_tg_ids()["out"]
#     print(ids)
#     for i in ids:
#         try:
#             print(i[0])
#             bot.send_message(i[0], "Вышла новая версия @mr_din_bot !\nСпешите опробовать! Все функции готовы!")
#         except Exception:
#             pass
#
#
# announcement()


def user_in_db(message):
    id = message.from_user.id
    user = User()
    status = user.get_from_tg_id(id)["status"]
    return status


def registration_reply(message):
    status = user_in_db(message)
    sentence = message.text.split("\n\n")
    user = User()

    if len(sentence) == 2 or len(sentence) == 4:
        global flags
        if status == "user not found":

            start_date = 0
            registration = {"tg_id": message.from_user.id, "tg_nickname": message.from_user.username}

            if not sentence[0].isalpha():
                return "Имя должно состоять только из букв.\nВоспользуйтесь коммандой /register заново."
            if len(censor_checker(sentence[0])) != 0:
                return censor_checker(sentence[0])

            if not sentence[1].isalpha():
                return "Фамилия должна состоять только из букв.\nВоспользуйтесь коммандой /register заново."
            if len(censor_checker(sentence[1])) != 0:
                return censor_checker(sentence[1])

            if flags[0]:
                registration["qualification"] = "работодатель"
                registration["category"] = "работодатель"
                start_date = 1960

            elif flags[1]:
                start_date = sentence[2]
                if len(start_date) == 4 and start_date.isdigit():
                    if 1960 > int(start_date) or int(start_date) > datetime.today().year:
                        return f"Год начала работв не может быт меньшк 1960 и больше {datetime.today().year}.\nВоспользуйтесь коммандой /register заново."
                else:
                    return "Введите корректную дату.\nВоспользуйтесь коммандой /register заново."
                if len(censor_checker(sentence[2])) != 0:
                    return censor_checker(sentence[2])

                if len(censor_checker(sentence[3])) != 0:
                    return censor_checker(sentence[3])
                registration["qualification"] = sentence[3]

                for i in range(len(list(categories.keys()))):
                    if list(categories.values())[i]:
                        registration["category"] = list(categories.keys())[i]

            registration["experience"] = int(start_date)
            registration["name"] = sentence[0]
            registration["surname"] = sentence[1]

            status = user.add_user(registration)["status"]
            print(status)
            if status == "ok":
                flags[0] = False
                flags[1] = False
                for i in list(categories.keys()):
                    categories[i] = False

                return "Вы успешно зарегистрированы!\nДля дальнейших действий передите в /help."
            else:
                return "Проверьте, правильно ли Вы ввели все данные.\nВоспользуйтесь коммандой /register заново."
        elif status == "ok":
            flags[0] = False
            flags[1] = False
            return "Вы уже зарагестрированны"
        else:
            "Произошла ошибка, пожалуйста попробуйте позже"
    else:
        return "Проверьте, что ввели все данные!.\nВоспользуйтесь коммандой /register заново.\n\nPS: Используйте Shift + Enter чтобы перенести курсор на следующую строчку, если вы работаете с компьютера."


@bot.message_handler(commands=['echo'])
def echo(message):
    ref_user = message.text
    bot.send_message(message.from_user.id, ref_user + " Связь с ботом установлена :)")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id,
                     "Здравствуйте!\n"
                     "Я Mr. Din - сервис, где начинающие фрилансеры могут "
                     "наработать себе партфолио, а заказчики получить работу "
                     "абсолютно бесплатно. Do It Now.\n"
                     "Чтобы узнать больше обо мне воспользуйтесь /help")


@bot.message_handler(commands=['help'])
def help(message):
    print("help", message)
    bot.send_message(message.from_user.id,
                     "Я, Mr Din - сервис, который поможет вам, как начинающим фрилансерам наработать портфолио из работ и получить опыт, чтобы в дальнейшем вы смогли стать опытными работниками.\n"
                     "Ключевой особенностью является то, что работы будут "
                     "выполняться абсолютно бесплатно, но условия взаимодействия "
                     "работника с заказчиком будут максимально приближенны к реальным.\n"
                     "Если вы являетесь заказчиком, то при помощи нашего сервиса ваша работа будет выполнена абсолютно бесплатно. Do It Now.\n\n"
                     "Команды по работе со мной:\n"
                     "/register - регистрация нового пользователя\n"
                     "/cabinet - просмотр вашего профиля\n"
                     "/my_orders - просмотр ваших заказов\n"
                     "/my_works - просмотр ваших работ\n"
                     "/add_order - добавление нового заказа\n"
                     "/find_worker - поиск работника\n"
                     "/find_work - поиск работы\n\n"
                     "Правила:\n"
                     "1. Чтобы завершить заказ заказчик должен вызвать /my_orders и следовать указаниям.\n"
                     "2. При поиске работников/заказов для выбора закза/работника вам нужно ответьть '+' (без ковычек) на выбранное сообщение\n")


@bot.message_handler(commands=['register'])
def register(message):
    print("register", message)
    status = user_in_db(message)

    if status == "user not found":
        keyboard = types.InlineKeyboardMarkup(True)
        keyboard.add(types.InlineKeyboardButton("РАБОТОДАТЕЛЬ", callback_data="employer"),
                     types.InlineKeyboardButton("РАБОТНИК", callback_data="mixed"))
        bot.send_message(message.from_user.id,
                         "Если если вы хотите иметь только права работодателя (Ваш профиль не будет рекомендоваться при поиске работников)",
                         reply_markup=keyboard)

    elif status == "ok":
        bot.send_message(message.from_user.id, "Вы уже зарегестрированны!\nДля дальнейших действий передите в /help.")


@bot.message_handler(commands=["cabinet"])
def cabinet(message):
    print(message)
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

            output = f'*Имя* - {name}\n*Фамилия* - {surname}'

        else:
            name = user.get_name()["out"]
            surname = user.get_surname()["out"]
            experience = user.get_experience()["out"]
            categories = user.get_category()["out"]
            qualification = user.get_qualification()["out"]
            print(user.get_avg_mark())
            mark = user.get_avg_mark()["out"]

            output = f'*Имя* - {name}\n\n*Фамилия* - {surname}\n\n*Рейтинг:* {mark}/10\n\n*Опыт работы* - с {experience} года\n\n*Область* - {categories}\n\n*Умения, навыки* - {qualification}'
        bot.send_message(message.from_user.id, output, parse_mode="Markdown")
        bot.send_message(message.from_user.id, "Для дальнейших действий передите в /help.")

    else:
        bot.send_message(message.from_user.id,
                         "Приносим извенения! Произошли неполадки! Мы уже работаем над их устранением")
        bot.send_message(message.from_user.id, "Для дальнейших действий передите в /help.")


@bot.message_handler(commands=["add_order"])
def add_order(message):
    print(message)
    status = user_in_db(message)
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
    print(message)
    status = user_in_db(message)
    if status == "ok":
        user = User()
        user.get_from_tg_id(message.from_user.id)
        orders = user.watch_my_orders()
        if orders["status"] == "ok":
            bot.send_message(message.from_user.id,
                             "Чтобы закончить заказ, ответьте на сообщение с выбранным заказом в следующем формате:\n\n'+' или '-' (без ковычек, '+' если успешно, '-' если неуспешно)\n\nОЦЕНКА (от 0 до 10)\n\nОТЗЫВ О РАБОТНИКЕ")
            for i in orders["out"]:
                print(i, "order my")
                print(i.get_active()["status"])
                active = "да" if i.get_active()['status'] == "ok" else "нет"
                if i.get_worker_id()['status'] == "ok":
                    user1 = User()
                    id = i.get_worker_id()["out"]
                    user = user1.get_user_by_id(id)["out"]
                    worker = f"\n\nРаботник: @{user.get_tg_nickname()['out']}"
                else:
                    worker = "\n\nРаботник: --------------"
                print(i.get_description())
                print(i.get_time())
                print(i.get_worker_skills())
                print(i.get_category())
                bot.send_message(message.from_user.id,
                                 f"Название: {i.title}\n\nОписание: {i.get_description()['out']}\n\nПродолжительность: {i.get_time()['out']} дня\n\nТребуемые навыки: {i.get_worker_skills()['out']}\n\nКатегория заказа: {i.get_category()['out']}\n\nАктивно: {active}{worker}",)
                global my_orders_f, flags
                for i in range(len(flags)):
                    flags[i] = False
                my_orders_f = True
            bot.send_message(message.from_user.id, "Для дальнейших действий передите в /help.")
        elif orders["status"] == "no orders found":
            bot.send_message(message.from_user.id,
                             "У вас пока нет заказов.\nДля добавления заказа передите в /add_order.")
    else:
        bot.send_message(message.from_user.id, "Сначала Вам нужно зарегистрироваться!\nВоспользуйтесь /register")


@bot.message_handler(commands=["my_works"])
def my_works(message):
    print(message)
    status = user_in_db(message)
    if status == "ok":
        user = User()
        user.get_from_tg_id(message.from_user.id)
        if user.get_qualification() != "работодатель":
            orders = user.watch_my_works()
            if orders["status"] == "ok":
                for i in orders["out"]:
                    active = "да" if i.get_active()['status'] == "ok" else "нет"
                    if i.get_active()['status'] == "order finished":
                        if i.get_mark()["status"] == "ok":
                            mark = f"\n\nОценка: {i.get_mark()['out']}/10"
                            feedback = f"\n\nОтзыв: {i.get_feedback()['out']}"
                        else:
                            mark = ""
                            feedback = ""
                    else:
                        mark = ""
                        feedback = ""
                    user = User()
                    employer_id = i.get_employer_id()["out"]
                    print(employer_id)
                    employer1 = user.get_user_by_id(employer_id)["out"]
                    print(employer1)
                    employer = f"\n\nРаботодатель: @{employer1.get_tg_nickname()['out']}"
                    bot.send_message(message.from_user.id,
                                     f"Название: {i.title}\n\nОписание: {i.get_description()['out']}\n\nПродолжительность: {i.get_time()['out']} дня\n\nАктивно: {active}{employer}\n\nКатегория: {i.get_category()['out']}{mark}{feedback}")
                bot.send_message(message.from_user.id, "Для дальнейших действий передите в /help.")
            elif orders["status"] == "no works found":
                bot.send_message(message.from_user.id,
                                 "У вас пока нет работ. Для поиска работы парейдите в /find_work.")
        else:
            bot.send_message(message.from_user.id,
                             "Вы не мождете просмотриеть свои работы, так как Вы зарегистрированы, как заказчик.")
            bot.send_message(message.from_user.id, "Для дальнейших действий передите в /help.")
    else:
        bot.send_message(message.from_user.id, "Сначала Вам нужно зарегистрироваться!\nВоспользуйтесь /register")


@bot.message_handler(commands=["find_work"])
def find_work(message):
    print(message)
    status = user_in_db(message)
    if status == "ok":
        user = User()
        user.get_from_tg_id(message.from_user.id)
        if user.get_qualification() != "работодатель":
            order = Order()
            call = order.get_all_orders(user.get_category()["out"], user.get_user_id()["out"])
            if call["status"] == "ok":
                raw_data = call["out"]
                s = meaning_rating.Similarity(model, index2word_set)
                mean_sorter = lambda x: s.sim([x[6], user.get_qualification()["out"]])

                data = sorted(raw_data, key=mean_sorter)

                work = tuple(
                    f"Заказчик: @{User().get_user_by_id(i[1])['out'].get_tg_nickname()['out']}\n\nНазвание: {i[3]}\n\nОписание: {i[4]}\n\nКатегория: {i[5]}\n\nНавыки: {i[6]}\n\nВремя на выполнение: {i[10]}"
                    for i in data)
                bot.send_message(message.from_user.id,
                                 "Чтобы начать выполнение заказа ответьте на выбранный заказ '+' (без ковычек).")
                for i in work:
                    bot.send_message(message.from_user.id, i)
                global flags
                for i in range(len(flags)):
                    flags[i] = False
                flags[4] = True
                print(flags[4], "flllllllaaaags[4]")

            else:
                bot.send_message(message.from_user.id,
                                 "Нет подходящих заказов")
                bot.send_message(message.from_user.id, "Для дальнейших действий передите в /help.")
        else:
            bot.send_message(message.from_user.id, "Вы не можете искать работу, так как вы являетесь работодателем.")
            bot.send_message(message.from_user.id, "Для дальнейших действий передите в /help.")
    else:
        bot.send_message(message.from_user.id, "Сначала Вам нужно зарегистрироваться!\nВоспользуйтесь /register")


def hire(message):
    print(message)
    if message.reply_to_message is not None:
        if message.text == "+":
            tg_nickname = message.reply_to_message.text[11:].split("\n")[0]
            global task
            user = User().get_user_by_nickname(tg_nickname)["out"]
            bot.send_message(user.tg_id,
                             f"Пользователь @{message.from_user.username} предлагает Вам работу!\nОтветьте /agree на следующее сообщение, если вы принимаетет предложение.")
            bot.send_message(user.tg_id, task)
            return "Ваше предложение успешно отправлено! Ждите ответа."


def work_application(message):
    print(message)
    if message.reply_to_message is not None:
        if message.text == "+":

            order = Order()
            out = order.get_by_title(message.reply_to_message.text.split("\n\n")[1].split(": ")[1])
            print(out, "aaaaaaaeeeeeennnnnnnnn")
            worker = User()
            worker.get_from_tg_id(message.from_user.id)
            out = order.take_task(worker.get_user_id()["out"], time.time())["status"]
            if out == "ok":
                user = User()
                bot.send_message(user.get_user_by_id(order.get_employer_id()["out"])["out"].tg_id, f"Работник приступил к выполнению заказа! Под названием '{order.title}', Работник: @{message.from_user.username}")
                return "Вы приступили к выполнению задания! Удачи!\nДля дальнейших действий передите в /help. "
            return "Я устал, дайте отдохнуть!"
        else:
            return "Извините, я вас не понимаю."


def appropriate_workers(message):
    print(message.text, "1234567890987654321")
    print(message.reply_to_message, "жжжжжжжжжжжжжжжжжжжжжжжж")
    if message.reply_to_message is not None:
        print(message.reply_to_message.text, "qwertyuiolkjhgfdewr5t6yuikbfdertyui")
        if message.text == "+":
            order = Order()
            user = User()
            title = message.reply_to_message.text.split("\n")[0].split(": ")[1]
            order.get_by_title(title)
            print(order.get_category(), "---------")
            category = order.get_category()["out"]
            user.get_from_tg_id(message.from_user.id)
            workers = user.get_all_users(category)
            if workers["status"] == "ok":
                w_data = workers["out"]
                rater = lambda x: (x[-1] / 10 +
                                   meaning_rating.Similarity(model, index2word_set).sim(
                                       [order.get_worker_skills()["out"], x[5]]) +
                                   activity_time_rating.task_completion(
                                       user.get_user_by_id(x[0])["out"].get_ml_data()["out"][0],
                                       user.get_user_by_id(x[0])["out"].get_ml_data()["out"][1],
                                       [[x[-2], order.get_time()["out"]]])) / 3

                w_data = sorted(w_data, key=rater, reverse=True)
                r = 15 if len(w_data) > 15 else len(w_data)
                out = list()
                out.append(
                    "Вот работники, которые могут подойти на вашу работу\nВыберете одного из них и ответьте '+' (без ковычек) на его анкету.")
                for i in range(r):
                    user = User().get_user_by_nickname(w_data[i][1])["out"]
                    mark = user.get_avg_mark()["out"]
                    sentence = f"Работник: @{w_data[i][1]}\n\nИмя: {w_data[i][3]}\n\nФамилия: {w_data[i][4]}\n\nНавыки: {w_data[i][5]}\n\nРейтинг: {mark}/10\n\nНачало работы: {w_data[i][7]} г."
                    global task
                    task = message.reply_to_message.text
                    out.append(sentence)
                return out

            elif workers["status"] == "no workers found":
                return ["Нет походящих работников для вашего заказа"]
        return ["Простите, я Вас не понимаю!"]


@bot.message_handler(commands=["agree"])
def agree(message):
    print(message)
    if message.reply_to_message is not None:
        order = Order()
        order.get_by_title(message.reply_to_message.text.split("\n")[0].split(": ")[1])
        print(order)
        user = User()
        user.get_from_tg_id(message.from_user.id)
        print(user)
        order.take_task(user.get_user_id()["out"], time.time())
        bot.send_message(message.from_user.id, "Вы начали работу над заказом!")
        emp_id = order.get_employer_id()["out"]
        employer = user.get_user_by_id(emp_id)["out"].tg_id
        bot.send_message(employer, f"Работник приступил к выполнению заказа с названием '{order.title}'")


@bot.message_handler(commands=["find_worker"])
def find_worker(message):
    print(message)
    status = user_in_db(message)
    if status == "ok":
        user = User()
        user.get_from_tg_id(message.from_user.id)
        orders = user.find_worker_data()
        if orders['status'] == "ok":
            data = user.find_worker_data()["out"]
            bot.send_message(message.from_user.id,
                             "Это-ваши активные заказы.\n\nОтветьте '+' (без ковычек) на сообщение с закаком, для которого вы хотели бы нации работника")
            for i in data:
                bot.send_message(message.from_user.id,
                                 f"Название: {i[3]}\n\nОписание заказа: {i[4]}\n\nВремя на выполнение: {i[10]} дня\n\nКатегория: {i[5]}\n\nТребуемые навыки: {i[6]}",)
                global flags
                for i in range(len(flags)):
                    flags[i] = False
                flags[3] = True

        elif orders["status"] == "no orders found":
            bot.send_message(message.from_user.id, "У Вас пока нет заказов для поиска работников!")

    else:
        bot.send_message(message.from_user.id, "Сначала Вам нужно зарегистрироваться!\nВоспользуйтесь /register")


def finish_order(message):
    print("---------------", message)
    if message.reply_to_message is not None:
        verdict = message.text.split("\n\n")[0]
        print(verdict)
        if verdict == "+" or verdict == "-":
            if len(message.text.split("\n\n")) == 3:
                res = 1 if verdict == "+" else 0
                order = Order()
                order.get_by_title(message.reply_to_message.text.split("\n\n")[0].split(": ")[1])
                active = order.get_active()["status"]
                if active == "ok":
                    out = order.set_finished(res, time.time())["status"]
                    print(out)
                    if out == "no worker for this order":
                        return "На данный заказ ещё не назначен работник"
                    if out == "ok":
                        if message.text.split("\n\n")[1].isdigit():
                            if 0 <= int(message.text.split("\n\n")[1]) <= 10:
                                print(message.text.split("\n\n")[2], int(message.text.split("\n\n")[1]))
                                output = order.add_feedback_and_mark(message.text.split("\n\n")[2],
                                                                     int(message.text.split("\n\n")[1]))["status"]
                                print(output, "output add_feedback")
                                if output == "ok":
                                    user = User()
                                    mark = order.get_mark()["out"]
                                    feed_back = order.get_feedback()["out"]
                                    title = order.title
                                    bot.send_message(user.get_user_by_id(order.get_worker_id()["out"])["out"].tg_id, f"Работодатель завершил заказ '{title}'\n\nОценка: {mark}/10\n\nОтзыв: {feed_back}")
                                    return "Заказ завершён.\nДля дальнейщих дейсвий перейдите в /help"

                                else:
                                    order.set_active_true()
                                    return "Попробуйте ещё раз. /my_orders"
                            else:
                                order.set_active_true()
                                return "Оценка не должна быть отрицательной или больше 10"
                        else:
                            order.set_active_true()
                            return "Оценка может быть только числом."
                    else:
                        order.set_active_true()
                        return "Извините, но даже ботам нужно отдыхать. Zzz.."
                else:
                    return "Заказ уже завершён"
            else:
                return "Проверьте,что ввели все данные. И попробуйте ещё раз /my_orders."
        else:
            return "Извините, не понимаю вас. Попробуйте ещё раз /my_orders."


@bot.message_handler(content_types=["text"])
def text(message):
    print(message)
    global flags, text, my_orders_f
    print(flags)
    if flags[0] or flags[1]:
        out = registration_reply(message)
        bot.send_message(message.from_user.id, out)
        for i in range(len(flags)):
            flags[i] = False
        return

    if flags[2]:
        print('flaaaaag')
        out = add_order_reply(message)
        bot.send_message(message.from_user.id, out)
        for i in range(len(flags)):
            flags[i] = False
        return

    if flags[3]:
        print("-----------")
        out = appropriate_workers(message)
        for i in out:
            bot.send_message(message.from_user.id, i, parse_mode="Markdown")
        for i in range(len(flags)):
            flags[i] = False
        flags[5] = True
        return

    if flags[4]:
        print("YYYYYYYYYYYY")
        global task
        out = work_application(message)
        bot.send_message(message.from_user.id,  out)
        for i in range(len(flags)):
            flags[i] = False
        task = ""
        return

    if flags[5]:
        print("немного зашло")
        print(message.reply_to_message.text)
        if message.reply_to_message.text[0] == "Р":
            print("Зашлоооооооооо")
            out = hire(message)
            bot.send_message(message.from_user.id, out)
        for i in range(len(flags)):
            flags[i] = False
        return

    if my_orders_f:
        out = finish_order(message)
        bot.send_message(message.from_user.id, out)
        for i in range(len(flags)):
            flags[i] = False
        my_orders_f = False


@bot.callback_query_handler(func=lambda call: True)
def callback_buttons(call):
    id = call.message.chat.id
    user = User()
    status = user.get_from_tg_id(id)["status"]
    global flags

    if status == "user not found":
        if call.data == 'employer':
            bot.send_message(call.message.chat.id,
                             "Для завершения регистрации отправьте сообщение в формате:\n\nИМЯ\n\nФАМИЛИЯ")
            bot.send_message(call.message.chat.id, 'Вы будете зарегистрированы, как работодатель')
            for i in range(len(flags)):
                flags[i] = False
            flags[0] = True
            print(flags, "employer")

        elif call.data == 'mixed':
            keyboard = types.InlineKeyboardMarkup(True)
            keyboard.add(types.InlineKeyboardButton("ДИЗАЙН", callback_data="Дизайн"),
                         types.InlineKeyboardButton("МОДЕЛИРОВАНИЕ", callback_data="Моделирование"),
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
            flags[1] = True
            print(flags, "mixed")

        elif call.data in list(categories.keys()):
            bot.send_message(call.message.chat.id,
                             "Для завершения регистрации отправьте сообщение в формате:\n\n*ИМЯ*\n\n*ФАМИЛИЯ*\n\n*ДАТА НАЧАЛА РАБОТЫ (ГГГГ)*\n\n*НАВЫКИ, ТЕХНОГОЛИИ И УМЕНИЯ*",
                             parse_mode="Markdown")
            bot.send_message(call.message.chat.id, 'Вы будете зарегистрированы, как работник')
            categories[call.data] = True

    if status == "ok":
        if call.data in list(categories.keys()):
            bot.send_message(call.message.chat.id,
                             "Для создания заказа отправьте сообщение в формате:\n\n*НАЗВАНИЕ ЗАКАЗА*\n\n*ДЛИТЕЛЬНОСТЬ ВЫПОЛНЕНИЯ В ДНЯХ*\n\n*ОПИСАНИЕ ЗАКАЗА*\n\n*ТРЕБУЕМЫЕ КАЧЕСТВА И КВАЛИФИКАЦИИ ОТ РАБОТНИКА*",
                             parse_mode="Markdown")
            categories[call.data] = True
            for i in range(len(flags)):
                flags[i] = False
            flags[2] = True


def add_order_reply(message):
    status = user_in_db(message)
    sentence = message.text.split("\n\n")
    print(sentence)
    if status == "ok":
        order = Order()
        if len(sentence) == 4:
            user = User()
            user.get_from_tg_id(message.from_user.id)
            order_creation = {"employer_id": user.get_user_id()["out"]}

            if len(sentence[0]) > 40 or len(sentence[0]) < 5:
                return "Длина названия должна быть больше 5 и меньше 40 символов.\nВоспользуйтесь коммандой /add_order заново."
            if len(censor_checker(sentence[0])) != 0:
                return censor_checker(sentence[0])
            if not sentence[1].isdigit():
                return "Длитеольность выполнения заказа должна састоять только из цифр.\nВоспользуйтесь коммандой /add_order заново."
            if len(censor_checker(sentence[1])) != 0:
                return censor_checker(sentence[1])
            if len(sentence[2]) < 30:
                return "Слишком короткое описание заказа(оно должно быть больше 30 символов.\nВоспользуйтесь коммандой /add_order заново."
            if len(censor_checker(sentence[2])) != 0:
                return censor_checker(sentence[2])

            order_creation["title"] = sentence[0]
            order_creation["time"] = int(sentence[1])
            order_creation["description"] = sentence[2]

            for i in range(len(list(categories.keys()))):
                if list(categories.values())[i]:
                    order_creation["category"] = list(categories.keys())[i]

            if len(censor_checker(sentence[3])) != 0:
                return censor_checker(sentence[3])
            order_creation["worker_skills"] = sentence[3]

            status = order.add_order(order_creation)["status"]
            if status == "ok":
                for i in list(categories.keys()):
                    categories[i] = False
                print(categories)
                return "Заказ успешно добавлен!\nДля дальнейших действий передите в /help."
            elif status == "order with this title already exists":
                return "Данное название уже существует. Придумайте другое.\nВоспользуйтесь коммандой /add_order заново."
            else:
                return "Провьрьте, указали ли вы все требуемые данные!\nВоспользуйтесь коммандой /add_order заново."
        else:
            return "Провьрьте, указали ли вы все требуемые данные!\nВоспользуйтесь коммандой /add_order заново."


try:
    print("BOT UP", str(datetime.now()).split(".")[0], sep="\t")
    bot.polling(none_stop=True)
except Exception as e:
    bot.stop_bot()
    print("BOT DOWN", str(datetime.now()).split(".")[0], sep="\t")
