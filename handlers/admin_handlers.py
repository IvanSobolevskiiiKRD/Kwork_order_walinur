from aiogram import F, Router, types, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime
import asyncio
import pandas as pd
from aiogram.types.input_file import FSInputFile
import math


import keybords as kb
import Text
import database.requests as rq
from main import bot

router = Router()

class Admin_states(StatesGroup):
    text = State()
    photo = State()
    batton_text = State()
    batton_url = State()

class New_Tovar(StatesGroup):
    categor = State()
    name = State()
    discript = State()
    file_id = State()
    ozon_url = State()
    wb_url = State()

class Otvet(StatesGroup):
    id_client = State()
    vopros = State()
    otvet = State()

class Promo(StatesGroup):
    new_Promo = State()
    time_work_promo = State()


@router.message(Command("admin"))
async def admin_panel(message: Message):
    admin_status = await rq.admin_cheak(message.from_user.id)
    print(admin_status)
    if admin_status:
        await message.answer(f"Привет, это админка", reply_markup= kb.admin_kb)

@router.message(F.text.contains("⬅️ В админку"))
async def admin_panel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Привет, это админка", reply_markup= kb.admin_kb)

@router.message(F.text == "GYBINfwewef:92648461")
async def set_admin_panel(message: Message):
    await rq.set_admin(message.from_user.id)
    await message.answer(f"Привет, это админка", reply_markup= kb.admin_kb)

# Выдача прав админа
@router.message(F.text == "GYBINfwewef:92648461")
async def set_admin_panel(message: Message):
    await rq.set_admin(message.from_user.id)
    await message.answer(f"Привет, это админка", reply_markup= kb.admin_kb)

#Работа с вопросами клиентов
@router.callback_query(F.data.contains("otvet_"))
async def write_otvet(callback: CallbackQuery, state: FSMContext):
    temp, id_client, vopros = callback.data.split("_")

    await state.set_state(Otvet.id_client)
    await state.update_data(id_client=id_client)
    await state.set_state(Otvet.vopros)
    await state.update_data(vopros=vopros)
    await state.set_state(Otvet.otvet)
    await callback.message.answer("Пожалуйста Введите ваш ответ", reply_markup=kb.cancel_rassilka_kb, show_alert=False)


