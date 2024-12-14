import aiogram
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.keyboards import start_kb

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!\nС помощью этого бота ты сможешь купить "
                         f"аккаунты Minecraft почти без обмана ;)\n"
                         f"Воспользуйся кнопками ниже 👇👇👇", reply_markup=start_kb)
