from fastapi import APIRouter
from sqlalchemy import select

from src.api.dependecies import SessionDep
from src.database import engine, Base
from src.schemas.books import BookSchema
from src.models.books import BookModel
from src.schemas.books import BookSchema, BookGetSchema

router = APIRouter()


@router.post("/setup")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@router.post("/books")
async def add_book(book: BookSchema, session: SessionDep) -> BookSchema:
    new_book = BookModel(**book.dict())
    session.add(new_book)
    await session.commit()
    return book


@router.get("/books")
async def get_books(session: SessionDep) -> list[BookGetSchema]:
    query = select(BookModel)
    result = await session.execute(query)
    books = result.scalars().all()
    print(f"{books=}")
    return books


@router.delete("/books/{id}")
async def delete_book(id: str, session: SessionDep):
    result = await session.execute(select(BookModel).where(BookModel.id == id))
    book = result.scalar_one_or_none()

    if book is None:
        return {"error": "Book not found"}

    await session.delete(book)
    await session.commit()

    return {"ok": True}
