import logging
import telegram
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from responses import responses
from urllib.parse import quote


API_KEY = "6214551617:AAGDXgiFtzZkoMaTxVrBXh2ESpSUvh9vyZc"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, _: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Бухгалтерия", callback_data='accounting'),
         InlineKeyboardButton("Отдел кадров", callback_data='hr')],
        [InlineKeyboardButton("IT", callback_data='it'),
         InlineKeyboardButton("Продажи", callback_data='sales')],
        [InlineKeyboardButton("Маркетинг", callback_data='marketing'),
         InlineKeyboardButton("Разработка", callback_data='development')],
        [InlineKeyboardButton("Управление проектами", callback_data='project_management'),
         InlineKeyboardButton("Юридический отдел", callback_data='legal')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Привет! Я бот, который отвечает на вопросы сотрудников. Выберите категорию вопроса:", reply_markup=reply_markup)

def handle_message(update: Update, _: CallbackContext):
    # Ваш код обработки сообщений остается без изменений

def button(update: Update, _: CallbackContext):
    query = update.callback_query
    query.answer()

    question = query.data.lower()
    answer = responses.get(question, responses['error'].format(question))
    query.edit_message_text(answer)

def error(update: Update, context: CallbackContext):
    logger.error('Update "%s" caused error "%s"', update, context.error)

def main():
    bot = telegram.Bot(token=API_KEY)
    updater = Updater(bot.token, persistence=None, workers=10)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
