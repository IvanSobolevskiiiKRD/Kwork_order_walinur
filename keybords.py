from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import database.requests as rq
import math


privacy_policy = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📝 Принять", callback_data="privacy_policy_True")],
    [InlineKeyboardButton(text="🔙 Отмена", callback_data="privacy_policy_False")]
])


start_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Инструкции"),
     KeyboardButton(text="Гарантия")],
    [KeyboardButton(text="Промокод"),
    KeyboardButton(text="Магазины")],
    [KeyboardButton(text="Cоцсети"),
    KeyboardButton(text="Задать вопрос")]
], resize_keyboard=True)


cansel_answer_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="⏮️ На главную ⏮️")]
], resize_keyboard=True)

async def answer_admin_button(id, text_answer):
    otvet = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Написать ответ", callback_data=f"otvet_{id}_{text_answer}")]
])
    return otvet


async def create_list_tovar_kb():
    tovars = await rq.get_data_tovar()
    key_board_tovar = ReplyKeyboardMarkup()

    for tovar in tovars:
        key_board_tovar.row(KeyboardButton(text=f"{tovar.name}", callback_data=f"tovar_{tovar.id}"))

    key_board_tovar.row(KeyboardButton(text="⏮️ На главную ⏮️", callback_data="back_kb"))
    return key_board_tovar.as_markup()

async def kreate_key_board(telegram_id):
    data_Tovars = await rq.get_data_tovar()
    user_data = await rq.get_user_data(telegram_id)
    user_data = user_data.__dict__
    data_Tovar = []
    for x in data_Tovars:
        if user_data["categor"] == x.categor:
            data_Tovar.append(x)
    page = int(user_data["page"]) - 1
    kol_tovar = len(data_Tovar)

    kol_tovarov = 5
    start_gen_kb = kol_tovarov * page
    end_gen_kb = start_gen_kb + kol_tovarov


    key_board_tovar = ReplyKeyboardBuilder()

    for tovar in data_Tovar[start_gen_kb:end_gen_kb]:
        key_board_tovar.row(KeyboardButton(text=f"{tovar.name}", callback_data=f"tovar_{tovar.id}"))
    
    
    stranic = math.ceil(kol_tovar/kol_tovarov)
    button_list = []
    button_list.append(KeyboardButton(text="⬅️ Назад"))
    #button_list.append(KeyboardButton(text=f"{page + 1} / {stranic}"))
    button_list.append(KeyboardButton(text="Вперед ➡️"))

    key_board_tovar.row(*button_list)

    key_board_tovar.row(KeyboardButton(text="⏮️ На главную ⏮️"))

    return key_board_tovar.as_markup(resize_keyboard=True)


async def tovar_kb(ozon,wb):

    tovar_kb = InlineKeyboardBuilder()
    if ozon != "Нет":
        tovar_kb.row(InlineKeyboardButton(text="Купить на Ozon", url=ozon))
    if wb != "Нет":
        tovar_kb.row(InlineKeyboardButton(text="Купить на WB", url=wb))
    return tovar_kb.as_markup()

skip_ozon_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Нет данного товара на Ozon",callback_data="skip_ozon")],
    [KeyboardButton(text="⬅️ В админку")]
], resize_keyboard=True)

skip_wb_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Нет данного товара на WB",callback_data="skip_wb")],
    [KeyboardButton(text="⬅️ В админку")]
], resize_keyboard=True)



admin_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🆕 Создание нового товара 🆕")],
    [KeyboardButton(text="🗑 Удалить товар 🗑")],
    [KeyboardButton(text="💬 Сделать рассылку 💬")],
    [KeyboardButton(text="🆕 Обновить промокод 🆕")],
    [KeyboardButton(text="🕐 Статистика за месяц 🕐")],
    [KeyboardButton(text="Выгрузить базу")]
], resize_keyboard=True)






rassilka = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Прикрепить фото", callback_data="prikrep_true_admin")],
    [KeyboardButton(text="Не прекриплять", callback_data="prikrep_false_admin")],
    [KeyboardButton(text="⬅️ В админку", callback_data="calnsel_admin")]
], resize_keyboard=True)

