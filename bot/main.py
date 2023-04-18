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
    update.message.reply_text("Привет! Я бот, который отвечает на вопросы сотрудников. Выберите категорию вопроса:",
                              reply_markup=reply_markup)


def handle_message(update: Update, _: CallbackContext):
    question = update.message.text.lower()

    accounting_keywords = r'\b(бухгалтери[яюе]|зп|бухгалтерск(ий|ой|ого|ая|ое)|финанс(ов|ы)?|з[а]?рплат(а|у|е|ой|ы)?|документ[ыа]?|налог[аи]?|отч[её]т[ау]?|бюджет)\b'
    hr_keywords = r'\b(отдел(а|е)? кадр(ов|ы)?|кадров(ый|ого|ом|ая|ое|ых)?|hr|персонал|найм|увольнен(ие|ия)?|трудоустро[йи]ство|трудов(ой|ая|ые)? договор|работник[аи]?|сотрудник[аи]?)\b'
    greetings_keywords = r'\b(привет|здравствуйте|добр(ый|ого) день|добр(ый|ого) вечер|доброе утро)\b'
    it_keywords = r'\b(ошибк[а-я]*|сбо[йи]*|неполадк[а-я]*|не\s*работа[ею][тт]*|загрузк[а-я]*|установк[а-я]*|активаци[я-я]*|логин[а-я]*|парол[ьяи]*|вирус[а-я]*|безопасност[ьи]*|сетев[ооеё]*\s*подключен[и>
    sales_keywords = r'\b(продаж[и]?|отдел продаж|менеджер по продажам|клиент|контракт|сделк[аи])\b'
    marketing_keywords = r'\b(маркетинг|реклам[аы]|бренд|продвижение|smm|seo|контент|социальн[ыа]е? меди[а]?|кампани[яи]?)\b'
    development_keywords = r'\b(разработк[аи]|инженер[ы]?|программист|код|дизайнер|тестировщик|devops|frontend|backend|fullstack)\b'
    project_management_keywords = r'\b(управление проектами|менеджер проекта|планирование|scrum|график|задач[аи]?|контроль|агил[е]?|методология)\b'
    legal_keywords = r'\b(юридический отдел|адвокат|юрист|закон|право|договор|суд|спор|регистрация|лиценз[ияи]?)\b'

    if re.search(accounting_keywords, question, re.IGNORECASE):
        answer = responses['accounting']
    elif re.search(hr_keywords, question, re.IGNORECASE):
        answer = responses['hr']
    elif re.search(greetings_keywords, question, re.IGNORECASE):
        answer = responses['greetings']
    elif re.search(it_keywords, question, re.IGNORECASE):
        encoded_question = quote(question)
        yandex_search_url = f"https://yandex.ru/search/?text={encoded_question}"
        answer = responses[
                     'it'] + f"\nДополнительно вы можете поискать информацию по этому запросу в Яндекс: {yandex_search_url}"
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
