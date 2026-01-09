
from dtos.createFornecedorDTO import FornecedorDTO



async def listarFornecedores(page: int = 1, page_size: int = 10):
    return 1


async def buscar_fornecedor_por_nome(nome: str, limit: int = 20, offset: int = 0):
    return 1


async def lerFornecedor(id: int):
    return 1


async def cadastrarFornecedor(novoFornecedor: FornecedorDTO):
    return 1


async def atualizarFornecedor(id: int, newData: FornecedorDTO):
    return 1


async def deletarFornecedor(id: int):
    return 1


async def contar_fornecedores():
    return 1


async def ordenar_fornecedores_por_nome():
    return 1
