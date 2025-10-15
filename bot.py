import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Конфигурация из переменных окружения
TOKEN = os.getenv('TOKEN')
RENDER_API_KEY = os.getenv('RENDER_API_KEY')

print("🔧 Проверка переменных окружения:")
print(f"TOKEN: {'✅ установлен' if TOKEN else '❌ отсутствует'}")
print(f"RENDER_API_KEY: {'✅ установлен' if RENDER_API_KEY else '❌ отсутствует'}")

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привет! Отправь мне описание изображения, и я сгенерирую его с помощью AI."
    )

def generate_image(update: Update, context: CallbackContext):
    user_text = update.message.text
    
    if not user_text.strip():
        update.message.reply_text("Пожалуйста, отправь описание изображения.")
        return

    try:
        wait_message = update.message.reply_text("🔄 Генерирую изображение...")
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=wait_message.message_id)
        update.message.reply_text("⏳ Функция генерации настраивается...")
    except Exception as e:
        update.message.reply_text(f"❌ Произошла ошибка: {str(e)}")

def main():
    print("🚀 Запуск бота...")
    
    if not TOKEN:
        print("❌ ОШИБКА: Не установлен TOKEN")
        return
    
    try:
        # Используем Updater для старых версий python-telegram-bot
        updater = Updater(TOKEN, use_context=True)
        dispatcher = updater.dispatcher
        
        print("✅ Updater создан")
        
        # Добавляем обработчики
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, generate_image))
        print("✅ Обработчики добавлены")
        
        # Запускаем бота
        print("🔄 Бот запущен и ожидает сообщения...")
        updater.start_polling()
        updater.idle()
        
    except Exception as e:
        print(f"❌ Критическая ошибка при запуске: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
