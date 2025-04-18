import asyncio
from datetime import datetime
from app.database.database import init_db
from bot.runner import dp, bot


def start_bot():
    asyncio.run(init_db())
    asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    try:
        start_bot()
    except KeyboardInterrupt:
        print(f"=== ⚫️ Finished at {datetime.now()} ===")
