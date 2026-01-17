from pydantic import Field
from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel

from models.produto import ProdutoDto


class Transacao(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
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
