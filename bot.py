import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Конфигурация из переменных окружения
TOKEN = os.getenv('TOKEN')
RENDER_API_KEY = os.getenv('RENDER_API_KEY')

print(f"🔧 Проверка переменных: TOKEN={'установлен' if TOKEN else 'НЕТ'}, API_KEY={'установлен' if RENDER_API_KEY else 'НЕТ'}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Отправь мне описание изображения, и я сгенерирую его с помощью AI."
    )

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    if not user_text.strip():
        await update.message.reply_text("Пожалуйста, отправь описание изображения.")
        return

    try:
        wait_message = await update.message.reply_text("🔄 Генерирую изображение...")
        await context.bot.delete_message(chat_id=update.message.chat_id, message_id=wait_message.message_id)
        await update.message.reply_text("⏳ Функция генерации настраивается...")
    except Exception as e:
        await update.message.reply_text(f"❌ Произошла ошибка: {str(e)}")

def main():
    print("🚀 Запуск бота...")
    
    if not TOKEN:
        print("❌ ОШИБКА: Не установлен TOKEN")
        return
    
    try:
        application = Application.builder().token(TOKEN).build()
        print("✅ Application создан")
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))
        print("✅ Обработчики добавлены")
        
        print("🔄 Бот запущен и ожидает сообщения...")
        application.run_polling()
        
    except Exception as e:
        print(f"❌ Критическая ошибка при запуске: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
