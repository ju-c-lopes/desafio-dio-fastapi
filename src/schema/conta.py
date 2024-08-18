from pydantic import BaseModel


class Conta(BaseModel):
    id: int
    saldo: float
    cliente: int


class Transacao(BaseModel):
    id: int
    tipo: str | None
    valor: float | None
    conta: Conta


class ContaUpdateIn(BaseModel):
    id: int | None = None
    saldo: float | None = None
    cliente: None = None
