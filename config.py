import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Channel
CHANNEL_USERNAME = "@Ghoghnoostradebot"

# Admin
ADMIN_PHONE = "09130127941"

ADMIN_NAME = "تامین سیمان ققنوس"

CITY = "اصفهان"

MIN_ORDER = 5
