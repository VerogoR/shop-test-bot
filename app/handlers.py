from pyexpat.errors import messages

import aiogram
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.keyboards import start_kb, admin_kb, category_kb
from app.keyboards import categories
from database.database import registration, show_catalog, add_item, if_admin
from config import CHAT_ID

router = Router()

class myStates(StatesGroup):
    category = State()
    name = State()
    price = State()
    photo = State()

class toOrder(StatesGroup):
    email = State()
    phone = State()

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

@router.callback_query(F.data == 'add_item')
async def add_item1(callback: CallbackQuery, state: FSMContext):
    await state.set_state(myStates.category)
    await callback.message.answer("Укажите категорию товара", reply_markup=await category_kb())

@router.message(myStates.category)
async def add_item2(message: Message, state: FSMContext):
    if message.text in categories:
        await state.update_data(item_category=message.text)
        await state.set_state(myStates.name)
        await message.answer('Отлично. Теперь укажите название товара')
    else:
        await message.answer('Неверно указанная категория. Выберите категорию из списка ниже', reply_markup=await category_kb())

@router.message(myStates.name)
async def add_item3(message: Message, state: FSMContext):
    await state.update_data(item_name=message.text)
    await state.set_state(myStates.photo)
    await message.answer('Отлично. Теперь отправьте фото товара (картинку или ссылку)')

@router.message(myStates.photo)
async def add_item4(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(item_photo=message.text)
    else:
        await state.update_data(item_photo=message.photo[-1].file_id)
    await state.set_state(myStates.price)
    await message.answer('Отлично. Теперь укажите стоимость товара (целое число в BYN)')

@router.message(myStates.price)
async def add_item5(message: Message, state: FSMContext):
    await state.update_data(item_price=message.text)
    data = await state.get_data()
    await message.answer('Все данные получены. Загрузка в базу')
    add_item(name=data['item_name'], price=data['item_price'], photo=data['item_photo'], category=data['item_category'])
    await state.clear()

# @router.callback_query(F.data == 'show_items')
# async def show_items(callback: CallbackQuery, state: FSMContext):
#     await callback.message.edit_text('Выберите тип вывода',)