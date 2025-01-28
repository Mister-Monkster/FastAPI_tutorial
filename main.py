from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel

app = FastAPI()

books = [
    {"id": 1,
     "title": "Асинхронность в Python",
     "Author": "Мэттью"},
    {"id": 2,
     "title": "Backend разработка в Python",
     "Author": "Артём"},
]


@app.get(
    "/books",
    tags=['Книги 📚'],
    summary='Получить все книги 📚',
)
def read_books():
    return books


@app.get(
    '/books/{id}',
    tags=['Книги 📚'],
    summary='Получить книгу по id 🆔',
)
def get_book(id: int):
    for book in books:
        if book["id"] == id:
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")

class New_book(BaseModel):
    title: str
    author: str


@app.post('/books',
          tags=['Книги 📚'],
          summary='Добавить новую книгу🆕')
def add_books(book: New_book):
    books.append({
        'id': len(books) + 1,
        'title': book.title,
        'author': book.author,
    })
    return {"success": True, "message": "Книга успешно добавлена."}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
