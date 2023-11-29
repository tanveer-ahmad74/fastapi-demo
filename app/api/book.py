from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.authentication.auth import JWTBearer
from app.crud import get, create, remove, update
from app.schemas.book_schema import BookSchema
from app.model import Book
from app.global_response import create_response, list_response, update_response, delete_response
from app.router import get_db
from fastapi import APIRouter

book_router = APIRouter()

@book_router.post("/create", status_code=201, dependencies=[Depends(JWTBearer())])
async def create_book(request: BookSchema, db: Session = Depends(get_db)):
    book_data = request.dict()
    _book = Book(title=book_data['title'], description=book_data['description'], user_id=book_data['user_id'])
    create(db, _book)
    return create_response


@book_router.get("/get", status_code=200, dependencies=[Depends(JWTBearer())])
async def get_all(db: Session = Depends(get_db)):
    books = get(db, Book)
    response = [
        {
            "id": book.id,
            "title": book.title,
            "description": book.description,
            "user":
                {
                    "username": book.user.username,
                    "email": book.user.email,
                    "password": book.user.password,
                    "is_active": book.user.is_active,
                    "id": book.user.id
                }
        }
        for book in books]
    list_response['result'] = response
    return list_response


@book_router.put("/update/{book_id}", status_code=200, dependencies=[Depends(JWTBearer())])
async def update_book(book_id: int, request: BookSchema, db: Session = Depends(get_db)):
    updated_data = request.dict()
    updated_book = update(db, Book, book_id, updated_data)

    if updated_book:
        return update_response
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@book_router.delete("/delete/{book_id}", status_code=200, dependencies=[Depends(JWTBearer())])
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted_book = remove(db, Book, book_id)
    if deleted_book:
        return delete_response
    else:
        raise HTTPException(status_code=404, detail="Book not found")
