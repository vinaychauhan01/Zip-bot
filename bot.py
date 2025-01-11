import os
from zipfile import ZipFile
from telegram import Update, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Directory to store temporary files
TEMP_DIR = "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me files, and I'll zip them for you.")

# File handler
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    file_name = file.file_name

    # Await the get_file() coroutine
    tg_file = await file.get_file()

    # Use the correct download() method to save the file
    file_path = os.path.join(TEMP_DIR, file_name)
    await tg_file.download(file_path)

    await update.message.reply_text(f"File {file_name} received! Send /zip to create the archive.") to 

    # Download file
    file_path = os.path.join(TEMP_DIR, file_name)
    await file.get_file().download_to_drive(file_path)

    await update.message.reply_text(f"File {file_name} received! Send /zip to create the archive.")

# Zip files handler
async def zip_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    zip_path = os.path.join(TEMP_DIR, "files.zip")

    # Create a zip archive
    with ZipFile(zip_path, "w") as zipf:
        for file_name in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, file_name)
            if os.path.isfile(file_path):
                zipf.write(file_path, arcname=file_name)

    # Send the zip file
    with open(zip_path, "rb") as zipf:
        await update.message.reply_document(zipf)

    # Clean up
    for file_name in os.listdir(TEMP_DIR):
        os.remove(os.path.join(TEMP_DIR, file_name))

# Main function
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    application.add_handler(CommandHandler("zip", zip_files))

    application.run_polling()

if __name__ == "__main__":
    main()
