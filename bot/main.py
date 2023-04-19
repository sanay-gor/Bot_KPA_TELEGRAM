import os
import glob
from docx import Document
import PyPDF2
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from nextcloud import Nextcloud

# Настройка токена и папки с документами
TOKEN = "6214551617:AAGDXgiFtzZkoMaTxVrBXh2ESpSUvh9vyZc"
DOCS_FOLDER = "docs/"

# Настройка Nextcloud
NEXTCLOUD_URL = "https://docs.avtomatika.kz/"
NEXTCLOUD_USERNAME = "nexcloud"
NEXTCLOUD_PASSWORD = "Hgiu0e4upfjsdhdksfht87LHUGFUFU232432!!"
NEXTCLOUD_UPLOAD_FOLDER = "/var/snap/nextcloud/common/nextcloud/data/nexcloud

nextcloud_client = Nextcloud(NEXTCLOUD_URL, NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD)


def search_docx(keyword: str):
    results = []
    for doc_path in glob.glob(os.path.join(DOCS_FOLDER, "*.docx")):
        doc = Document(doc_path)
        for paragraph in doc.paragraphs:
            if keyword in paragraph.text:
                results.append(doc_path)
                break
    return results


def search_pdf(keyword: str):
    results = []
    for pdf_path in glob.glob(os.path.join(DOCS_FOLDER, "*.pdf")):
        pdf = PyPDF2.PdfFileReader(pdf_path)
        for page_num in range(pdf.numPages):
            text = pdf.getPage(page_num).extractText()
            if keyword in text:
                results.append(pdf_path)
                break
    return results


def upload_to_nextcloud_and_get_link(file_path: str):
    with open(file_path, "rb") as file:
        file_content = file.read()
    file_name = os.path.basename(file_path)

    # Загрузка файла в Nextcloud
    response = nextcloud_client.upload_file(file_content, NEXTCLOUD_UPLOAD_FOLDER + "/" + file_name)

    if response.is_ok:
        # Создание публичной ссылки
        share_response = nextcloud_client.create_share(NEXTCLOUD_UPLOAD_FOLDER + "/" + file_name, share_type=3)

        if share_response.is_ok:
            return share_response.get_link()
        else:
            raise Exception("Ошибка создания публичной ссылки: " + share_response.raw_error)
    else:
        raise Exception("Ошибка загрузки файла: " + response.raw_error)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Введите ключевое слово для поиска в документах:")


def search(update: Update, context: CallbackContext):
    keyword = update.message.text

    docx_results = search_docx(keyword)
    pdf_results = search_pdf(keyword)

    if not docx_results and not pdf_results:
        update.message.reply_text("Документы, содержащие указанное ключевое слово, не найдены.")
    else:
        update.message.reply_text("Найденные документы:")
        for result in docx_results + pdf_results:
            try:
                public_link = upload_to_nextcloud_and_get_link(result)
                update.message.reply_text(f"Публичная ссылка: {public_link}")
            except Exception as e:
                update.message.reply_text(f"Ошибка загрузки файла {result} в Nextcloud: {str(e)}")


def main():
    updater = Updater(TOKEN)

    dp
