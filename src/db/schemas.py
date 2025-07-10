from pydantic import BaseModel


class BaseNote(BaseModel):
    name: str
    text: str
    user_id: int
