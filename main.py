# Импортируем необходимые классы.
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
import json

# считываем конфиг с токеном
with open('config.json') as f:
    config = json.loads(f.read())
    TOKEN = config["TOKEN"]


def echo(update, context):  # функция эхо нужна для теста связи с ботом
    print(update.message.text)
    update.message.reply_text(f"Я получил сообщение {update.message.text}")


def help(update, context):  # help поможет в будущем пользователю разобраться с возможностями бота
    update.message.reply_text(f"Пока что, я ничего не умею, но скоро всему научусь)")


def start(update, context):  # начало работы бота с клиентом
    update.message.reply_text(f"Отлично, начнём!")


def main():
    # создаём апдейтер добавляя туда токен бота
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # отключенныя функция эхо
    # text_handler = MessageHandler(Filters.text, echo)
    # dp.add_handler(text_handler)

    dp.add_handler(CommandHandler("start", start))  # подключение функции старт
    dp.add_handler(CommandHandler("help", help))  # подключение функции help

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
