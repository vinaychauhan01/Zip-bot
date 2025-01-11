import os
from zipfile import ZipFile
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(TOKEN)

# Directory to store temporary files
TEMP_DIR = "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

# Start command handler
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! Send me files, and I'll zip them for you.")

# File handler
def handle_file(update: Update, context: CallbackContext):
    file = update.message.document
    file_name = file.file_name

    # Download file
    file_path = os.path.join(TEMP_DIR, file_name)
    file.get_file().download(file_path)

    update.message.reply_text(f"File {file_name} received! Send /zip to create the archive.")

# Zip files handler
def zip_files(update: Update, context: CallbackContext):
    zip_path = os.path.join(TEMP_DIR, "files.zip")

    # Create a zip archive
    with ZipFile(zip_path, "w") as zipf:
        for file_name in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, file_name)
            if os.path.isfile(file_path):
                zipf.write(file_path, arcname=file_name)

    # Send the zip file
    with open(zip_path, "rb") as zipf:
        update.message.reply_document(zipf)

    # Clean up
    for file_name in os.listdir(TEMP_DIR):
        os.remove(os.path.join(TEMP_DIR, file_name))

# Error handler
def error(update: Update, context: CallbackContext):
    update.message.reply_text("An error occurred.")

# Main function
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document, handle_file))
    dispatcher.add_handler(CommandHandler("zip", zip_files))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()