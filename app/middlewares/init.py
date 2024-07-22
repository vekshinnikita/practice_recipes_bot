

from aiogram import Dispatcher

from app.middlewares.admin import AdminMiddleware


def init_middlewares(dp: Dispatcher):
    dp.message.middleware(AdminMiddleware())