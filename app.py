from aiogram import executor

from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    import filters
    import middlewares

    filters.setup(dispatcher)
    middlewares.setup(dispatcher)

    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
