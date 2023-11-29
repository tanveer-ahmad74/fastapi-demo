from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Request
from app.authentication.auth import JWTBearer
from app.authentication.auth_handler import signJWT, decodeJWT
from app.crud import create, get, update, remove
from app.schemas.users_schema import UserSchema, GetUserSchema, UpdateUserSchema, UserLoginSchema
from app.model import User
from app.global_response import create_response, list_response, update_response, delete_response, email_response
from app.router import get_db
from fastapi import APIRouter
from utils.password_hasher import Hasher
from utils.reusable import check_email_exist, check_user

user_router = APIRouter()

@user_router.post("/create", status_code=201)
async def create_user(request: Request, schema: UserSchema, db: Session = Depends(get_db)):
    user_data = schema.dict()
    email = check_email_exist(db, user_data['email'])
    if email:
        hash_pass = Hasher.get_password_hash(user_data['password'])
        _user = User(username=user_data['username'], email=user_data['email'], password=hash_pass)
        create(db,  _user)
        data = signJWT(str(_user.email))
        create_response['token'] = data['access_token']
        return create_response
    else:
        return email_response


@user_router.get("/get", status_code=200, dependencies=[Depends(JWTBearer())])
async def get_all(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get('authorization')[7:]
    user = decodeJWT(token=token)
    users = get(db, User)
    books_dict_list = [book.__dict__ for book in users]
    get_users = [GetUserSchema(**book) for book in books_dict_list]
    list_response['result'] = get_users
    return list_response


@user_router.put("/update/{user_id}", status_code=200, dependencies=[Depends(JWTBearer())])
async def update_user(request: Request, user_id: int, schema: UpdateUserSchema, db: Session = Depends(get_db)):
    updated_data = schema.dict()
    email = check_email_exist(db, updated_data['email'])
    if email:
        updated_book = update(db, User, user_id, updated_data)

        if updated_book:
            return update_response
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    else:
        return email_response


@user_router.delete("/delete/{user_id}", status_code=200, dependencies=[Depends(JWTBearer())])
async def delete_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    deleted_book = remove(db, User, user_id)
    if deleted_book:
        return delete_response
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@user_router.post("/login")
async def user_login(schema: UserLoginSchema, db: Session = Depends(get_db)):
    status = check_user(db, schema.email, schema.password)
    if status:
        token = signJWT(schema.email)
        return token
    return {
        "error": "Wrong login details!"
    }
