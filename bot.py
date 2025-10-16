import logging
from telegram import Bot, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Вставь свой токен
TOKEN = "ТВОЙ_ТОКЕН_СЮДА"  # <-- НЕ ЗАБУДЬ ВСТАВИТЬ

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Команда /start
def start(update, context):
    update.message.reply_text("Привет! Я готов генерировать изображения. Напиши стиль и описание.")

# Обработка текстовых сообщений
def handle_message(update, context):
    text = update.message.text
    update.message.reply_text(f"Генерирую по запросу: {text}")

def main():
        if TOKEN == "" or TOKEN == "ТВОЙ_ТОКЕН_СЮДА":
            print("❌ Ошибка: вставь токен в переменную TOKEN")
            return

        updater = Updater(TOKEN)
        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

        updater.start_polling()
        updater.idle()

if __name__ == "__main__":
    main()
