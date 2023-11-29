from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta

def get(db: Session, model: DeclarativeMeta):
    return db.query(model).all()


def get_by_id(db: Session, model: DeclarativeMeta, book_id: int):
    return db.query(model).filter(model.id == book_id).first()


def create(db: Session, book):
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def remove(db: Session, model: DeclarativeMeta, book_id: int):
    _book = get_by_id(db=db, model=model, book_id=book_id)

    if _book:
        db.delete(_book)
        db.commit()
        return _book
    else:
        return None


def update(db: Session, model: DeclarativeMeta, book_id: int, new_data: dict):
    book = db.query(model).filter(model.id == book_id).first()
    if book:
        for key, value in new_data.items():
            setattr(book, key, value)
        db.commit()
        db.refresh(book)
        return book
    return None
