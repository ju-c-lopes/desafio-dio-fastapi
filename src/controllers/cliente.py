from datetime import UTC, datetime
from fastapi import APIRouter, HTTPException, status

from src.security import sign_jwt
from src.schema.cliente import Cliente
from src.services.cliente import ClienteService
from src.views.cliente import ClienteOut

router = APIRouter(prefix="/cliente", tags=["clientes"])

service = ClienteService()


@router.post("/login",  response_model=ClienteOut)
async def login(acesso: Cliente):
    return sign_jwt(cliente_id=acesso.id)


@router.post("/cadastrar-cliente", response_model=Cliente, status_code=status.HTTP_201_CREATED)
async def cadastrar_cliente(cliente: Cliente):
    hoje = datetime.now(UTC)
    if ((hoje.date() - cliente.data_nasc).days // 365) < 18:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="É necessário ter mais de 18 anos para abrir uma conta.")
    return {**cliente.model_dump(), "id": await service.create(cliente)}
