import asyncio
import logging
from aiogram import Bot, Dispatcher

from main import bot_token
from app.handlers.start_handler import start_router
from app.handlers.application_handler import application_router



async def main():
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(application_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exit")