cancel_rassilka_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="⬅️ В админку")]
])

rassilka_batton = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Добавить кнопку")],
    [KeyboardButton(text="Не добавлять кнопку", callback_data="batton_false_admin")],
    [KeyboardButton(text="⬅️ В админку", callback_data="calnsel_admin")]
], resize_keyboard=True)

cancel_rassilka_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="⬅️ В админку")]
], resize_keyboard=True)

finish_rassilka_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Да начинаем рассылку", callback_data="ras_start")],
    [KeyboardButton(text="⬅️ В админку", callback_data="calnsel_admin")]
], resize_keyboard=True)

back_admin_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="В админку", callback_data="back_admin_menu")]
])

async def create_button(text,url):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{text}", url=f"{url}")]
    ])

magazin_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="WB WALINUR", url="https://www.wildberries.ru/seller/123026")],
    [InlineKeyboardButton(text="OZON WALINUR", url="https://ozon.ru/t/1WczDmd")],
    [InlineKeyboardButton(text="OZON CARDALE", url="https://ozon.ru/t/MukcsDn")],
    #[InlineKeyboardButton(text="OZON Erium", url="https://ozon.ru/t/gaz2fgV")]
])

socsites_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Дзен", url="https://dzen.ru/id/692dcd0283f974561dd48d25")],
    [InlineKeyboardButton(text="YouTube", url="https://youtube.com/@cardale-k4q?si=XE8ei_OVUt7ItYzC")],
    [InlineKeyboardButton(text="ВК", url="https://vk.com/cardale1")],
    [InlineKeyboardButton(text="Instagram", url="https://www.instagram.com/cardale.ru?igsh=aWVrMjlndGhvNHI4&utm_source=qr")],
    [InlineKeyboardButton(text="Telegram канал", url="https://t.me/cardale_akb")]
])

promo_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Ozon CARDALE", url="https://ozon.ru/t/MukcsDn")]
])

add_categor_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Категория: Зарядные устройства")],
    [KeyboardButton(text="Категория: Другое")],
    [KeyboardButton(text="⬅️ В админку")]
], resize_keyboard=True)

select_categor_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="ㅤㅤЗарядные устройстваㅤㅤ")],
    [KeyboardButton(text="ㅤㅤДругоеㅤㅤ")],
    [KeyboardButton(text="⏮️ На главную ⏮️")]
], resize_keyboard=True)

select_categor_delet_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Категория : Зарядные устройства")],
    [KeyboardButton(text="Категория : Другое")],
    [KeyboardButton(text="⬅️ В админку")]
], resize_keyboard=True)



async def kreate_key_board_for_del(telegram_id):
    data_Tovars = await rq.get_data_tovar()
    user_data = await rq.get_user_data(telegram_id)
    user_data = user_data.__dict__
    data_Tovar = []
    for x in data_Tovars:
        if user_data["categor"] == x.categor:
            data_Tovar.append(x)
    page = int(user_data["page"]) - 1
    kol_tovar = len(data_Tovar)

    kol_tovarov = 5
    start_gen_kb = kol_tovarov * page
    end_gen_kb = start_gen_kb + kol_tovarov


    key_board_tovar = ReplyKeyboardBuilder()

    for tovar in data_Tovar[start_gen_kb:end_gen_kb]:
        key_board_tovar.row(KeyboardButton(text=f"Удалить - {tovar.name}"))
    
    
    stranic = math.ceil(kol_tovar/kol_tovarov)
    button_list = []
    button_list.append(KeyboardButton(text="⬅️ Предыдущая страница ⬅️"))
    #button_list.append(KeyboardButton(text=f"{page + 1} / {stranic}"))
    button_list.append(KeyboardButton(text="➡️ Следущая страница ➡️"))

    key_board_tovar.row(*button_list)

    key_board_tovar.row(KeyboardButton(text="⬅️ В админку"))

    return key_board_tovar.as_markup(resize_keyboard=True)