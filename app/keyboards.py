from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from config import admin_ids
import app.database as db
async def mainkb(userid):
    main = InlineKeyboardBuilder()
    main.add(InlineKeyboardButton(text="👔 Общий Каталог",callback_data='allproduct'))
    main.add(InlineKeyboardButton(text="🧢 Каталог",callback_data="catalog"))
    main.add(InlineKeyboardButton(text="🗑️ Корзина",callback_data='cart'))
    main.add(InlineKeyboardButton(text="📞 Связь",callback_data='contact'))
    if userid in admin_ids:
        main.add(InlineKeyboardButton(text="🔒 Админ Панель",callback_data='adminpanel'))
        return main.adjust(2).as_markup()
    else:
        return main.adjust(2).as_markup()


adminpanel = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Добавить товар",callback_data="regproduct"),
                                                    InlineKeyboardButton(text="Удалить товар",callback_data="delproduct")],
                                                   [InlineKeyboardButton(text="Добавить бренд",callback_data="regbrand"),
                                                    InlineKeyboardButton(text="Удалить бренд",callback_data="delbrand")],
                                                   [InlineKeyboardButton(text="Добавить категорию",callback_data="regcategory"),
                                                    InlineKeyboardButton(text="Удалить категорию",callback_data="delcategory")],
                                                   [InlineKeyboardButton(text="Создать обьявление",callback_data="notificateall")],
                                                   [InlineKeyboardButton(text="Просмотреть текущие тикеты",callback_data="showtickets")],
                                                   [InlineKeyboardButton(text="⏪ Отмена",callback_data="main")]])



confirmnotify = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="Подтвердить",callback_data="confirmnotify")
],[InlineKeyboardButton(text="Отмена",callback_data="adminpanel")]])

genders = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Мужской"),
         KeyboardButton(text="Женский"),]],resize_keyboard=True)

cancel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Главное меню',callback_data='main')]
])

cartmenu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⏪ Назад",callback_data='cart')]
])
adminpanelcancel = InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton(text="⏪ Назад",callback_data="adminpanel")]])

add_brand = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить бренд",callback_data="regbrand")]
])
add_category = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить категорию",callback_data="regcategory")]
])

confirm_clear = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да",callback_data="yesclear"),InlineKeyboardButton(text="⏪ Отмена",callback_data="cart")]
])

cart = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="👁️‍ Просмотр",callback_data="showcart")],
    [InlineKeyboardButton(text="Удалить товар",callback_data="clearitem"),
    InlineKeyboardButton(text="🚮 Очистить всё",callback_data="clearcart")],
    [InlineKeyboardButton(text="⏪ Назад",callback_data="main")]
])
async def reply_brands(brands):
    keyboard = ReplyKeyboardBuilder()
    for brand in brands:
        keyboard.add(KeyboardButton(text=brand[1]))
    return keyboard.adjust(2).as_markup(resize_keyboard=True)


async def create_product_buttons(products, page=1, items_per_page=6):
    keyboard = InlineKeyboardBuilder()
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_products = products[start_idx:end_idx]
    page_products = reversed(page_products)
    for product in page_products:
        button = InlineKeyboardButton(text=f"{product[6]} {product[1]} {product[3]}с", callback_data=f"product_{product[0]}")
        keyboard.add(button)

    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⏪ Предыдущая", callback_data=f"page_{page - 1}"))

    if end_idx < len(products):
        navigation_buttons.append(InlineKeyboardButton(text="Следующая ⏩", callback_data=f"page_{page + 1}"))

    if navigation_buttons:
        keyboard.row(*navigation_buttons)

    keyboard.add(InlineKeyboardButton(text="Отмена", callback_data='main'))
    return keyboard.adjust(2).as_markup()
async def create_delete_product_buttons(products):
    keyboard = InlineKeyboardBuilder()
    for product in products:
        keyboard.add(InlineKeyboardButton(text=product[1], callback_data=f"delproduct_{product[0]}"))
    keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="adminpanel"))
    return keyboard.adjust(2).as_markup()

async def create_ticket_buttons(tickets):
    keyboard = InlineKeyboardBuilder()
    for ticket in tickets:
        keyboard.add(InlineKeyboardButton(text=str(ticket[1]), callback_data=f"viewoneticket_{ticket[0]}"))
    keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="adminpanel"))
    return keyboard.adjust(2).as_markup()

async def create_delete_brand_buttons(brands):
    keyboard = InlineKeyboardBuilder()
    for brand in brands:
        keyboard.add(InlineKeyboardButton(text=brand[1], callback_data=f"delbrand_{brand[0]}"))
    keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="adminpanel"))
    return keyboard.adjust(3).as_markup()

async def create_delete_category_buttons(categories):
    keyboard = InlineKeyboardBuilder()
    for cat in categories:
        keyboard.add(InlineKeyboardButton(text=cat[1], callback_data=f"delcategory_{cat[0]}"))
    keyboard.add(InlineKeyboardButton(text="Отмена",callback_data="adminpanel"))
    return keyboard.adjust(3).as_markup()

async def create_clear_item_buttons(cart):
    keyboard = InlineKeyboardBuilder()
    for item in cart:
        keyboard.add(InlineKeyboardButton(text=item[1], callback_data=f"delitem_{item[0]}"))
    keyboard.add(InlineKeyboardButton(text="Отмена",callback_data="cart"))
    return keyboard.adjust(1).as_markup()
async def show_products(product_id):
    buttons = InlineKeyboardBuilder()
    buttons.add(InlineKeyboardButton(text="В корзину", callback_data=f"addtocart_{product_id}"))
    return buttons.adjust(1).as_markup()

async def show_one_ticket(ticket_id):
    buttons = InlineKeyboardBuilder()
    buttons.add(InlineKeyboardButton(text="Ответить и закрыть", callback_data=f"answerticket_{ticket_id}"))
    buttons.add(InlineKeyboardButton(text="Закрыть не отвечая", callback_data=f"deleteticket_{ticket_id}"))
    buttons.add(InlineKeyboardButton(text='Отмена', callback_data=f"showtickets"))
    return buttons.adjust(1).as_markup()