@router.message(Otvet.otvet)
async def create_new_tovar_set_name(message: Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(data["id_client"], Text.otvet.format(data["vopros"], message.html_text))
    await state.clear()
    await message.answer("Ответ отправлен")



#Создание нового товара
@router.message(F.text.contains("🆕 Создание нового товара 🆕"))
async def create_new_tovar(message: Message, state: FSMContext):
    await state.set_state(New_Tovar.categor)
    await message.answer("Пожалуйста выберите категорию товара", reply_markup=kb.add_categor_kb)

@router.message(F.text.contains("Категория: Зарядные устройства"))
@router.message(F.text.contains("Категория: Другое"))
async def create_new_tovar(message: Message, state: FSMContext):
    if message.text == "Категория: Зарядные устройства":
        await state.update_data(categor = "Зарядные устройства")
    if message.text == "Категория: Другое":
        await state.update_data(categor = "Другое")
    await state.set_state(New_Tovar.name)
    await message.answer("Пожалуйста название товара", reply_markup=kb.cancel_rassilka_kb)

@router.message(New_Tovar.name)
async def create_new_tovar_set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(New_Tovar.discript)
    await message.answer("Отправьте описание товара", reply_markup=kb.cancel_rassilka_kb)


@router.message(New_Tovar.discript)
async def create_new_tovar_set_disc(message: Message, state: FSMContext):
    await state.update_data(discript=message.html_text)
    await state.set_state(New_Tovar.file_id)
    await message.answer("Отправьте файл для загрузки", reply_markup=kb.cancel_rassilka_kb)

@router.message(New_Tovar.file_id)
async def create_new_tovar_set_file_id(message: Message, state: FSMContext):
    await state.update_data(file_id=message.document.file_id)
    await state.set_state(New_Tovar.ozon_url)
    await message.answer("Отправьте ссылку на Озон", reply_markup=kb.skip_ozon_kb)


@router.message(F.text.contains("Нет данного товара на Ozon"))
async def skip_ozon(message: Message, state: FSMContext):
    await state.update_data(ozon_url="Нет")
    await state.set_state(New_Tovar.wb_url)
    await message.answer("Отправьте ссылку на WB", reply_markup=kb.skip_wb_kb)

@router.message(New_Tovar.ozon_url)
async def create_new_tovar_set_ozon_url(message: Message, state: FSMContext):
    await state.update_data(ozon_url=message.text)
    await state.set_state(New_Tovar.wb_url)
    await message.answer("Отправьте ссылку на WB", reply_markup=kb.cancel_rassilka_kb)

@router.message(F.text.contains("Нет данного товара на WB"))
async def skip_ozon(message: Message, state: FSMContext):
    await state.update_data(wb_url="Нет")
    data = await state.get_data()
    await rq.create_tovar(data["categor"], data["file_id"], data["name"], data["discript"], data["ozon_url"], data["wb_url"])
    await state.clear()
    await message.answer("Товар добавлен 🤗")
    #await message.answer(Text.instrachion, reply_markup=await kb.create_list_tovar_kb())
    await message.answer(f"Привет, это админка", reply_markup= kb.admin_kb)

@router.message(New_Tovar.wb_url)
async def create_new_tovar_set_ozon_url(message: Message, state: FSMContext):
    await state.update_data(wb_url=message.text)
    data = await state.get_data()
    await rq.create_tovar(data["categor"], data["file_id"], data["name"], data["discript"], data["ozon_url"], data["wb_url"])
    await state.clear()
    await message.answer("Товар добавлен 🤗")
    #await message.answer(Text.instrachion, reply_markup=await kb.create_list_tovar_kb())
    await message.answer(f"Привет, это админка", reply_markup= kb.admin_kb)



#Рассылка
@router.message(F.text.contains("💬 Сделать рассылку 💬"))
async def rassilka_1(message: Message, state: FSMContext):
    await state.set_state(Admin_states.text)
    await message.answer("Пожалуйста напишите текст", reply_markup=kb.cancel_rassilka_kb)

@router.message(F.text.contains("Прикрепить фото"))
async def rassilka_1(message: CallbackQuery, state: FSMContext):
    await state.set_state(Admin_states.photo)
    await bot.send_message(message.from_user.id, "Отправьте фото", reply_markup=kb.cancel_rassilka_kb)

@router.message(F.text.contains("Не прекриплять"))
async def rassilka_1(message: CallbackQuery):
    await bot.send_message(message.from_user.id, "Прикрепляем кнопку с ссылкой?", reply_markup= kb.rassilka_batton)

@router.message(F.text.contains("Добавить кнопку"))
async def rassilka_1(message: Message, state: FSMContext):
    await state.set_state(Admin_states.batton_text)
    await message.answer("Напишите текст для кнопки", reply_markup=kb.cancel_rassilka_kb)

@router.message(F.text.contains("Не добавлять кнопку"))
async def rassilka_1(message: Message, state: FSMContext):
    data = await state.get_data()

    try:
        await bot.send_photo(message.from_user.id, data["photo"], caption= data["text"])
    except:
        await bot.send_message(message.from_user.id, data["text"])

    await bot.send_message(message.from_user.id,"Вы уверенны в рассылке?", reply_markup=kb.finish_rassilka_kb)


@router.message(F.text.contains("Да начинаем рассылку"))
async def rassilka_1(message: Message, state: FSMContext):
    data = await state.get_data()
    user_list = await rq.get_data_Users_all()
    kol_rassilka = 0
    for user in user_list:
        await asyncio.sleep(1)
        try:
            await bot.send_photo(user.tg_id, data["photo"], caption= data["text"], reply_markup= await kb.create_button(data["batton_text"], data["batton_url"]))
            kol_rassilka += 1
        except:
            try:
                await bot.send_photo(user.tg_id, data["photo"], caption= data["text"])
                kol_rassilka += 1
            except:
                try:
                    await bot.send_message(user.tg_id, data["text"], reply_markup= await kb.create_button(data["batton_text"], data["batton_url"]))
                    kol_rassilka += 1
                except:
                    try:
                        await bot.send_message(user.tg_id, data["text"])
                        kol_rassilka += 1
                    except:
                        pass
    await state.clear()                
    await message.answer(f"Рассылка завершена, отправил данные {kol_rassilka} пользователям")
    await message.answer(f"Привет, это админка", reply_markup= kb.admin_kb)



@router.message(Admin_states.batton_text)
async def rassilka_2(message: Message, state: FSMContext):
    await state.update_data(batton_text=message.text)
    await state.set_state(Admin_states.batton_url)
    await bot.send_message(message.from_user.id,"Отправьте ссылку для кнопки", reply_markup=kb.cancel_rassilka_kb)

@router.message(Admin_states.batton_url)
async def rassilka_2(message: Message, state: FSMContext):
    await state.update_data(batton_url=message.text)
    data = await state.get_data()

    try:
        await bot.send_photo(message.from_user.id, data["photo"], caption= data["text"], reply_markup= await kb.create_button(data["batton_text"], data["batton_url"]))
    except:
        await bot.send_message(message.from_user.id, data["text"], reply_markup= await kb.create_button(data["batton_text"], data["batton_url"]))

    await message.answer("Вы уверенны в рассылке?", reply_markup=kb.finish_rassilka_kb)

@router.message(Admin_states.text)
async def rassilka_2(message: Message, state: FSMContext):
    await state.update_data(text=message.html_text)
    await message.answer("Прикрепляем фото к сообщению?", reply_markup= kb.rassilka)

@router.message(Admin_states.photo)
async def rassilka_2(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await message.answer("Прикрепляем кнопку с ссылкой?", reply_markup= kb.rassilka_batton)


@router.message(F.text.contains("🆕 Обновить промокод 🆕"))
async def rassilka_1(message: Message, state: FSMContext):
    await state.set_state(Promo.new_Promo)
    data = await rq.get_promo()
    await bot.send_message(message.from_user.id, Text.promo_admin_text.format(data.promocode), reply_markup=kb.cancel_rassilka_kb)

@router.message(Promo.new_Promo)
async def rassilka_2(message: Message, state: FSMContext):
    await state.update_data(new_Promo=message.text)
    await state.set_state(Promo.time_work_promo)
    await message.answer(Text.time_work_promo_admin_text, reply_markup= kb.cancel_rassilka_kb)

@router.message(Promo.time_work_promo)
async def rassilka_2(message: Message, state: FSMContext):
    await state.update_data(time_work_promo=message.text)
    try:
        date_object = datetime.strptime(message.text, "%Y-%m-%d")
        seconds = int(date_object.timestamp())
        data = await state.get_data()
        await rq.update_promo(data["new_Promo"], seconds)
        await message.answer("Новый промокод установлен")
        await state.clear()
        await bot.send_message(message.from_user.id, "Привет, это админка", reply_markup= kb.admin_kb)
    except:
        await message.answer("Данные даты были введены не верно, повторите попытку")
        await bot.send_message(message.from_user.id, "Привет, это админка", reply_markup= kb.admin_kb)

# Статистика активности пользователей

@router.message(F.text.contains("🕐 Статистика за месяц 🕐"))
async def statistika(message: Message):
    user_list = await rq.get_data_Users_all()
    all_users = len(user_list)
    new_user = 0
    month_now = datetime.now()
    month_now = month_now.month
    
    for user in user_list:
        time_reg_user = user.time_start
        time_reg_user = time_reg_user.month
        if time_reg_user == month_now:
            new_user = new_user + 1

    await message.answer(Text.statistika_text.format(new_user, all_users), reply_markup=kb.cancel_rassilka_kb)

@router.message(F.text.contains("Выгрузить базу"))
async def export_db(message: Message):
    data = await rq.get_data_Users_all()
    data_end = []
    for t in data:
        info = {'ID': t.id, 'TG_ID': t.tg_id, 'Username': t.username, 'Admin': t.admin, 'Reg_data': t.time_start}
        data_end.append(info)
    df = pd.DataFrame(data_end)
    df.to_excel("db_exel.xlsx", index=False)
    document = FSInputFile('db_exel.xlsx')
    await bot.send_document(message.from_user.id, document=document)
    await bot.send_message(message.from_user.id, "Привет, это админка", reply_markup= kb.admin_kb)

#Создание нового товара
@router.message(F.text.contains("🗑 Удалить товар 🗑"))
async def create_new_tovar(message: Message, state: FSMContext):
    await rq.set_page(message.from_user.id, 1)
    await message.answer(Text.select_categor, reply_markup=kb.select_categor_delet_kb)

@router.message(F.text.contains("Категория : Зарядные устройства"))
@router.message(F.text.contains("Категория : Другое"))
async def instachion(message: Message):
    if message.text == "Категория : Зарядные устройства":
        await rq.set_categor(message.from_user.id, "Зарядные устройства")
    if message.text == "Категория : Другое":
        await rq.set_categor(message.from_user.id, "Другое")
    await message.answer(Text.instrachion, reply_markup=await kb.kreate_key_board_for_del(message.from_user.id))

@router.message(F.text.contains("Удалить - "))
async def tovar(message: Message):
    _, name_tovar = message.text.split("далить - ")
    tovars = await rq.get_data_tovar()
    for tovar in tovars:
        if tovar.name.lower() == name_tovar.lower():
            await rq.update_tovar(tovar.id, "Удалён")
            await message.answer("Товар Удалён")
            await message.answer(f"Привет, это админка", reply_markup= kb.admin_kb)


@router.message(F.text.contains("➡️ Следущая страница ➡️"))
async def instachion(message: Message):
    user_data = await rq.get_user_data(message.from_user.id)
    user_data = user_data.__dict__
    data_Tovars = await rq.get_data_tovar()
    data_Tovar = []
    for x in data_Tovars:
        if user_data["categor"] == x.categor:
            data_Tovar.append(x)

    page = int(user_data["page"])
    kol_tovar = len(data_Tovar)
    kol_tovarov = 5
    stranic = math.ceil(kol_tovar/kol_tovarov)

    if page == stranic:
        await rq.set_page(message.from_user.id, 1)
    else:
        await rq.set_page(message.from_user.id, page + 1)

    await message.answer(Text.instrachion, reply_markup=await kb.kreate_key_board_for_del(message.from_user.id))

@router.message(F.text.contains("⬅️ Предыдущая страница ⬅️"))
async def instachion(message: Message):
    user_data = await rq.get_user_data(message.from_user.id)
    user_data = user_data.__dict__
    page = int(user_data["page"])
    data_Tovars = await rq.get_data_tovar()
    data_Tovar = []
    for x in data_Tovars:
        if user_data["categor"] == x.categor:
            data_Tovar.append(x)
            
    kol_tovar = len(data_Tovar)
    kol_tovarov = 5
    stranic = math.ceil(kol_tovar/kol_tovarov)

    if page == 1:
        await rq.set_page(message.from_user.id, stranic)
    else:
        await rq.set_page(message.from_user.id, stranic - 1)

    await message.answer(Text.instrachion, reply_markup=await kb.kreate_key_board_for_del(message.from_user.id))