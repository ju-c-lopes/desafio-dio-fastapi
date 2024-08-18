from pydantic import BaseModel

from src.database import database
from src.models.cliente import clientes
from src.schema.cliente import Cliente


class ClienteService(BaseModel):
    async def create(self, cliente: Cliente):
        command = clientes.insert().values(
            id=cliente.id,
            nome=cliente.nome,
            data_nasc=cliente.data_nasc
        )
        return await database.execute(command)

    async def count(self, id: int) -> int:
        query = "select count(id) as total from clientes where id = :id"
        result = await database.fetch_one(query, {"id": id})
        return result.total
