from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


import app.keyboards.start_inline as start_inline
from app.utils.gpt import response_ai

start_router = Router()


class LevelTest(StatesGroup): #FSM for AI response
    waiting_for_text = State()
    processing = State()


@start_router.message(Command('start'))
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer(f"👋 Здравствуйте!\n"
                         f"Я — AI-ассистент курсов английского языка <b>Kabiev_English</b>\n\n"
                         f"Я помогу вам:\n"
                         f"• бесплатно определить ваш уровень английского\n"
                         f"• рассказать о наших курсах и формате обучения\n\n"
                         f"Вы можете прямо сейчас пройти короткую проверку уровня — просто написать текст о себе на английском ✍️\n"
                         f"С чего начнём? 👇",
                         parse_mode="html",
                         reply_markup=start_inline.start_inline_keyboard()
    )
    await state.clear()

@start_router.callback_query(F.data == 'check')
async def check_handler(callback: types.CallbackQuery,
                        state: FSMContext):
    await callback.answer("")
    await state.set_state(LevelTest.waiting_for_text)

    await callback.message.answer(
        "🔍 Отлично! Давайте проверим ваш уровень английского.\n\n"
        "✍️ Напишите текст о себе на английском языке "
        "(примерно 150–200 слов).\n\n"
        "Можно рассказать:\n"
        "• кто вы\n"
        "• чем занимаетесь\n"
        "• зачем учите английский\n\n"
        "Я проанализирую текст и подскажу ваш примерный уровень 😊"
    )

@start_router.message(LevelTest.waiting_for_text)
async def take_answer_handler(message: types.Message,
                              state: FSMContext):

    await state.set_state(LevelTest.processing)
    await state.update_data(text=message.text)
    data = await state.get_data()
    text_user = data['text']

    response_text = response_ai(text_user)

    await message.answer(
        f"{response_text}\n\n"
        "📩 Хотите продолжить обучение?\n"
        "Нажмите кнопку ниже, чтобы оставить заявку на курс 👇",
        parse_mode="html",
        reply_markup=start_inline.application_keyboard()
    )

    await state.clear()

@start_router.message(LevelTest.processing)
async def ignore_message(message: types.Message):
    pass

@start_router.callback_query(F.data == 'back_to_main')
async def back_to_main_handler(callback: types.CallbackQuery,
                               state: FSMContext):
    await callback.answer()

    await callback.message.answer(f"🔙 Вы вернулись в главное меню\n\n"
                                  f"Вы можете снова проверить уровень английского или узнать информацию о курсе 👇",
                                  reply_markup=start_inline.start_inline_keyboard())
    await state.clear()










