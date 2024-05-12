from pydantic import BaseModel


class Subscription(BaseModel):
    id: str
    name: str
    data: str
