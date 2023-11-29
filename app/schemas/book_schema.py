from typing import Optional
from pydantic import BaseModel


class BookSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    user_id: int

    class config:
        orm_mode = True






