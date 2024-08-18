from datetime import date

from pydantic import BaseModel


class Cliente(BaseModel):
    id: int
    nome: str
    data_nasc: date
