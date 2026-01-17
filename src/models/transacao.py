from pydantic import Field
from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel

from models.produto import ProdutoDto


class Transacao(BaseModel):
    _id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    quantidade: int
    data_transacao: datetime | None
    listaDosProdutos: list[ProdutoDto]

    @property
    def id(self):
        return self._id

