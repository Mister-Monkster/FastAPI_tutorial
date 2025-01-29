from typing import Annotated

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from fastapi import FastAPI, Depends

app = FastAPI()

engine = create_async_engine('sqlite+aiosqlite:///books.db')

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


class BooksModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]


@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        return {"ok": True}


class BookAddSchema(BaseModel):
    title: str
    author: str


class BookGetSchema(BookAddSchema):
    id: int


@app.post('/books')
async def add_book(data: BookAddSchema, session: SessionDep):
    new_book = BooksModel(
        title=data.title,
        author=data.author
    )
    session.add(new_book)
    await session.commit()
    return {"ok": True}


@app.get('/books')
async def get_books(session: SessionDep):
    query = select(BooksModel)
    result = await session.execute(query)
    return result.scalars().all()


