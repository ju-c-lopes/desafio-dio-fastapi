from databases.interfaces import Record
from fastapi import HTTPException, status
from pydantic import BaseModel

from src.database import database
from src.models.conta import contas
from src.schema.conta import Conta, ContaUpdateIn


class ContaService(BaseModel):
    async def create(self, conta: Conta):
        command = contas.insert().values(
            id=conta.id,
            saldo=conta.saldo,
            cliente=conta.cliente,
        )
        conta_id = await database.execute(command)

        query = contas.select().where(contas.c.id == conta_id)
        return await database.fetch_one(query)

    async def get_conta(self, id: int) -> Record:
        return await self.__get_by_id(id)

    async def update(self, id: int, conta: ContaUpdateIn) -> Record:
        total = await self.count(id)
        if not total:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conta não encontrada.",
            )

        data = conta.model_dump(exclude_unset=True)
        command = contas.update().where(contas.c.id == id).values(**data)
        await database.execute(command)

        return await self.__get_by_id(id)

    async def count(self, id: int) -> int:
        query = "select count(id) as total from contas where id = :id"
        result = await database.fetch_one(query, {"id": id})
        return result.total

    async def __get_by_id(self, id) -> Record:
        query = contas.select().where(contas.c.id == id)
        _conta = await database.fetch_one(query)
        if not _conta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada."
            )
        return _conta
