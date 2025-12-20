from aiogram import F, Router, types, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime
import math


import keybords as kb
import Text
import database.requests as rq
from main import bot

router = Router()

class Answer(StatesGroup):
    answer = State()

# СТАРТ
@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()
    await rq.set_user(message.from_user.id, message.from_user.username)
    await message.answer(Text.start_text, reply_markup=kb.start_kb)


@router.message(F.text.contains("⏮️ На главную ⏮️"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await rq.set_user(message.from_user.id, message.from_user.username)
    await message.answer(Text.start_text, reply_markup=kb.start_kb)

@router.message(F.text.contains("Инструкции"))
async def instachion(message: Message):
    await rq.set_page(message.from_user.id, 1)
    await message.answer(Text.select_categor, reply_markup=kb.select_categor_kb)

@router.message(F.text.contains("ㅤㅤЗарядные устройстваㅤㅤ"))
@router.message(F.text.contains("ㅤㅤДругоеㅤㅤ"))
async def instachion(message: Message):
    if message.text == "ㅤㅤЗарядные устройстваㅤㅤ":
        await rq.set_categor(message.from_user.id, "Зарядные устройства")
    if message.text == "ㅤㅤДругоеㅤㅤ":
        await rq.set_categor(message.from_user.id, "Другое")
    await message.answer(Text.instrachion, reply_markup=await kb.kreate_key_board(message.from_user.id))

@router.message(F.text.contains("Вперед ➡️"))
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

    if page == stranic:
        await rq.set_page(message.from_user.id, 1)
    else:
        await rq.set_page(message.from_user.id, page + 1)

    await message.answer(Text.instrachion, reply_markup=await kb.kreate_key_board(message.from_user.id))

@router.message(F.text.contains("⬅️ Назад"))
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

    await message.answer(Text.instrachion, reply_markup=await kb.kreate_key_board(message.from_user.id))

@router.message(F.text.contains("Магазины"))
async def dack_menu(message: Message):
    await message.answer(Text.magazin_text, reply_markup=kb.magazin_kb)

@router.message(F.text.contains("Гарантия"))
async def garant(message: Message):
    await message.answer(Text.garant)

@router.message(F.text.contains("Промокод"))
async def dack_menu(message: Message):
    data = await rq.get_promo()
    time_now = int(datetime.now().timestamp())
    print(f"Время в сек сейчас: {time_now}")
    if data.time_work_promo > time_now:
        await message.answer(Text.promo_code_text.format(data.promocode), reply_markup=kb.promo_kb)
    else:
        await message.answer(Text.promo_not_text, reply_markup=kb.promo_kb)

@router.message(F.text.contains("Задать вопрос"))
async def dack_menu(message: Message, state: FSMContext):
    await state.set_state(Answer.answer)
    await message.answer(Text.answer_text, reply_markup=kb.cansel_answer_kb)

@router.message(Answer.answer)
async def create_new_tovar_set_name(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Ваш вопрос отправлен 👌")
    await bot.send_message(1667550116, Text.answer_to_admin.format(message.from_user.id, message.from_user.username, message.html_text),
                           reply_markup=await kb.answer_admin_button(message.from_user.id, message.html_text))
    await message.answer(Text.start_text, reply_markup=kb.start_kb)

@router.message(F.text)
async def tovar(message: Message):
    tovars = await rq.get_data_tovar()
    for tovar in tovars:
        if tovar.name.lower() == message.text.lower():
            await message.answer_document(tovar.doc_id)
            await message.answer(Text.tovar_text.format(tovar.name, tovar.descript), show_alert=False, reply_markup=await kb.tovar_kb(tovar.link_ozon, tovar.link_wb))

@router.message(F.document)
async def tovar(message: Message):
    print(message.document.file_id)

