from pydantic import BaseModel, ConfigDict
from beanie import Document


class Fornecedor(Document):
    cnpj: int
    nome: str
    contato: str
    endereco: str

    class Settings:
        name = "fornecedor"


class FornecedorDTO(BaseModel):
    cnpj: int
    nome: str
    contato: str
    endereco: str

    model_config = ConfigDict(extra="forbid")


class FornecedorUpdate(BaseModel):
    cnpj: int | None = None
    nome: str | None = None
    contato: str | None = None
    endereco: str | None = None

    model_config = ConfigDict(extra="forbid")




