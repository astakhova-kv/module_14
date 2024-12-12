from itertools import product

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from crud_functions import *

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb_1 = ReplyKeyboardMarkup(
    keyboard=[
            [KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация')],
            [KeyboardButton(text='Купить')]
    ], resize_keyboard=True
)


kb_2 = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
        InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
    ]
)


kb_3 = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text='Продукт 1', callback_data='product_buying'),
        InlineKeyboardButton(text='Продукт 2', callback_data='product_buying'),
        InlineKeyboardButton(text='Продукт 3', callback_data='product_buying'),
        InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')]
    ]
)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb_1)


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_2)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = get_all_products()
    for product in products:
        id, title, description, price = product
        with open(f'{id}.jpeg', 'rb') as img:
            await message.answer(f'Название: {title} | Описание: {description} | Цена: {price} ')
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки: ', reply_markup=kb_3)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('''для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;
для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.''')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


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
async def set_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    resoult = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
    await message.answer(f'Ваша норма калорий {resoult}')
    await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    initiate_db()
    executor.start_polling(dp, skip_updates=True)
