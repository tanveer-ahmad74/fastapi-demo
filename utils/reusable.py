from app.model import User
from sqlalchemy.orm import Session

from utils.password_hasher import Hasher


def check_email_exist(db: Session, email):
    query = db.query(User).filter(User.email == email).first()
    if query:
        return False
    return True

def check_user(db: Session, email, password):
    user = db.query(User).filter(User.email == email).first()
    check_pass = Hasher.verify_password(password, user.password)
    if check_pass:
        return True
    return False
