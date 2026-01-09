
from models.produto import Produto,ProdutoDto, ProdutoUpdate, produtoList_serializer
from fastapi import HTTPException
from beanie.odm.fields import PydanticObjectId


async def produtosPorNome(nome,limit,offset):
    try:
        produtosLista = await Produto.find(Produto.mercadoria == nome).skip(offset).limit(limit).to_list()

    except:
        return "Nao foi possivel encontrar o produto."

    return produtosLista


async def produtosPorCategoria(categoria,limit,offset):
    try:
        produtosLista = await Produto.find(Produto.categoria == categoria).skip(offset).limit(limit).to_list()

    except:
        return "Nao foi possivel encontrar o produto."

    return produtosLista


async def cadastrarProduto(novoProduto: ProdutoDto):
   
   try:
       newP = Produto(
       mercadoria=novoProduto.mercadoria,
       valor=novoProduto.valor,
       categoria=novoProduto.categoria)

       await newP.insert()

       return newP
     
   except:
        return "Nao foi possivel cadastrar o produto."


async def cadastrarMuitosProduto(listaNovosProdutosDTO: list[ProdutoDto]):
    try:
        ListaNovosProdutos = produtoList_serializer(listaNovosProdutosDTO)
        await Produto.insert_many(ListaNovosProdutos)
    except:
        return "Nao foi possivel cadastrar muitos produtos."

    return "Muitos produtos cadastrados com sucesso"


async def deletarProduto(id: PydanticObjectId):
    try:
        produto = await Produto.find_one(Produto.id == id)

        if(produto):
            await produto.delete()
            return "Produto excluido com sucesso"
        
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


        produto = await Produto.find_one(Produto.id == id)
        await produto.set(update_filds)

        return produto


    except ValueError as e:
        if(len(e.args) != 0):
            return e.args[0] 
    
        raise HTTPException(status_code=404, detail="Item not found")

        
        







































        