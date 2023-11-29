from app.model import User
from sqlalchemy.orm import Session


def check_email_exist(db: Session, email):
    query = db.query(User).filter(User.email == email).first()
    if query:
        return False
    return True
