from aiogram import Bot, Dispatcher, types

from bot.handlers.text_handler import text_handler, on_start_training_handler
from utils.env_loader import get_bot_token

token = get_bot_token()
bot = Bot(token)
dp = Dispatcher()


@dp.message()
async def on_message(message: types.Message):
    await text_handler(message=message, bot=bot)
    await on_start_training_handler(message=message)
