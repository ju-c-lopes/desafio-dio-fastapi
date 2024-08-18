from fastapi import APIRouter, Depends, HTTPException, status

from src.controllers.cliente import service as serv_cliente
from src.database import database
from src.models.conta import transacoes
from src.schema.conta import Conta, ContaUpdateIn
from src.security import login_required
from src.services.conta import ContaService
from src.views.conta import ContaOut

router = APIRouter(prefix="/contas", tags=["contas"], dependencies=[Depends(login_required)])

service = ContaService()


@router.get("/{id}", response_model=ContaOut)
async def ver_conta(id: int):
    return await service.get_conta(id=id)


@router.post(
    "/criar-conta/{id_cliente}",
    response_model=ContaOut,
    status_code=status.HTTP_201_CREATED,
)
async def criar_conta(conta: Conta, id_cliente: int):
    if conta.saldo < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O saldo não pode ser um valor negativo.",
        )
    cliente = await serv_cliente.count(id_cliente)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado."
        )
    return await service.create(conta)


@router.patch("/{id}/saque/{valor}", response_model=ContaOut)
async def saque(id: int, valor: float):
    _conta = await service.get_conta(id=id)
    if valor > _conta.saldo:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Saldo insuficiente.")
    elif valor <= 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Requisição inválida.")
    conta = ContaUpdateIn(
        id=_conta.id,
        saldo=_conta.saldo,
    )
    conta.saldo -= valor
    command = transacoes.insert().values(tipo="Saque", valor=valor, conta=_conta.id)
    await database.execute(command)
    return await service.update(id=id, conta=conta)


@router.patch("/{id}/deposito/{valor}", response_model=ContaOut)
async def deposito(id: int, valor: float):
    _conta = await service.get_conta(id=id)
    conta = ContaUpdateIn(
        id=_conta.id,
        saldo=_conta.saldo,
    )
    if valor <= 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Requisição inválida.")
    conta.saldo += valor
    command = transacoes.insert().values(tipo="Deposito", valor=valor, conta=_conta.id)
    await database.execute(command)
    return await service.update(id=id, conta=conta)


@router.get("/{id}/extrato")
async def extrato(id: int, limit: int = 10):
    command = transacoes.select().where(transacoes.c.conta == id).limit(limit)
    transac = await database.fetch_all(command)
    return [
        {
            "Data": f"{transacao.data}",
            "transacao": f"{transacao.tipo} R$ {transacao.valor:.2f}",
        }
        for transacao in transac
    ]
