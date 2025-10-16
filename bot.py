# bot.py
# Python 3.8 — webhook версия, подходит для деплоя на Render
import os
import requests
import time 
from urllib.parse import quote_plus
from flask import Flask, request, Response
from telegram import Bot, InputFile

# -------- CONFIG ----------
TOKEN = os.environ.get("TG_BOT_TOKEN")  # Установим в Render как переменную окружения
BOT_NAME = os.environ.get("BOT_NAME", "Avatar ai bot")
TRANSLATE_URL = os.environ.get("LIBRETRANSLATE_URL", "https://libretranslate.com/translate")
POLLINATIONS_BASE = "https://image.pollinations.ai/prompt/"
# --------------------------

if not TOKEN:
    raise RuntimeError("Не найден TG_BOT_TOKEN в переменных окружения")

app = Flask(name)
bot = Bot(token=TOKEN)


def translate_to_en(text: str) -> str:
    """Попробуем перевести текст на английский через LibreTranslate; при ошибке — вернём исходный."""
    try:
        payload = {"q": text, "source": "auto", "target": "en", "format": "text"}
        r = requests.post(TRANSLATE_URL, data=payload, timeout=10)
        r.raise_for_status()
        data = r.json()
        return data.get("translatedText") or text
    except Exception as e:
        print("Translate failed:", e)
        return text


def generate_image_bytes(prompt_en: str) -> bytes:
    """Запрос к Pollinations — вернёт байты изображения."""
    encoded = quote_plus(prompt_en)
    # Просим портрет в стиле аниме, 1024x1024
    url = f"{POLLINATIONS_BASE}{encoded}?width=1024&height=1024&nologo=true"
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    content_type = resp.headers.get("Content-Type", "")
    if "image" in content_type:
        return resp.content
    # Иногда Pollinations возвращает в теле URL
    text = resp.text.strip()
    if text.startswith("http"):
        r2 = requests.get(text, timeout=60)
        r2.raise_for_status()
        return r2.content
    return resp.content


@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    """Telegram будет слать сюда обновления (webhook)."""
    try:
        update = request.get_json(force=True)
        if not update:
            return Response("ok", status=200)

        message = update.get("message") or update.get("edited_message")
        if not message:
            return Response("ok", status=200)

        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()
        if not text:
            bot.send_message(chat_id=chat_id, text="Отправь любой текст — я сгенерирую аватарку в стиле аниме.")
            return Response("ok", status=200)

        # 1) Сообщаем пользователю, что начинаем
        sending_msg = bot.send_message(chat_id=chat_id, text="Генерирую… пожалуйста подожди")

        # 2) Переводим на английский
        prompt_en = translate_to_en(text)

        # 3) Подставляем шаблон prompt'а для аниме-аватара
        enhanced_prompt = (
            f"{prompt_en}, anime style, portrait, head and shoulders, highly detailed, "
            "sharp eyes, soft cinematic lighting, vibrant colors, clean lineart, ultra-detailed"
        )

        # 4) Генерируем картинку
        try:
            img_bytes = generate_image_bytes(enhanced_prompt)
        except Exception as e:
            print("Generate error:", e)
            bot.send_message(chat_id=chat_id, text="Ошибка генерации изображения — попробуй другой запрос.")
            return Response("ok", status=200)

        # 5) Временный файл и отправка
        tmp_name = f"/tmp/avatar_{int(time.time())}.png"
        try:
            with open(tmp_name, "wb") as f:
                f.write(img_bytes)

            with open(tmp_name, "rb") as f:
                bot.send_photo(chat_id=chat_id, photo=InputFile(f, filename="avatar.png"))
        finally:
            # Удаляем временный файл, если он есть
            try:
                if os.path.exists(tmp_name):
                    os.remove(tmp_name)
            except Exception:
                pass

# 6) Удаляем сообщение "Генерирую..."
        try:
            bot.delete_message(chat_id=chat_id, message_id=sending_msg.message_id)
        except Exception:
            pass

    except Exception as ex:
        print("Webhook handler error:", ex)

    return Response("ok", status=200)


@app.route("/", methods=["GET"])
def index():
    return f"{BOT_NAME} is running."


if __name__ == "__main__":
    # Для локального теста (не для Render) можно запустить Flask:
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
