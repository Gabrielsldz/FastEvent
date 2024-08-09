from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int
    password: str
    email: str
