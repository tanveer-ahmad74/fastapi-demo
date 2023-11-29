from fastapi import FastAPI
import model
from config import engine
from api.book import book_router
from api.user import user_router
model.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(book_router, prefix="/book", tags=["book"])
app.include_router(user_router, prefix="/user", tags=["user"])
