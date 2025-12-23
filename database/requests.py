from database.models import async_session
from database.models import User, Tovar, Promos
from sqlalchemy import select, update, delete
from datetime import datetime

async def user_exists(telegram_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == telegram_id))

        if not user:
            return False
        else:
            return True

async def set_user(telegram_id, username):
    async with async_session() as session:
        start_data = datetime.now()
        user = await session.scalar(select(User).where(User.tg_id == telegram_id))

        if not user:
            session.add(User(tg_id=telegram_id, admin=False, username=username, page=1, categor="Все", time_start=start_data, privacy_policy=False))

            await session.commit()

async def redact_data_user(tg_id, col, new_data):
    tg_id = int(tg_id)
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(**{col: new_data}))
        await session.commit()

async def get_user_data(telegram_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == telegram_id))

async def get_data_Users_all():
    async with async_session() as session:
        res =  await session.execute(select(User))
        return res.scalars().all()


async def admin_cheak(telegram_id):
    async with async_session() as session:
        return await session.scalar(select(User.admin).where(User.tg_id == telegram_id))
    
async def set_admin(telegram_id):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == telegram_id).values({"admin": True}))
        await session.commit()

async def set_page(telegram_id, page):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == telegram_id).values({"page": page}))
        await session.commit()
    
async def set_categor(telegram_id, categor):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == telegram_id).values({"categor": categor}))
        await session.commit()

async def create_tovar(categor, doc_id, name, descript, ozon, link_wb):
    async with async_session() as session:
        session.add(Tovar(categor=categor, doc_id=doc_id, name=name, descript=descript, link_ozon=ozon, link_wb=link_wb))
        await session.commit()

async def get_data_tovar():
    async with async_session() as session:
        res =  await session.execute(select(Tovar))
        return res.scalars().all()
    
async def get_data_one_Tovar(post_id):
    async with async_session() as session:
        return await session.scalar(select(Tovar).where(Tovar.id == post_id))
    
async def update_tovar(id,categor):
    async with async_session() as session:
        await session.execute(update(Tovar).where(Tovar.id == id).values({"categor": categor}))
        await session.commit()


async def update_promo(promocode,time_work_promo):
    async with async_session() as session:
        await session.execute(update(Promos).where(Promos.id == 1).values({"promocode": promocode, "time_work_promo": time_work_promo}))
        await session.commit()

async def get_promo():
    async with async_session() as session:
        return await session.scalar(select(Promos).where(Promos.id == 1))

