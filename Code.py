import base64
from io import BytesIO

@app.route('/send_image', methods=['POST'])
def send_image():
    data = request.json
    chat_id = data.get('chat_id')
    image_base64 = data.get('image_url')

    if not chat_id or not image_base64:
        return jsonify({"status": "error", "message": "chat_id or image_url is missing"}), 400

    try:
        # Убрать префикс data:image/png;base64, если есть
        header, encoded = image_base64.split(',', 1)
        image_bytes = base64.b64decode(encoded)
        bio = BytesIO(image_bytes)
        bio.name = 'image.png'

        bot.send_photo(chat_id=chat_id, photo=bio)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "success", "message": "Image sent"}), 200
