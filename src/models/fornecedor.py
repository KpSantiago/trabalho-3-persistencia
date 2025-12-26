from pydantic import BaseModel
from models.produto import Produto

class Fornecedor(BaseModel):
    cnpj: int
    nome: str
    contato: str
    endereco: str
    produtosFornecedor: list[Produto] | None




