import sqlalchemy as sa

from src.database import metadata
from .cliente import clientes  # noqa

contas = sa.Table(
    "contas",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("saldo", sa.Float(precision=2), nullable=False, default=0),
    sa.Column("cliente", sa.ForeignKey("clientes.id"), nullable=False),
)

transacoes = sa.Table(
    "transacoes",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("tipo", sa.String(20), nullable=False),
    sa.Column("valor", sa.Float(precision=2), nullable=False),
    sa.Column("conta", sa.ForeignKey("contas.id"), nullable=False),
    sa.Column("data", sa.TIMESTAMP(timezone=True), nullable=True, server_default=sa.func.now())
)
