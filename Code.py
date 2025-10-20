from flask import Flask, request, jsonify
import requests
from telegram import Bot

app = Flask(__name__)

# Токен вашего Telegram бота
BOT_TOKEN = "8472306870:AAGjlAiWmvFhsIqhuQ-hKGpaD3A8UkElZws"
bot = Bot(token=BOT_TOKEN)

@app.route('/send_image', methods=['POST'])
def send_image():
    data = request.json
    chat_id = data.get('chat_id')
    image_url = data.get('image_url')
    
    if not chat_id or not image_url:
        return jsonify({"status": "error", "message": "chat_id or image_url is missing"}), 400

    # Отправляем картинку в Telegram по URL напрямую
    try:
        bot.send_photo(chat_id=chat_id, photo=image_url)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "success", "message": "Image sent"}), 200

if __name__ == '__main__':
    app.run(port=5000)
