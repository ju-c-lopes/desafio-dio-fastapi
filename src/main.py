from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.controllers import cliente, conta
from src.database import database, engine, metadata

metatags = [
    {
        "name": "clientes",
        "description": "Operações de authenticação para realizar operações bancárias"
    },
    {
        "name": "contas",
        "description": "Endpoints para realização das operações bancárias"
    }
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    from .models.cliente import clientes  # noqa
    from .models.conta import contas  # noqa

    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()


app = FastAPI(
    lifespan=lifespan,
    title="DIO-Bank",
    summary="Uma API de transações bancárias.",
    description="""
Operações disponíveis:

## Depósito:

* Valores maiores que zero, lança **Invalid Exception** se for menor que zero.

## Saque:

* Valores maiores que zero, lança **Invalid Exception** se for menor que zero.
* Valores iguais ou menores que o saldo disponível na conta, lança **Unauthorizated Exception** do contrário.

## Extrato:

* Exibe as transações realizadas em determinada conta. Há a possibilidade de usar **"query parameter"** para especificar limite.

Cada transação realizada pertence a uma conta específica.
""",
    openapi_tags=metatags
)

app.include_router(cliente.router)
app.include_router(conta.router)
