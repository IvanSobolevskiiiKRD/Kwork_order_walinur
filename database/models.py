from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column()
    admin: Mapped[bool] = mapped_column()
    page: Mapped[int] = mapped_column()
    categor: Mapped[str] = mapped_column()
    time_start: Mapped[DateTime] = mapped_column(DateTime)
    privacy_policy: Mapped[bool] = mapped_column()

class Tovar(Base):
    __tablename__ = "tovars"

    id: Mapped[int] = mapped_column(primary_key=True)
    categor: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    descript: Mapped[str] = mapped_column()
    doc_id: Mapped[str] = mapped_column()
    link_ozon: Mapped[str] = mapped_column()
    link_wb: Mapped[str] = mapped_column()

class Promos(Base):
    __tablename__ = "promocode"

    id: Mapped[int] = mapped_column(primary_key=True)
    promocode: Mapped[str] = mapped_column()
    time_work_promo: Mapped[int] = mapped_column()


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)