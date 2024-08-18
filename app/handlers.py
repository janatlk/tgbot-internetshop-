from aiogram import F,Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb
from app import database as db
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext
from config import admin_ids


router = Router()

class RegisterProduct(StatesGroup):
    title = State()
    description = State()
    price = State()
    photo = State()
    gender = State()
    brand = State()
    category = State()
class RegisterBrand(StatesGroup):
    name_brand = State()
class RegisterCategory(StatesGroup):
    name_category = State()

class RegisterTicket(StatesGroup):
    text = State()

class FilterProducts(StatesGroup):
    gender = State()
    brand = State()
    category = State()

class RegNotification(StatesGroup):
    text = State()
class AnswerTicket(StatesGroup):
    ticket = State()
    text = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await db.cmd_start_db(message.from_user.id)
    if message.from_user.id in admin_ids:
        await message.answer(f"Здравствуйте, {message.from_user.full_name}, ваша роль Админ",
                            reply_markup=await kb.mainkb(message.from_user.id))
    else:
        await message.answer(f"Hello, your id {message.from_user.id}",
                             reply_markup=await kb.mainkb(message.from_user.id))


@router.callback_query(F.data == 'allproduct')
async def show_catalog(callback: CallbackQuery):
    await callback.message.edit_text(text="Выберите товар",reply_markup=await kb.create_product_buttons(await db.get_all_products()))

# ---------------------- Обработчик элементов ----------------------- #

@router.callback_query(lambda query: query.data.startswith('page_'))
async def paginate_products(callback_query: CallbackQuery):
    page = int(callback_query.data.split('_')[1])
    products = await db.get_all_products()

    await callback_query.message.edit_text("Выберите товар",reply_markup=await kb.create_product_buttons(products,page=page))
    await callback_query.answer()

@router.callback_query(lambda query: query.data.startswith('viewoneticket_'))
async def show_one_ticket(callback_query: CallbackQuery):
    ticketid = int(callback_query.data.split('_')[1])
    tickets = await db.get_all_tickets()

    await callback_query.message.edit_text("Выберите действие",reply_markup=await kb.show_one_ticket(ticketid))
    await callback_query.answer()



@router.callback_query(lambda query: query.data.startswith('product_'))
async def process_product_button(callback_query: CallbackQuery):
    product_id = int(callback_query.data.split('_')[1])
    product = await db.get_product_by_id(product_id)
    product_info = f"Название: {product[1]}\nОписание: \n{product[2]}\n\nЦена: {product[3]} сом\nПол: {product[5]}\nБренд: {product[6]}\nКатегория: {product[7]}."
    await callback_query.message.answer_photo(product[4],caption=product_info,reply_markup=await kb.show_products(product[0]))
    await callback_query.answer()



@router.callback_query(F.data == 'delproduct')
async def show_delete_product_menu(callback: CallbackQuery):
    products = await db.get_all_products()
    if products:
        await callback.message.edit_text("Выберите продукт для удаления:", reply_markup=await kb.create_delete_product_buttons(products))
    else:
        await callback.message.edit_text("Нет доступных продуктов для удаления.")
    await callback.answer()

@router.callback_query(lambda query: query.data.startswith('delproduct_'))
async def delete_product(callback_query: CallbackQuery):
    product_id = int(callback_query.data.split('_')[1])

    # Удаляем продукт по его ID
    await db.delete_product_by_id(product_id)

    await callback_query.answer('Продукт успешно удалён.')
    await callback_query.message.edit_text("Выберите действие", reply_markup=kb.adminpanel)

@router.callback_query(F.data == 'delbrand')
async def show_delete_brands_menu(callback: CallbackQuery):
    brands = await db.get_all_brands()
    if brands:
        await callback.message.edit_text("Выберите бренд для удаления:", reply_markup=await kb.create_delete_brand_buttons(brands))
    else:
        await callback.message.edit_text("Нет доступных брендов для удаления.")
    await callback.answer()

