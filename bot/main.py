import logging
import telegram
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from responses import responses
from urllib.parse import quote


API_KEY = "6037731646:AAESrQjxr0Kf5O0NO8vyMX_ZI5JditpoAQg"

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

def button(update: Update, _: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Выбрана категория: {query.data}. Теперь задайте свой вопрос по этой категории.")

def handle_message(update: Update, _: CallbackContext):
    question = update.message.text.lower()

    if re.search(accounting_keywords, question, re.IGNORECASE):
        answer = responses['accounting']
    elif re.search(hr_keywords, question, re.IGNORECASE):
        answer = responses['hr']
    elif re.search(greetings_keywords, question, re.IGNORECASE):
        answer = responses['greetings']
    elif re.search(it_keywords, question, re.IGNORECASE):
        encoded_question = quote(question)
        yandex_search_url = f"https://yandex.ru/search/?text={encoded_question}"
        answer = responses['it'] + f"\nДополнительно вы можете поискать информацию по этому запросу в Яндекс: {yandex_search_url}"
    elif re.search(sales_keywords, question, re.IGNORECASE):
        answer = responses['sales']
    elif re.search(marketing_keywords, question, re.IGNORECASE):
        answer = responses['marketing']
    elif re.search(development_keywords, question, re.IGNORECASE):
        answer = responses['development']
    elif re.search(project_management_keywords, question, re.IGNORECASE):
        answer = responses['project_management']
    elif re.search(legal_keywords, question, re.IGNORECASE):
        answer = responses['legal']
    else:
        answer = responses['error'].format(question)

    update.message.reply_text(answer)
def error(update: Update, context: CallbackContext):
    logger.error('Update "%s" caused error "%s"', update, context.error)

def main():
    bot = telegram.Bot(token=API_KEY)
    updater = Updater(bot.token, persistence=None, workers=10)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
