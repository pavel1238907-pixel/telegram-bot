import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Конфигурация
TOKEN = "8337981356:AAFEYQ16ZTPxlFTdz2Z1fu9QeGhQp5BGhLw"
RENDER_API_KEY = "rnd_DbdO6fyNX19QUl9EDBR5XGtMTy6s"

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
        # Отправляем запрос в Render API
        headers = {
            "Authorization": f"Bearer {RENDER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": user_text,
            "width": 512,
            "height": 512
        }
        
        response = requests.post(
            "https://api.render.ai/v1/images/generate",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            image_url = response.json()["url"]
            
            # Отправляем изображение пользователю
            await update.message.reply_photo(image_url)
        else:
            await update.message.reply_text("Ошибка генерации изображения. Попробуйте позже.")
            
    except Exception as e:
        await update.message.reply_text("Произошла ошибка. Попробуйте другой запрос.")

def main():
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))
    
    # Запускаем бота
    application.run_polling()

    if __name__ == "__main__":
        main()
