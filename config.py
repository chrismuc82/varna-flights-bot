from dotenv import load_dotenv
import os

load_dotenv()  # this loads the .env file automatically

# Kiwi API Key
KIWI_API_KEY = os.getenv("KIWI_API_KEY")

# Tinyurl API Token
TINYURL_API_KEY = os.getenv("TINYURL_API_KEY")

# Telegram Bot API Key
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")

# Your Telegram group
GROUP_ID = os.getenv("GROUP_ID")