@router.callback_query(lambda query: query.data.startswith('delbrand_'))
async def delete_brand(callback_query: CallbackQuery):
    brandid = int(callback_query.data.split('_')[1])

    # Удаляем продукт по его ID
    await db.delete_brand_by_id(brandid)

    await callback_query.answer('Бренд успешно удалён.')
    await callback_query.message.edit_text("Выберите действие", reply_markup=kb.adminpanel)

@router.callback_query(F.data == 'delcategory')
async def show_delete_category_menu(callback: CallbackQuery):
    categories = await db.get_all_categories()
    if categories:
        await callback.message.edit_text("Выберите категорию для удаления:", reply_markup=await kb.create_delete_category_buttons(categories))
    else:
        await callback.message.edit_text("Нет доступных категорий для удаления.")
    await callback.answer()

@router.callback_query(lambda query: query.data.startswith('delcategory_'))
async def delete_category(callback_query: CallbackQuery):
    catid = int(callback_query.data.split('_')[1])

    # Удаляем продукт по его ID
    await db.delete_category_by_id(catid)

    await callback_query.answer('Категория успешно удалён.')
    await callback_query.message.edit_text("Выберите действие", reply_markup=kb.adminpanel)
    # --------------------- #

@router.callback_query(F.data == 'contact')
async def contact_menu(callback: CallbackQuery, state: FSMContext):
    tickets = await db.get_all_tickets()
    ids = []
    for i in tickets:
        ids.append(i[1])
    if callback.from_user.id not in ids:
        await callback.message.answer("Напишите ваш вопрос, жалобу, предложение. Уместите в одно сообщение.",reply_markup=kb.cancel)
        await state.set_state(RegisterTicket.text)
    else:
        await callback.answer("На ваше имя уже зарегистрирован запрос, пожалуйста дождитесь пока администраторы вам ответят.")
