import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.app_register.settings')
django.setup()

from asgiref.sync import sync_to_async
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.app_register.settings import TELEGRAM_BOT_API
from django.contrib.auth.models import User


# State creation
class Register(StatesGroup):
    first_name = State()
    last_name = State()
    password = State()


storage = MemoryStorage()


bot = Bot(TELEGRAM_BOT_API)
dp = Dispatcher(bot, storage=storage)

btn_register = KeyboardButton('Start Registration')
btn_cancel_register = KeyboardButton('Cancel register')

keyboards = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
)
keyboards.add(btn_register, btn_cancel_register)


async def on_startup(_):
    print('Bot it\'s the work')


# user existence check
async def check_user_exists(username: int) -> bool:
    try:
        user = await sync_to_async(User.objects.get)(username=username)
        return True
    except User.DoesNotExist:
        return False


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        f'Hello {message.from_user.first_name}.\n'
        'This is a registration bot.\n'
        'Press the button to register',
        reply_markup=keyboards
    )
    await message.delete()


@dp.message_handler(Text(equals='Cancel register', ignore_case=True),
                    state=[Register.first_name, Register.last_name,
                           Register.password])
async def cancel_register(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(
        message.from_user.id,
        'Registration cancel successfully',
        reply_markup=keyboards
    )


@dp.message_handler(Text(equals='Start Registration', ignore_case=True))
async def register_command(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'For registration, please specify:\n'
        'Name;',
        reply_markup=keyboards
    )
    await Register.first_name.set()


@dp.message_handler(state=Register.first_name)
async def get_first_name(message: types.Message, state: FSMContext):
    await state.update_data({"first_name": message.text})
    await bot.send_message(
        message.from_user.id,
        f'Now {message.from_user.first_name} please specify:\n'
        'surname',
        reply_markup=keyboards
    )
    await Register.last_name.set()


@dp.message_handler(state=Register.last_name)
async def get_last_name(message: types.Message, state: FSMContext):
    await state.update_data({"last_name": message.text})
    await bot.send_message(
        message.from_user.id,
        f'Теперь {message.from_user.first_name} укажи пожалуйста:\n'
        'Пароль',
        reply_markup=keyboards
    )
    await Register.password.set()


@dp.message_handler(state=Register.password)
async def get_password(message: types.Message, state: FSMContext):
    await state.update_data({"password": message.text})
    await bot.send_message(message.from_user.id, 'Data saved',)

    data = await state.get_data()
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    password = data.get('password', '')

    if await check_user_exists(message.from_user.username):
        await bot.send_message(
            message.from_user.id,
            'There is already a user with this nickname'
        )

    create_user_sync = sync_to_async(User.objects.create_user)
    user = await create_user_sync(
        first_name=first_name,
        last_name=last_name,
        password=password,
        username=message.from_user.username,
    )
    await bot.send_message(
        message.from_user.id,
        'User successfully created\n'
        'You can login with this link'
    )
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)