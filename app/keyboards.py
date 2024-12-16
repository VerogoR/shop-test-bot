from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

to_cart_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Корзина 🛒')]
], one_time_keyboard=True, resize_keyboard=True)

start_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог 🛍️')],
    [KeyboardButton(text='Корзина 🛒'), KeyboardButton(text='О нас 📞')]
], resize_keyboard=True, one_time_keyboard=True)

add_to_cart = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить в корзину 💰', callback_data='add_to_cart')]
])

cart_inl = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='➕', callback_data='plusOne'),
     InlineKeyboardButton(text='🗑️', callback_data='clear'),
     InlineKeyboardButton(text='➖', callback_data='minusOne')]
], resize_keyboard=True)

cart_repl = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Очистить корзину 🥶')],
    [KeyboardButton(text='Оформить заказ 😈')]
], resize_keyboard=True, one_time_keyboard=True)

admin_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить айтем', callback_data='add_item')],
    [InlineKeyboardButton(text='Показать все айтемы', callback_data='show_items')],
    [InlineKeyboardButton(text='Показать заказы', callback_data='show_orders')],
    [InlineKeyboardButton(text='Добавить админа', callback_data='make_admin')]
], resize_keyboard=True)


categories = ['Genshin Impact', 'Brawl Stars', 'Roblox', 'Minecraft', 'Valorant', 'Fortnite']
async def category_kb():
    keyboard = ReplyKeyboardBuilder()
    for cat in categories:
        keyboard.add(KeyboardButton(text=cat))
    return keyboard.adjust(2).as_markup(one_time_keyboard=True, resize_keyboard=True)

# show_option_kb = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='По категории', callback_data='by_cat')],
#     [InlineKeyboardButton(text='Все', callback_data='no_cat')]
# ], resize_keyboard=True)