import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import requests
from dotenv import load_dotenv
from aiogram.types import ParseMode

dotenv_path = './app/.env'
load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
API_URL = os.getenv('API_URL')

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
user_tokens = {}


class Query(StatesGroup):
    term = State()

@dp.message_handler(Command('start'))
async def start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Помощь"),
            types.KeyboardButton(text="Задать вопрос"),
            #types.KeyboardButton(text="Последние новости"])
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    await message.answer(f"Привет, {message.from_user.first_name}! Я помогу тебе узнать любую информацию про университет"
                         f"ИТМО\n Ты можешь узнать последние новости, получить ответ на свой вопрос от языковой модели"
                         f"с указанием внешних источников", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text.lower() == 'помощь', state="*")
async def help(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! Я помогу тебе узнать любую информацию про университет"
        f"ИТМО\n Ты можешь получить ответ на свой вопрос от языковой модели"
        f"с указанием внешних источников")
    

@dp.message_handler(lambda message: message.text.lower() == 'задать вопрос', state="*")
async def query(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Пожалуйста, напишите Ваш вопрос с вариантами ответа")
    await state.set_state(Query.term)

@dp.message_handler(state=Query.term)
async def complete_query(message: types.Message, state: FSMContext):
    term = message.text
    json_raw = {
        "id": 1,
        "query": term
    }
    response = requests.post(f"{API_URL}/api/request", json=json_raw)

    if response.status_code == 200:
        data = response.json()
        print(data)
        answer = data['answer']
        reasoning = data['reasoning']
        sources = "\n".join([str(source) for source in data['sources']])

        await message.answer(
            f"Ответ: {answer}\nПричина: {reasoning}\nИсточники: {sources}",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await message.answer(f"Ошибка при запросе: {response.status_code}")

    await state.finish()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
