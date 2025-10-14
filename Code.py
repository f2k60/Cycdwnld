import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8360021032:AAFbqzS-9RqYjTbiVAi5yxW_v_DEcRoh3BI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне видеофайл, и я верну тебе звук из него.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video or update.message.document
    if video is None:
        await update.message.reply_text("Пожалуйста, отправь именно видеофайл.")
        return

    file_id = video.file_id
    file = await context.bot.get_file(file_id)

    input_path = f"temp_{file_id}.mp4"
    output_path = f"audio_{file_id}.mp3"

    await file.download_to_drive(input_path)

    # Конвертируем видео в аудио через ffmpeg
    command = ['ffmpeg', '-i', input_path, '-vn', '-acodec', 'mp3', output_path]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Отправляем аудио пользователю
    with open(output_path, 'rb') as audio_file:
        await update.message.reply_audio(audio_file)

    # Удаляем временные файлы
    os.remove(input_path)
    os.remove(output_path)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text("Отправь видеофайл, чтобы я мог извлечь звук.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
