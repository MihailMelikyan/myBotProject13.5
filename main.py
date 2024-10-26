from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text="Расcчитать")
button2 = KeyboardButton(text="Информация")
kb.row(button1,button2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def set_age(message):
    await message.answer('Привет я бот помощник и я помогу тебе считать калории!', reply_markup=kb)

@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Бот поможет следить за калориями v.1.0',reply_markup=kb)


@dp.message_handler(text='Расcчитать')
async def set_growth(message):
    await message.answer('Введите свой возраст:', reply_markup=kb)
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calorie_norm = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age'])
    await message.answer(f'Ваша норма калорий {calorie_norm}')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
