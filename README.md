# Telegram Zip Bot

A Telegram bot that zips files sent by users and returns the archive.

## Features
- Accepts multiple files from users.
- Creates a `.zip` archive.
- Sends the compressed archive back to the user.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/your-username/telegram-zip-bot.git
   cd telegram-zip-bot
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file.
   - Add your Telegram Bot API key:
     ```
     TELEGRAM_BOT_TOKEN=your_bot_token_here
     ```

4. Run the bot:
   ```
   python bot.py
   ```

## Usage
1. Start the bot on Telegram.
2. Send files to the bot.
3. Use the `/zip` command to receive the zipped archive.

## License
MIT