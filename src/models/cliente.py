import sqlalchemy as sa

from src.database import metadata

clientes = sa.Table(
    "clientes",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("nome", sa.String(80), nullable=False),
    sa.Column("data_nasc", sa.Date, nullable=False),
)
