# Импортируем необходимые классы.
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler


def echo(update, context):
    print(update.message.text)
    update.message.reply_text(f"Я получил сообщение {update.message.text}")


def help(update, context):
    update.message.reply_text(f"Пока что, я ничего не умею, но скоро всему научусь)")


def start(update, context):
    update.message.reply_text(f"Отлично, начнём!")


def main():
    updater = Updater("1122672197:AAFFrYPRv8VICDcCT-UywBP0Ygy1XEnoRUs", use_context=True)
    dp = updater.dispatcher

    # text_handler = MessageHandler(Filters.text, echo)
    # dp.add_handler(text_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
