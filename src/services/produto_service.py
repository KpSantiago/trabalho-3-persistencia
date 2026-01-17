import logging
from models.produto import Produto,ProdutoDto, ProdutoUpdate, produtoList_serializer
from fastapi import HTTPException
from beanie.odm.fields import PydanticObjectId

logger = logging.getLogger(__name__)

async def produtosPorNome(nome,limit,offset):
    try:
        produtosLista = await Produto.find(Produto.mercadoria == nome).skip(offset).limit(limit).to_list()

        if not len(produtosLista):
            raise HTTPException(404, "Nada encontrado")
        
    except HTTPException:
        raise

    except Exception:
        logger.error(
        "Erro ao acessar produtos",
        exc_info=True
        )
        raise HTTPException(status_code=500, detail="Erro interno ao acessar produtos.")

    return produtosLista

async def produtosPorNomeParcial(mercadoria):
    try:
        pipeLine = [
            {
                "$project": {"_id": 0}
            },
                {
                    "$match": {"mercadoria":{"$regex": mercadoria,"$options": "i"}}
                }
        ]

        response = await Produto.aggregate(pipeLine).to_list()
    except Exception:
        logger.error(
        "Erro ao acessar produtos",
        exc_info=True
        )
        raise HTTPException(status_code=500, detail="Erro interno ao acessar produtos.")

    return response

async def produtosPorCategoria(categoria,limit,offset):
    try:
        produtosLista = await Produto.find(Produto.categoria == categoria).skip(offset).limit(limit).to_list()

        if len(produtosLista) == 0:
            raise HTTPException(404, "Nada encontrado")
        
    except HTTPException:
        raise

    except Exception:
        logger.error(
        "Erro ao acessar produtos",
        exc_info=True
        )
        raise HTTPException(status_code=500, detail="Erro interno ao acessar produtos.")

    return produtosLista

async def produtosQuantidade():
    try:
        qtdProdutos = await Produto.count()
    except Exception:
        logger.error(
        "Erro ao acessar produtos",
        exc_info=True
        )
        raise HTTPException(status_code=500, detail="Erro interno ao acessar produtos.")

    return qtdProdutos

async def totalVendasDaCategoria(categoria):
    try:
        pipeLine = [
                {
                    "$match": {"categoria":{"$regex": categoria,"$options": "i"}}
                },
                
                {
                    "$group": {
                        "_id": "$categoria",
                        "totalVendas": {"$sum": "$valor"}
                    }
                }
        ]
        response = await Produto.aggregate(pipeLine).to_list()
    except Exception:
        logger.error(
        "Erro ao acessar produtos",
        exc_info=True
        )
        raise HTTPException(status_code=500, detail="Erro interno ao acessar produtos.")

    return response

async def produtosPorPreco(typeSort,limit,offset):
    try:
        pipeLine = [
            {
                "$project": {"_id": 0}
            },
            {
                "$sort": {
                    "valor": typeSort
       
                }
            },
            {
                "$limit": limit
            },
            {
                "$skip": offset
            }
        ]
        response = await Produto.aggregate(pipeLine).to_list()
    except Exception:
        logger.error(
        "Erro ao acessar produtos",
        exc_info=True
        )
        raise HTTPException(status_code=500, detail="Erro interno ao acessar produtos.")

    return response

async def cadastrarProduto(novoProduto: ProdutoDto):
   try:
       newP = Produto(
       mercadoria=novoProduto.mercadoria,
       valor=novoProduto.valor,
       categoria=novoProduto.categoria)
       await newP.insert()

       return newP
     
   except Exception:
        logger.error(
        "Erro ao cadastra produto.",
        exc_info=True
        )
        raise HTTPException(status_code=500, detail="Erro interno ao cadastrar produto.")      

async def cadastrarMuitosProduto(listaNovosProdutosDTO: list[ProdutoDto]):
    try:
        ListaNovosProdutos = produtoList_serializer(listaNovosProdutosDTO)
        await Produto.insert_many(ListaNovosProdutos)

    except Exception:
        logger.error(
        "Erro ao cadastrar muitos produtos",
        exc_info=True
        )
        raise HTTPException(status_code=500, detail="Erro interno ao cadastrar muitos produtos.")

    return ListaNovosProdutos

async def deletarProduto(id: PydanticObjectId):
    try:
        produto = await Produto.find_one(Produto.id == id)

        if(produto):
            await produto.delete()
            return "Produto excluido com sucesso"
        
        if not produto:
            raise HTTPException(404, "Produto inexistente")
        
    except HTTPException:
        raise
    
    except Exception:
        logger.error(
        "Erro ao deletar produto",
        exc_info=True
        )
        raise HTTPException(status_code=500, detail="Erro interno ao deletera produto.")

async def atualizarProduto(id,update: ProdutoUpdate):
    
    try:
        if update.categoria is None and update.mercadoria is None and update.valor is None:
            raise HTTPException(status_code=400, detail="Modelo de requisiçao invalido.")
        
        chavesRequest = dict(update).keys()

        update_filds = dict(update)
        for key in chavesRequest:
            if(update_filds[key] == None):
                del update_filds[key]


        produto = await Produto.find_one(Produto.id == id)
        await produto.set(update_filds)

        return produto

    except HTTPException:
        raise

    except Exception:
        logger.error(
        "Erro ao atualizar produto",
        exc_info=True
        )
    
        raise HTTPException(status_code=500, detail="Erro interno ao atualizar produto.")

        
        







































        
