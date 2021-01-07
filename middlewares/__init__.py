from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware


if __name__ == "a.middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
