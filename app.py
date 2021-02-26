from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.misc.set_bot_commands import set_default_commands
from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    # Уведомляет про запуск
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
