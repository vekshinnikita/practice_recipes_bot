import asyncio
import logging
from aiogram import Bot, Dispatcher

import app.config as config
from app.handlers.basic import router as basic_router
from app.handlers.recipe import router as recipe_router
from app.handlers.admin import router as admin_router
from app.handlers.admin_add_recipe import router as admin_add_recipe_router
from app.handlers.admin_update_recipe import router as admin_update_recipe_router
from app.middlewares.init import init_middlewares

dp = Dispatcher()


def init_routers():
    dp.include_routers(
        basic_router,
        recipe_router,
        admin_router,
        admin_add_recipe_router,
        admin_update_recipe_router
    )

async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)

    init_routers()
    init_middlewares(dp)
    bot = Bot(token=config.TG_BOT_TOKEN)
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())