import logging
import telegram
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

    if 'бухгалтерию' in question or 'бухгалтерия' in question or 'бухгалтерский' in question or 'финансы' in question or 'зп' in question or 'зарплата' in question or 'документы' in question:
        answer = responses['accounting']
    elif 'отдел кадров' in question or 'кадры' in question or 'hr' in question or 'персонал' in question or 'найм' in question or 'увольнение' in question:
        answer = responses['hr']
    elif 'привет' in question or 'здравствуйте' in question or 'добрый день' in question or 'добрый вечер' in question or 'доброе утро' in question:
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
