import logging
from telegram import Bot, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Вставь свой токен
TOKEN = "ТВОЙ_ТОКЕН_СЮДА"

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Команда /start
def start(update, context):
    update.message.reply_text("Привет! Я готов генерировать изображения. Напиши стиль и описание.")

# Обработка текстовых сообщений
def handle_message(update, context):
    text = update.message.text
    # Заглушка — здесь должна быть генерация
    update.message.reply_text(f"Генерирую по запросу: {text}")
    # Пример отправки картинки, если она уже есть
    # with open("test.jpg", "rb") as f:
    #     update.message.reply_photo(photo=InputFile(f))

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
