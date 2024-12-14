import asyncio

import logging

import aiogram
from aiogram import Bot, Dispatcher

bot = Bot(token="")
dp = Dispatcher()

async def main():
    await async_main()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("STOPPED")