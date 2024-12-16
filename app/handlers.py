from ftplib import all_errors
from pyexpat.errors import messages

import aiogram
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.keyboards import start_kb, admin_kb, category_kb, add_to_cart, to_cart_kb, cart_inl, cart_repl, get_phone
from app.keyboards import categories
from database.database import registration, show_catalog, add_item, if_admin, add_to_cart_db, show_cart_db, get_item_db, clear_cart_db, get_check
from config import CHAT_ID

router = Router()
from main import bot

class myStates(StatesGroup):
    category = State()
    name = State()
    price = State()
    photo = State()

class toOrder(StatesGroup):
    email = State()
    phone = State()
    category = State()

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
async def about_us(message: Message):
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

@router.callback_query(F.data == 'show_items')
async def show_all_items(callback: CallbackQuery):
    data = show_catalog()
    await callback.message.answer_photo(photo=f'{data[0][2]}', caption = f"{data[0][1]}\n{data[0][3]}")

@router.message(F.text == 'Каталог 🛍️')
async def show_items_by_cat(message: Message, state: FSMContext):
    await state.set_state(toOrder.category)
    await message.answer('Выберите категорию', reply_markup=await category_kb())

@router.message(toOrder.category)
async def show_items_by_cat_final(message: Message, state: FSMContext):
    if message.text in categories:
        await state.clear()
        data = show_catalog(message.text)
        if data:
            for item in data:
                await message.answer_photo(photo=f'{item[2]}', caption = f"{item[1]}\n{item[3]} BYN", reply_markup=add_to_cart)
        else:
            await message.answer('В выбранной категории товаров нет')
    else:
        await message.answer('Неверно указанная категория. Выберите категорию из списка ниже', reply_markup=await category_kb())

@router.callback_query(F.data == 'add_to_cart')
async def add_item_to_cart(callback: CallbackQuery):
    item_data = callback.message.caption.split("\n")
    add_to_cart_db(callback.from_user.id, item_data[0], item_data[1])
    await callback.message.answer("Товар добавлен в корзину", reply_markup=to_cart_kb)

@router.message(F.text == 'Корзина 🛒')
async def show_cart(message: Message):
    cart = show_cart_db(message.from_user.id)
    sum = 0
    if len(cart) == 0:
        await message.answer('Корзина пуста')
    else:
        for item in cart:
            item_info = get_item_db(item[2])
            sum += (item_info[0][3] * item[4])
            await message.answer_photo(photo=item_info[0][2], caption = f"{item_info[0][1]}\n{item_info[0][3]} BYN\n{item[4]} шт.")#, reply_markup=cart_inl)
        await message.answer(f"Сумма: {sum} BYN", reply_markup=cart_repl)

@router.message(F.text == 'Очистить корзину 🥶')
async def clear_cart(message: Message):
    clear_cart_db(message.from_user.id)
    await message.answer("Корзина очищена")

@router.message(F.text == 'Оформить заказ 😈')
async def make_order(message: Message, state: FSMContext):
    await state.set_state(toOrder.phone)
    await message.answer('Укажите свой номер телефона', reply_markup=get_phone)

@router.message(toOrder.phone)
async def make_order2(message: Message, state: FSMContext):
    await state.update_data(name=message.contact.first_name)
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(toOrder.email)
    await message.answer('Введите почту.\nБудьте внимательны. На почту придет код')

@router.message(toOrder.email)
async def make_order_final(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    data = await state.get_data()
    # await message.answer(f"{data}")
    await state.clear()
    check = get_check(message.from_user.id)
    await message.answer('Спасибо за заказ!\nОжидайте свой код на почте в течение 24 лет')
    await message.answer(check)
    await bot.send_message(chat_id=CHAT_ID, text=f'Новый заказ\n{check}\n{data['name']}\n{data['phone']}\n{data['email']}')
    data = await state.get_data()
    clear_cart_db(message.from_user.id)
