from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from keyboards.inline import support
from keyboards.inline.support import check_support_available, get_support_manager, cancel_keyboard
from loader import bot, dp


@dp.message_handler(Command("support_call"))
async def ask_support_call(message: types.Message):
    text = "Хотите связаться с техподдержкой? Нажмите на кнопку ниже!"
    keyboard = await support.support_keyboard(messages="many")
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(support.support_callback.filter(messages="many", as_user="yes"))
async def send_to_support(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.message.edit_text("Вы обратились в техподдержку. Ждем ответа от оператора!")

    user_id = int(callback_data.get("user_id"))
    if not await check_support_available(user_id):
        support_id = await get_support_manager()
    else:
        support_id = user_id
    if not support_id:
        await call.message.edit_text("К сожалению, сейчас нет свободных операторов. Попробуйте позже.")
        await state.reset_state()

    await state.set_state("wait_in_support")
    await state.update_data(second_id=support_id)
    keyboard = await support.support_keyboard(messages="many", user_id=call.from_user.id)

    await bot.send_message(
        support_id,
        f"С вами хочет связаться пользователь {call.from_user.full_name}",
        reply_markup=keyboard
    )


@dp.callback_query_handler(support.support_callback.filter(messages="many", as_user="no"))
async def answer_support(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    second_id = int(callback_data.get("user_id"))
    user_state = dp.current_state(user=second_id, chat=second_id)

    if str(await user_state.get_state()) != "wait_in_support":
        await call.message.edit_text("К сожалению, пользователь передумал.")
        return

    await state.set_state("in_support")
    await user_state.set_state("in_support")

    await state.update_data(second_id=second_id)

    keyboard = cancel_keyboard(second_id)
    keyboard_second_user = cancel_keyboard(call.from_user.id)

    await call.message.edit_text("Вы на связи с пользователем!\n"
                                 "Чтобы завершить общение нажмите на кнопку.",
                                 reply_markup=keyboard)
    await bot.send_message(second_id, "Техподдержка на связи! Можете писать сюда свое сообщение. \n"
                                      "Чтобы завершить общение нажмите на кнопку.",
                           reply_markup=keyboard_second_user)


@dp.message_handler(state="wait_in_support", content_types=types.ContentTypes.ANY)
async def not_supported(message: types.Message, state: FSMContext):
    data = await state.get_data()
    second_id = data.get("second_id")
    await message.answer("Дождитесь ответа оператора или отмените сеанс",
                         reply_markup=support.cancel_keyboard(second_id))


@dp.callback_query_handler(support.cancel_support.filter(), state=["in_support", "wait_in_support", None])
async def exit_support(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = int(callback_data.get("user_id"))
    second_state = dp.current_state(user=user_id, chat=user_id)

    if await second_state.get_state() is not None:
        await second_state.reset_state()
        await bot.send_message(user_id, "Пользователь завершил сеанс техподдержки")

    await call.message.edit_text("Вы завершили сеанс.")
    await state.reset_state()
