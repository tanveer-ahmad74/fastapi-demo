from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import create, get, update, remove
from app.schemas.users_schema import UserSchema, GetUserSchema, UpdateUserSchema
from app.model import User
from app.global_response import create_response, list_response, update_response, delete_response, email_response
from app.router import get_db
from fastapi import APIRouter
from utils.password_hasher import Hasher
from utils.reusable import check_email_exist
user_router = APIRouter()

@user_router.post("/create", status_code=201)
async def create_user(request: UserSchema, db: Session = Depends(get_db)):
    user_data = request.dict()
    email = check_email_exist(db, user_data['email'])
    if email:
        hash_pass = Hasher.get_password_hash(user_data['password'])
        _user = User(username=user_data['username'], email=user_data['email'], password=hash_pass)
        create(db,  _user)
        return create_response
    else:
        return email_response


@user_router.get("/get", status_code=200)
async def get_all(db: Session = Depends(get_db)):
    users = get(db, User)
    books_dict_list = [book.__dict__ for book in users]
    get_users = [GetUserSchema(**book) for book in books_dict_list]
    list_response['result'] = get_users
    return list_response


@user_router.put("/update/{user_id}", status_code=200)
async def update_user(user_id: int, request: UpdateUserSchema, db: Session = Depends(get_db)):
    updated_data = request.dict()
    email = check_email_exist(db, updated_data['email'])
    if email:
        updated_book = update(db, User, user_id, updated_data)

        if updated_book:
            return update_response
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    else:
        return email_response


@user_router.delete("/delete/{user_id}", status_code=200)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted_book = remove(db, User, user_id)
    if deleted_book:
        return delete_response
    else:
        raise HTTPException(status_code=404, detail="Book not found")


