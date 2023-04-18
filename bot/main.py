import logging
import telegram
import re
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from responses import responses

API_KEY = "6037731646:AAESrQjxr0Kf5O0NO8vyMX_ZI5JditpoAQg"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, _: CallbackContext):
    update.message.reply_text("Привет! Я бот, который отвечает на вопросы сотрудников. Задайте свой вопрос.")

def handle_message(update: Update, _: CallbackContext):
    question = update.message.text.lower()

    accounting_keywords = r'\b(бухгалтери[яюе]|бухгалтерск(ий|ой|ого)|финанс|з[а]?рплат[ыауе]?|документ|налог|отч[её]т|бюджет)\b'
    hr_keywords = r'\b(отдел(а|е)? кадр(ов|ы)?|кадров(ый|ого|ом)?|hr|персонал|найм|увольнен|трудоустро[йи]ство|трудов[ао]?й договор|работник|сотрудник)\b'
    greetings_keywords = r'\b(привет|здравствуйте|добр(ый|ого) день|добр(ый|ого) вечер|доброе утро)\b'

    if re.search(accounting_keywords, question):
        answer = responses['accounting']
    elif re.search(hr_keywords, question):
        answer = responses['hr']
    elif re.search(greetings_keywords, question):
        answer = responses['greetings']
    else:
        answer = responses['default'].format(question)

    update.message.reply_text(answer)

def error(update: Update, context: CallbackContext):
    logger.error('Update "%s" caused error "%s"', update, context.error)

def main():
    bot = telegram.Bot(token=API_KEY)
    updater = Updater(bot.token, persistence=None, workers=10)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
