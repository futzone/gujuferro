from dotenv import load_dotenv
import os

load_dotenv()


def get_bot_token() -> str:
    bot_token = os.getenv("BOT_TOKEN")
    return bot_token


def get_badword_percent() -> int:
    percent = os.getenv('BADWORD_PERCENT')
    return float(percent)
