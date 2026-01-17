from pydantic import BaseModel, ConfigDict
from beanie import Document
from beanie.odm.fields import PydanticObjectId

class ProdutoFornecedor(Document):
    produto_id: PydanticObjectId 
    fornecedor_id: PydanticObjectId 

    class Settings:
        name = "produtoFornecedor"

class ProdutoFornecedorDTO(BaseModel):
    produto_id: PydanticObjectId 
    fornecedor_id: PydanticObjectId 

    model_config = ConfigDict(extra="forbid")

class ProdutoFornecedorUpdate(BaseModel):
    produto_id: PydanticObjectId | None = None
    fornecedor_id: PydanticObjectId | None = None

    model_config = ConfigDict(extra="forbid")










