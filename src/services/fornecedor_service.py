import logging
from beanie.odm.fields import PydanticObjectId
from exceptions.not_found_exception import NotFoundException
from models.fornecedor import Fornecedor, FornecedorUpdate
from models.produtoFornecedor import ProdutoFornecedor

logger = logging.getLogger(__name__)


async def lerFornecedor(id: str):
    try:
        fornecedor = await Fornecedor.get(PydanticObjectId(id))
        return fornecedor
    except Exception:
        logger.error("Erro ao buscar fornecedor")
        raise NotFoundException("Fornecedor não encontrado")


async def listarFornecedoresComProdutos(page: int = 1, page_size: int = 10):
    try:
        skip = (page - 1) * page_size
        
        pipeline = [
            {
                "$project": {"_id": 0}
            },
            {
                "$lookup": {
                    "from": "produtoFornecedor",
                    "localField": "_id",
                    "foreignField": "fornecedor_id",
                    "as": "produtos"
                }
            },
            {"$skip": skip},
            {"$limit": page_size}
        ]

        return await Fornecedor.aggregate(pipeline).to_list()
    except Exception:
        logger.error("Erro ao listar fornecedores com produtos")
        raise Exception("Erro ao listar fornecedores")


async def listarFornecedoresPorCategoriaProduto(categoria: str, page: int = 1, page_size: int = 10):
    try:
        skip = (page - 1) * page_size
        
        pipeline = [
            {
                "$lookup": {
                    "from": "produtoFornecedor",
                    "localField": "_id",
                    "foreignField": "fornecedor_id",
                    "as": "fornecimentos"
                }
            },
            {
                "$lookup": {
                    "from": "produto",
                    "localField": "fornecimentos.produto_id",
                    "foreignField": "_id",
                    "as": "produtos"
                }
            },
            {
                "$match": {
                    "produtos.categoria": categoria
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "cnpj": 1,
                    "nome": 1,
                    "contato": 1,
                    "endereco": 1,
                    "produtos": {
                        "$map": {
                            "input": "$produtos",
                            "as": "p",
                            "in": {
                                "mercadoria": "$$p.mercadoria",
                                "valor": "$$p.valor",
                                "categoria": "$$p.categoria"
                            }
                        }
                    }
                }
            },
            {"$skip": skip},
            {"$limit": page_size}
        ]

        return await Fornecedor.aggregate(pipeline).to_list()
    except Exception:
        logger.error("Erro ao filtrar por categoria")
        raise Exception("Erro ao filtrar fornecedores")


async def buscar_fornecedor_por_nome(nome: str, limit: int = 20, offset: int = 0):
    try:
        from beanie import PydanticObjectId
        fornecedores = await Fornecedor.find(
            {"nome": {"$regex": nome, "$options": "i"}}
        ).skip(offset).limit(limit).to_list()
        
        return fornecedores
    except Exception:
        logger.error("Erro ao buscar por nome")
        raise Exception("Erro na busca")


async def buscar_fornecedor_por_endereco(endereco: str):
    try:
        fornecedores = await Fornecedor.find(
            {"endereco": {"$regex": endereco, "$options": "i"}}
        ).to_list()
        
        return fornecedores
    except Exception:
        logger.error("Erro ao buscar por endereço")
        raise Exception("Erro na busca")


async def contar_fornecedores():
    try:
        count = await Fornecedor.count()
        return {"total": count}
    except Exception:
        logger.error("Erro ao contar")
        raise Exception("Erro ao contar fornecedores")


async def ordenar_fornecedores_por_nome(ordem: str = "asc", page: int = 1, page_size: int = 10):
    try:
        skip = (page - 1) * page_size
        sort_order = 1 if ordem == "asc" else -1
        
        fornecedores = await Fornecedor.find_all().sort([("nome", sort_order)]).skip(skip).limit(page_size).to_list()
        return fornecedores
    except Exception:
        logger.error("Erro ao ordenar")
        raise Exception("Erro ao ordenar fornecedores")


async def ordenar_fornecedores_por_cnpj(ordem: str = "asc"):
    try:
        sort_order = 1 if ordem == "asc" else -1
        
        fornecedores = await Fornecedor.find_all().sort([("cnpj", sort_order)]).to_list()
        return fornecedores
    except Exception:
        logger.error("Erro ao ordenar por CNPJ")
        raise Exception("Erro ao ordenar fornecedores")

async def listarFornecedores(page: int = 1, page_size: int = 10):
    try:
        skip = (page - 1) * page_size
        fornecedores = await Fornecedor.find_all().skip(skip).limit(page_size).to_list()
        return fornecedores
    except Exception:
        logger.error("Erro ao listar")
        raise Exception("Erro ao listar fornecedores")


async def cadastrarFornecedor(novoFornecedor):
    try:
        fornecedor = Fornecedor(
            cnpj=novoFornecedor.cnpj,
            nome=novoFornecedor.nome,
            contato=novoFornecedor.contato,
            endereco=novoFornecedor.endereco
        )
        await fornecedor.insert()
        return fornecedor
    except Exception:
        logger.error("Erro ao cadastrar")
        raise Exception("Erro ao cadastrar fornecedor")


async def atualizarFornecedor(id: str, newData):
    try:
        fornecedor = await Fornecedor.get(PydanticObjectId(id))
        
        if fornecedor is None:
            raise NotFoundException("Fornecedor não encontrado")
        
        update_data = {}
        if newData.cnpj is not None:
            update_data["cnpj"] = newData.cnpj
        if newData.nome is not None:
            update_data["nome"] = newData.nome
        if newData.contato is not None:
            update_data["contato"] = newData.contato
        if newData.endereco is not None:
            update_data["endereco"] = newData.endereco
        
        if update_data:
            await fornecedor.update({"$set": update_data})
        
        return await Fornecedor.get(PydanticObjectId(id))
    except NotFoundException:
        raise
    except Exception:
        logger.error("Erro ao atualizar")
        raise Exception("Erro ao atualizar fornecedor")


async def deletarFornecedor(id: str):
    try:
        fornecedor = await Fornecedor.get(PydanticObjectId(id))
        
        if fornecedor is None:
            raise NotFoundException("Fornecedor não encontrado")
        
        await ProdutoFornecedor.find({"fornecedor_id": PydanticObjectId(id)}).delete()
        
        await fornecedor.delete()
        
        return True
    except NotFoundException:
        raise
    except Exception:
        logger.error("Erro ao deletar")
        raise Exception("Erro ao deletar fornecedor")
