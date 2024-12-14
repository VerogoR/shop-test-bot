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

@router.message(F.text == "Каталог 🛒")
async def catalog(message: Message):
    # work with DB
    await message.answer("Здесь будет каталог\n(Как только я доделая БДшки)")

@router.message(F.text == "Корзина 🎰")
async def cart(message: Message):
    # work with DB
    await message.answer("Здесь будет корзина\n(Как только я доделая БДшки)")

@router.message(F.text == "О нас 📵")
async def aboutUs(message: Message):
    await message.answer("Мы почти самый честный магазин аккаунтов Minecraft.\nТолько у нас Вы можете приобрести аккаунты"
                         "с различными плюшками по самой дорогой цене.\nК каждому заказу в подарок идет шанс"
                         "блокировки аккаунта на всегда.\nПо всем вопросом вы никуда не сможете обратиться.")
