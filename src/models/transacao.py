import uuid
from uuid import UUID

from pydantic import Field, ConfigDict
from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel

from models.produto import ProdutoDto


class Transacao(BaseModel):
    id: str = Field(default=str(uuid.uuid4()))
    quantidade: int
    data_transacao: datetime | None
    listaDosProdutos: list[ProdutoDto]


class CreateTransacao(BaseModel):
    quantidade: int
    produtos: list[ProdutoDto]


class UpdateTransacao(BaseModel):
    quantidade: int | None
    data_transacao: datetime | None
    produtos: list[ProdutoDto] | None
