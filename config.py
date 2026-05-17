"""
Configuration module - loads settings from environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token (get from @BotFather)
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Your Telegram User ID (get from @userinfobot)
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# Default check interval in seconds
DEFAULT_INTERVAL = int(os.getenv("DEFAULT_INTERVAL", "60"))

# MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI", "")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "testflight_monitor")

# Request timeout in seconds
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))
