from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True, nullable=True)
    is_active = Column(Boolean, default=True)

    # Define a relationship with Book model
    books = relationship('Book', back_populates='user')

class Book(Base):
    __tablename__ = 'Book'

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

    # Define a foreign key relationship with the User model
    user_id = Column(Integer, ForeignKey('User.id'))

    # Establish a bidirectional relationship
    user = relationship('User', back_populates='books')
