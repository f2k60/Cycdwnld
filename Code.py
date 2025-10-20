from flask import Flask, request, jsonify
import requests
from telegram import Bot, InputFile

app = Flask(__name__)

# Токен вашего Telegram бота
BOT_TOKEN = "ВАШ_ТОКЕН_БОТА"
bot = Bot(token=BOT_TOKEN)

@app.route('/send_image', methods=['POST'])
def send_image():
    data = request.json
    chat_id = data.get('chat_id')
    image_url = data.get('image_url')
    
    if not chat_id or not image_url:
        return jsonify({"status": "error", "message": "chat_id or image_url is missing"}), 400

    # Скачиваем картинку
    resp = requests.get(image_url)
    if resp.status_code != 200:
        return jsonify({"status": "error", "message": "Failed to download image"}), 400

    # Отправляем картинку в Telegram чат
    try:
        bot.send_photo(chat_id=chat_id, photo=resp.content)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "success", "message": "Image sent"}), 200

if __name__ == '__main__':
    app.run(port=5000)
