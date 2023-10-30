from telegram import Bot
from dotenv import load_dotenv
import os


load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


async def send_code(code):
    bot = Bot(token=TELEGRAM_TOKEN)
    async with bot:
        await bot.send_message(text=code, chat_id=TELEGRAM_CHAT_ID)
