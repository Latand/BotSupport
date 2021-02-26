from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("support", "Написать сообщение техподдержку"),
        types.BotCommand("support_call", "Пообщаться с техподдержкой"),
        types.BotCommand("help", "Помощь"),
    ])
