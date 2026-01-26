from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from main import telegram_user_id

from app.keyboards.start_inline import start_inline_keyboard

application_router = Router()

class ApplicationState(StatesGroup):
    Name = State()
    Number = State()

@application_router.callback_query(F.data == "application")
async def application_callback_query(callback: CallbackQuery,
                                     state: FSMContext):
    await callback.answer()

    await state.clear()
    await state.set_state(ApplicationState.Name)
    await callback.message.answer( "📝 <b>Запись на курс</b>\n\n"
                                  "👤 Напишите ваше <b>имя</b>:",
                                   parse_mode='HTML')

@application_router.message(ApplicationState.Name)
async def application_name(message: types.Message,
                           state: FSMContext):
    name = (message.text or "").strip()

    if len(name) < 2:
        await message.answer("⚠️ Имя слишком короткое. Напишите имя ещё раз:")
        return

    await state.update_data(name=name)
    await state.set_state(ApplicationState.Number)

    await message.answer("📞 Теперь напишите ваш <b>номер телефона</b> (пример: +7 777 123 45 67):",
                         parse_mode='HTML')

@application_router.message(ApplicationState.Number)
async def application_number(message: types.Message,
                             state: FSMContext):
    number = (message.text or "").strip()

    cleaned = number.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if len(cleaned) < 6:
        await message.answer("⚠️ Похоже на неверный номер. Введите номер ещё раз:")
        return

    await state.update_data(number=number)
    data_application = await state.get_data()

    name = data_application.get("name", "—")
    number = data_application.get("number", "—")

    user_id= message.from_user.id
    username = message.from_user.username or "нет username"

    bot = message.bot

    await bot.send_message(
        chat_id=telegram_user_id,
        text=(
            "📩 <b>Новая заявка на курс</b>\n\n"
            f"👤 Имя: <b>{name}</b>\n"
            f"📞 Телефон: <b>{number}</b>\n"
            f"🧾 Username: @{username}\n"
            f"🆔 ID: <code>{user_id}</code>"
        ),
        parse_mode='HTML'
    )

    await message.answer(
        "✅ <b>Заявка отправлена!</b>\n\n"
        "Я передал ваши данные менеджеру. Скоро с вами свяжутся 🙂",
        reply_markup=start_inline_keyboard(),
        parse_mode="HTML"
    )

    await state.clear()







