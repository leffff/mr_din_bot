from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
import create_environment
from os import getenv
from swear_words import russian_swear_words
from russian_word_db import RussianDataset

rd = RussianDataset()
rd.download()

swearing = russian_swear_words()

TOKEN = getenv("TOKEN")
PROXY = getenv("PROXY")
DBNAME = getenv("DBNAME")
USER = getenv("USER")
PASSWORD = getenv("PASSWORD")
PORT = getenv("PORT")
HOST = getenv("HOST")

REQUEST_KWARGS = {
    "proxy_url": PROXY  # Адрес прокси сервера
}


def start(update, context):  # начало работы бота с клиентом
    update.message.reply_text(f"Вас приветствует Job Bot!\n советуем ознакомиться с /help")


def echo(update, context):  # функция эхо нужна для теста связи с ботом
    print(update.message.text)
    print(
        update.message.from_user.id,
        update.message.from_user.first_name,
        update.message.from_user.last_name,
        update.message.from_user.username
    )
    update.message.reply_text(f"Я получил сообщение {update.message.text}")


def help(update, context):  # help поможет в будущем пользователю разобраться с возможностями бота
    update.message.reply_text(f"Пока что, я ничего не умею, но скоро всему научусь)")
    # если тг ник есть в базе, то предлагать фичи внктри
    # если тг ника нет в базе то предлагать /register
    reply_keyboard = [["/register"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Пока что, я ничего не умею, но скоро всему научусь)", reply_markup=markup)


def register(update, context):  # регистрация
    update.message.reply_text("Давайте зарегистрируемся!")


def find_work(update, context):  # поиск работы
    update.message.reply_text("Давайте найдём предложения!")


def post_order(update, context):  # создание заказа
    update.message.reply_text("Давайте опубликуем заказ!!")


def find_worker(update, context):  # посик работников
    update.message.reply_text("Давайте найдём работника!")


def view_tasks(update, context):  # просмотр своих выполняемых заданий
    update.message.reply_text("Просмотр заказов для выполнения")


def view_orders(update, context):  # создвние своих заказов
    update.message.reply_text("Просмотр своих заказов")


def main():
    # создаём апдейтер добавляя туда токен бота
    updater = Updater(TOKEN, use_context=True,
                      request_kwargs=REQUEST_KWARGS)
    dp = updater.dispatcher

    # отключенныя функция эхо
    dp.add_handler(CommandHandler("start", start))  # подключение функции старт
    dp.add_handler(CommandHandler("help", help))  # подключение функции help
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CommandHandler("find_work", find_work))
    dp.add_handler(CommandHandler("post_order", post_order))
    dp.add_handler(CommandHandler("find_worker", find_worker))
    dp.add_handler(CommandHandler("view_tasks", view_tasks))
    dp.add_handler(CommandHandler("view_orders", view_orders))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
