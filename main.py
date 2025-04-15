import asyncio
from datetime import datetime

from app.chat.app import train_bot
from bot.runner import dp, bot


def start_bot():
    train_bot()
    asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    try:
        start_bot()
    except KeyboardInterrupt:
        print(f"=== ⚫️ Finished at {datetime.now()} ===")