@router.message(RegisterTicket.text)
async def register_ticket(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer("Администратор уведомлен, он ответит в ближайшее время.",reply_markup=kb.cancel)
    data = await state.get_data()
    await db.create_user_ticket(message.from_user.id, data['text'])
    await state.clear()
@router.callback_query(F.data == "catalog")
async def s2how_catalog(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы выбрали Каталог с фильтрами')
    await callback.message.delete()
    await callback.message.answer('Выберите пол',reply_markup=kb.genders)
    await state.set_state(FilterProducts.gender)


@router.message(FilterProducts.gender)
async def filter1(message: Message, state: FSMContext):
    if message.text == "Мужской" or message.text == "Женский":
        await state.update_data(gender=message.text)
        await message.answer("Выберите бренд продукта",reply_markup=await kb.reply_brands(await db.get_all_brands()))
        await state.set_state(FilterProducts.brand)
    else:
        await message.reply("Выберите с помощью кнопок.", reply_markup=kb.genders)
        await state.set_state(FilterProducts.gender)

@router.message(FilterProducts.brand)
async def filter2(message: Message, state: FSMContext):
    brands = await db.get_all_brands()
    brands1 = []
    for i in brands:
        brands1.append(i[1])
    if message.text in brands1:
        await state.update_data(brand=message.text)
        await state.set_state(FilterProducts.category)
        await message.answer("Выберите категорию продукта",reply_markup=await kb.reply_brands(await db.get_all_categories()))
    else:
        await message.reply("Такого бренда нет в базе данных")
        await state.set_state(FilterProducts.brand)


@router.message(FilterProducts.category)
async def filter3(message: Message, state: FSMContext):
    category = await db.get_all_categories()
    categories1 = []
    for i in category:
        categories1.append(i[1])
    if message.text in categories1:
        await state.update_data(category=message.text)
        data = await state.get_data()
        try:
            filter = await db.filter_product(data['gender'],data['brand'],data['category'])
            await message.answer(f"Выберите один из продуктов",reply_markup=await kb.create_product_buttons(filter))
        except IndexError:
            await message.answer("Товаров с выбранными параметрами не найдено.",reply_markup=await kb.mainkb(message.from_user.id))
        await state.clear()
    else:
        await message.reply("Такой категории ещё нет в базе данных")
        await state.set_state(FilterProducts.category)


@router.callback_query(F.data == "main")
async def main(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы вернулись')
    try:
        await callback.message.edit_text('Выберите действие',reply_markup=await kb.mainkb(callback.from_user.id))
        await state.clear()
    except Exception as e:
        await callback.message.answer('Выберите действие',reply_markup=await kb.mainkb(callback.from_user.id))
@router.callback_query(F.data == "cart")
async def cart(callback: CallbackQuery):
    await callback.message.edit_text('Выберите действие',reply_markup=kb.cart)
####### ADMIN REGISTERS ############################################################
################################################################################
################################################################################
@router.callback_query(F.data == "adminpanel")
async def adminpanel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Добро пожаловать в Админ-Панель')
    await callback.message.edit_text('Выберите действие',reply_markup=kb.adminpanel)

@router.callback_query(F.data == "regbrand")
async def reg1(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in admin_ids:
        await state.set_state(RegisterBrand.name_brand)
        await callback.message.edit_text("Введите название добавляемого бренда",reply_markup=kb.adminpanelcancel)
    else:
        await callback.answer("Вам недоступна эта команда")
        await state.clear()

@router.message(RegisterBrand.name_brand)
async def regbrand1(message: Message, state:FSMContext):
    await state.update_data(name_brand=message.text)
    data = await state.get_data()
    await db.add_brand(message.text)
    await message.answer(f"Добавлено! {data}",reply_markup=kb.adminpanel)

    await state.clear()

@router.callback_query(F.data == 'regcategory')
async def reg1(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in admin_ids:
        await state.set_state(RegisterCategory.name_category)
        await callback.message.edit_text("Введите название добавляемой категории товаров",reply_markup=kb.adminpanelcancel)
    else:
        await callback.answer("Вам недоступна эта команда")
        await state.clear()


@router.message(RegisterCategory.name_category)
async def regbrand1(message: Message, state: FSMContext):
    await state.update_data(name_category=message.text)
    data = await state.get_data()
    await db.add_category(message.text)
    await message.answer(f"Добавлено! {data}",reply_markup=kb.adminpanel)
    await state.clear()


@router.callback_query(F.data == 'regproduct')
async def reg1(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in admin_ids:
        await state.set_state(RegisterProduct.title)
        await callback.message.edit_text("Введите название модели продукта",reply_markup=kb.adminpanelcancel)
    else:
        await callback.answer("Вам недоступна эта команда")
        await state.clear()




@router.message(RegisterProduct.title)
async def reg2(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(RegisterProduct.description)
    await message.answer("Введите описание продукта")

@router.message(RegisterProduct.description)
async def reg3(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(RegisterProduct.gender)
    await message.answer(
        f"Выберите пол к продукту",
        reply_markup=kb.genders)

@router.message(RegisterProduct.gender)
async def reg4(message: Message, state:FSMContext):
    if message.text == "Мужской" or message.text == "Женский":
        await state.update_data(gender=message.text)
        await state.set_state(RegisterProduct.photo)
        await message.answer(f'Отправьте фото продукта')
    else:
        await message.answer("Невалидные данные используйте кнопки")
        await state.set_state(RegisterProduct.gender)

@router.message(RegisterProduct.photo)
async def reg5(message: Message,state:FSMContext):
    if message.photo is not None:
        await state.update_data(photo=message.photo[-1].file_id)
        await state.set_state(RegisterProduct.price)
        await message.answer("Фото принято! Отправьте цену продукта в сомах (только цифры)")
    else:
        await state.set_state(RegisterProduct.photo)
        await message.answer("Ошибка с принятием фото отправьте валидное фото")

@router.message(RegisterProduct.price)
async def reg6(message: Message,state:FSMContext):
    try:
        price = int(message.text)
        await state.update_data(price=price)
        await message.answer(f"Выберите бренд",reply_markup=await kb.reply_brands(await db.get_all_brands()))
        await state.set_state(RegisterProduct.brand)
    except ValueError:
        await state.set_state(RegisterProduct.price)
        await message.answer('Ошибка введите число без букв')

@router.message(RegisterProduct.brand)
async def reg7(message: Message,state:FSMContext):
    brandslist = []
    brands = await db.get_all_brands()
    for i in brands:
        brandslist.append(i[1])
    if message.text in brandslist:
        await state.update_data(brand=message.text)
        # data = await state.get_data()
        # await db.add_product(data['title'],data['description'],data['price'],data['photo'],data['gender'],'brand','category')
        await message.answer(f"Выберите категорию продукта",reply_markup=await kb.reply_brands(await db.get_all_categories()))
        await state.set_state(RegisterProduct.category)
    else:
        await state.set_state(RegisterProduct.brand)
        await message.reply('Такого бренда не существует в базе данных',reply_markup=kb.add_brand)


@router.message(RegisterProduct.category)
async def reg8(message: Message, state: FSMContext):
    categorylist = []
    categoryes = await db.get_all_categories()
    for i in categoryes:
        categorylist.append(i[1])
    if message.text in categorylist:
        await state.update_data(category=message.text)
        data = await state.get_data()
        await db.add_product(data['title'],data['description'],data['price'],data['photo'],data['gender'],data['brand'],data['category'])
        await message.answer(f"Готово, обьект создан:\n{data}",reply_markup=kb.adminpanel)
        await state.clear()
    else:
        await state.set_state(RegisterProduct.category)
        await message.reply('Такой категории не существует в базе данных', reply_markup=kb.add_category)

@router.callback_query(F.data == "notificateall")
async def notificateall(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id in admin_ids:
        await state.set_state(RegNotification.text)
        await callback.message.answer("Введите сообщение для отправки всем пользователям")
    else:
        await state.clear()
@router.message(RegNotification.text)
async def getnotificationtext(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await message.answer(f"Ваш текст:\n{data['text']}\n\nПодтвердите действие",reply_markup=kb.confirmnotify)

async def send_message_to_user(bot, user_id: int, message: str):
    await bot.send_message(chat_id=user_id, text=message)

@router.callback_query(F.data == 'confirmnotify')
async def confirmnotify(callback: CallbackQuery, state: FSMContext):
    usersids = await db.get_all_user_ids()
    data = await state.get_data()
    for userid in usersids:
        await send_message_to_user(callback.bot, userid[0], data['text'])
    await state.clear()


### TICKET


@router.callback_query(F.data == 'showtickets')
async def showtickets(callback: CallbackQuery):
    tickets = await db.get_all_tickets()
    await callback.message.edit_text("Выберите тикет для взаимодействия",reply_markup=await kb.create_ticket_buttons(tickets))

@router.callback_query(lambda query: query.data.startswith('answerticket_'))
async def answerticket1(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(AnswerTicket.ticket)
    ticketid = int(callback_query.data.split('_')[1])
    ticket = await db.get_ticket_by_id(ticketid)
    await state.update_data(ticket=ticket)
    # Удаляем продукт по его ID
    await callback_query.message.answer(f"""
                                ------------===ЗАПРОС #{ticketid}===-------------\n
        {ticket[2]}\n
    Введите ответ данному пользователю
    """)
    await state.set_state(AnswerTicket.text)
@router.callback_query(lambda query: query.data.startswith('deleteticket_'))
async def deleteticket1(callback_query: CallbackQuery):
    ticketid = int(callback_query.data.split('_')[1])
    userid = await db.get_ticket_by_id(ticketid)
    await send_message_to_user(callback_query.bot,userid,f"Ваш запрос был закрыт без ответа, администратором {callback_query.from_user.full_name}.")
    await db.delete_ticket_by_id(ticketid)
    await callback_query.answer(f"Тикет {ticketid} закрыт без ответа!")
    tickets = await db.get_all_tickets()
    await callback_query.message.edit_text("Выберите тикет для взаимодействия", reply_markup=await kb.create_ticket_buttons(tickets))
@router.message(AnswerTicket.text)
async def answerticket2(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    ticket = data['ticket']
    userid = ticket[1]
    ticketid = ticket[0]
    await send_message_to_user(message.bot, userid, f"Администратор {message.from_user.full_name} ответил вам:\n\n{data['text']}")
    await db.delete_ticket_by_id(ticketid)
    alltickets = await db.get_all_tickets()
    await state.clear()
    await message.answer(f"Ответ был отправлен пользователю. Тикет {ticketid} закрыт",reply_markup=await kb.create_ticket_buttons(alltickets))
#####################################################################
####################################################################
#################################################################


# ================ КОРЗИНА ================================================ #
cart = {}
@router.callback_query(lambda c: c.data.startswith('addtocart_'))
async def add_to_cart(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    product_id = int(callback_query.data.split('_')[1])
    # Получаем товар из базы данных
    product = await db.get_product_by_id(product_id)

    if user_id not in cart:
        cart[user_id] = []
    cart[user_id].append(product)

    await callback_query.message.answer(f"Товар добавлен в корзину (Товаров в корзине: {len(cart[user_id])})",reply_markup=kb.cartmenu)


@router.callback_query(F.data == 'showcart')
async def show_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in cart:
        cartuser = cart[user_id]
        cart_text = "Ваша корзина:\n"
        count = 1
        pricelist = []
        for product in cartuser:
            cart_text += f"{count}. {product[1]} - {product[3]} сом.\n"
            count += 1
            pricelist.append(int(product[3]))
        total = sum(pricelist)
        cart_text += f"\nИтого: {total} сом\n"
        await callback.message.edit_text(cart_text,reply_markup=kb.cartmenu)
    else:
        await callback.answer("Ваша корзина пустая!")

@router.callback_query(F.data == 'clearcart')
async def clear_cart(callback: CallbackQuery):
    if callback.from_user.id in cart:
        await callback.message.edit_text("Подтвердите действие",reply_markup=kb.confirm_clear)
    else:
        await callback.answer("Ваша корзина пустая!")
@router.callback_query(F.data == 'yesclear')
async def yesclear(callback: CallbackQuery):
    user_id = callback.from_user.id
    try:
        del cart[user_id]
        await callback.message.edit_text("Корзина очищена.",reply_markup=kb.cart)
    except KeyError:
        await callback.answer("Корзина пустая.")
        await callback.message.edit_text("Выберите действие",reply_markup=kb.cart)


@router.callback_query(F.data == 'clearitem')
async def clear_item_cart(callback: CallbackQuery):
    try:
        usercart = cart[callback.from_user.id]
        if usercart:
            await callback.message.edit_text("Выберите товар для удаления",reply_markup=await kb.create_clear_item_buttons(usercart))
        else:
            await callback.answer("Корзина пуста.")
    except KeyError:
        await callback.answer("Корзина пуста.")

@router.callback_query(lambda c: c.data.startswith('delitem_'))
async def clear_item_func(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    item_id = int(callback_query.data.split('_')[1])
    # Получаем товар из базы данных
    usercart = cart[user_id]
    for item in usercart:
        if item_id == item[0]:
            usercart.remove(item)
            break
    await callback_query.answer("Товар успешно удален")

    new_markup = await kb.create_clear_item_buttons(cart[user_id])

    if callback_query.message.reply_markup != new_markup:
        if len(new_markup.inline_keyboard) > 1:
            print(len(new_markup.inline_keyboard))
            await callback_query.message.edit_text(f"Выберите товар для удаления", reply_markup=new_markup)
        else:
            await callback_query.message.edit_text(f"Выберите действие", reply_markup=kb.cart)
    else:
        await callback_query.answer("Сообщение не изменилось, товар уже удален.")

