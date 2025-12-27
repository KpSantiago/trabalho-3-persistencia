
from database.database import ProductsCollection
from models.produto import Produto, ProdutoUpdate
from deserializer.deserializer import produto_serializer, produtoList_serializer
from fastapi import FastAPI, HTTPException
from bson import ObjectId


async def produtosPorNome(nome,limit,offset):
    cursor = ProductsCollection.find({"mercadoria": nome}).skip(offset)
    produtosDocList = await cursor.to_list(limit)

    if len(produtosDocList) == 0:
        raise HTTPException(status_code=404, detail="Itens not found")
    
    produtosList = produtoList_serializer(produtosDocList)

    return produtosList


async def produtosPorCategoria(categoria,limit,offset):
    cursor = ProductsCollection.find({"categoria": categoria}).skip(offset)
    produtosDocList = await cursor.to_list(limit)

    if len(produtosDocList) == 0:
        raise HTTPException(status_code=404, detail="Itens not found")

    produtosList = produtoList_serializer(produtosDocList)
    return produtosList


async def cadastrarProduto(novoProduto: Produto):
    try:
        await ProductsCollection.insert_one(dict(novoProduto))
    except:
        return "Nao foi possivel cadastrar o produto."

    return novoProduto


async def deletarProduto(id):
    try:
        query_filter = { "_id": ObjectId(id) }
        result = await ProductsCollection.delete_one(query_filter)
        
        if(result.deleted_count != 0):
            return "Elemento excluido com sucesso"
        
        raise ValueError("O produto nao existe.")
    
    except ValueError as e:
        return e.args[0]


async def atualizarProduto(id,update: ProdutoUpdate):
    try:
        i = 0
        chavesClasse = list(ProdutoUpdate.model_fields.keys())
        chavesRequest = dict(update).keys()

        for key in chavesRequest:
            if key != chavesClasse[i]:
                raise ValueError("Modelo de requisicao invalida.")
            i += 1

        update_filds = dict(update)
        for key in chavesRequest:
            if(update_filds[key] == None):
                del update_filds[key]


        query_filter = { "_id": ObjectId(id) }
        update_obj = {"$set": update_filds}

        result = await ProductsCollection.update_one(query_filter, update_obj)

    
        return 1


    except ValueError as e:
        return e.args[0]


# async def fornecedoresDeProdutos():
#     print()


# async def ProdutosDataTransacoes():
#     print()





































        