import aiogram
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.keyboards import start_kb, admin_kb
from database.database import registration, show_catalog, add_item, if_admin
from config import CHAT_ID

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    registration(message.from_user.id, message.from_user.first_name, message.from_user.username)
    await message.answer(f"Привет, {message.from_user.first_name}!\nС помощью этого бота ты сможешь купить "
                         f"валюту в различных играх ;)\n"
                         f"Воспользуйся кнопками ниже 👇👇👇", reply_markup=start_kb)

@router.message(F.text == "Каталог 🛒")
async def catalog(message: Message):
    # work with DB
    await message.answer(show_catalog())

@router.message(F.text == "Корзина 🎰")
async def cart(message: Message):
    # work with DB
    await message.answer("Здесь будет корзина\n(Как только я доделая БДшки)")

@router.message(F.text == "О нас 📞")
async def aboutUs(message: Message):
    await message.answer("Цифровая Пещера — это ваш надежный источник виртуальной валюты "
                         "для всех популярных игр!\nНаша цель — предоставить вам быстрый"
                         " и удобный способ увеличить свой игровой баланс без "
                         "лишних хлопот и долгих ожиданий.\nВ нашем магазине вы найдете: \n"
                         "- Широкий ассортимент валюты: Мы предлагаем игровые монеты, золото, и другие ресурсы"
                         " для множества популярных игр.\n"
                         "- Молниеносные транзакции: Получите свои виртуальные богатства в кратчайшие"
                         " сроки благодаря нашей оперативной службе доставки.\n"
                         "- Конфиденциальность и безопасность: Вся информация о транзакциях"
                         " защищена и полностью конфиденциальна.\n- Доступные цены: Мы предлагаем "
                         "самые выгодные курсы для наших клиентов, чтобы вы могли наслаждаться игрой "
                         "на полную мощь без значительных затрат.\nЗайдите к нам сегодня"
                         " и испытайте новый уровень игры с Цифровая Пещера!")


@router.message(Command("admin"))
async def admin(message: Message):
    if if_admin(message.from_user.id)[0][0] == 1:
        await message.answer('Активирована админ панель.\nВыберите действие', reply_markup=admin_kb)
    else:
        await message.answer("Доступ запрещен")
