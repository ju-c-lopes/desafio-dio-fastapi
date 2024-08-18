from pydantic import BaseModel


class ClienteOut(BaseModel):
    access_token: str
