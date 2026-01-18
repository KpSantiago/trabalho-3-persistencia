import asyncio
import random

from faker import Faker

from database.database import initDB
from models.fornecedor import Fornecedor
from models.produto import Produto, ProdutoDto
from models.produtoFornecedor import ProdutoFornecedor
from models.transacao import Transacao


async def popular_db(
	qtd_fornecedores: int = 10,
	qtd_produtos: int = 50,
	relacoes_por_produto_min: int = 1,
	relacoes_por_produto_max: int = 3,
	transacoes_por_fornecedor: int = 5,
):
	faker = Faker("pt_BR")

	categorias = [
		"Alimentos",
		"Bebidas",
		"Higiene",
		"Limpeza",
		"Eletrônicos",
		"Vestuário",
		"Papelaria",
		"Ferramentas",
	]

	fornecedores = []
	for _ in range(qtd_fornecedores):
		fornecedores.append(
			Fornecedor(
				cnpj=faker.random_number(digits=14, fix_len=True),
				nome=faker.company(),
				contato=faker.phone_number(),
				endereco=faker.address(),
			)
		)

	inserted_fornecedores = []
	for f in fornecedores:
		await f.insert()
		inserted_fornecedores.append(f)
	fornecedores = inserted_fornecedores

	produtos = []
	for _ in range(qtd_produtos):
		nome_produto = faker.word().capitalize()
		categoria = random.choice(categorias)
		valor = round(random.uniform(5.0, 1000.0), 2)
		produtos.append(Produto(mercadoria=nome_produto, valor=valor, categoria=categoria))

	inserted_produtos = []
	for p in produtos:
		await p.insert()
		inserted_produtos.append(p)
	produtos = inserted_produtos

	relacoes = []
	fornecedor_ids = [f.id for f in fornecedores]
	for p in produtos:
		qtd_relacoes = random.randint(relacoes_por_produto_min, relacoes_por_produto_max)
		fornecedores_escolhidos = random.sample(
			fornecedor_ids, k=min(qtd_relacoes, len(fornecedor_ids))
		)
		for forn_id in fornecedores_escolhidos:
			relacoes.append(ProdutoFornecedor(produto_id=p.id, fornecedor_id=forn_id))

	if relacoes:
		await ProdutoFornecedor.insert_many(relacoes)

	for forn in fornecedores:
		rels = await ProdutoFornecedor.find(ProdutoFornecedor.fornecedor_id == forn.id).to_list()
		produtos_ids = [r.produto_id for r in rels]
		if not produtos_ids:
			continue

		produtos_do_fornecedor = []
		for pid in produtos_ids:
			prod = await Produto.get(pid)
			if prod is not None:
				produtos_do_fornecedor.append(prod)

		if not produtos_do_fornecedor:
			continue

		for _ in range(transacoes_por_fornecedor):
			selecionados = random.sample(
				produtos_do_fornecedor, k=min(len(produtos_do_fornecedor), random.randint(1, 5))
			)

			lista_produtos_dto = [
				ProdutoDto(mercadoria=p.mercadoria, valor=p.valor, categoria=p.categoria)
				for p in selecionados
			]

			data_transacao = faker.date_time_between(start_date="-90d", end_date="now")

			transacao = Transacao(
				quantidade=len(lista_produtos_dto),
				data_transacao=data_transacao,
				listaDosProdutos=lista_produtos_dto,
			)

			await Fornecedor.update(forn, {"$push": {"transacoesFornecedor": transacao}})


async def main():
	await initDB()
	await popular_db(
		qtd_fornecedores=10,
		qtd_produtos=60,
		relacoes_por_produto_min=1,
		relacoes_por_produto_max=3,
		transacoes_por_fornecedor=4,
	)

	total_fornecedores = await Fornecedor.count()
	total_produtos = await Produto.count()
	total_relacoes = await ProdutoFornecedor.count()

	print({
		"fornecedores": total_fornecedores,
		"produtos": total_produtos,
		"relacoes": total_relacoes,
	})


if __name__ == "__main__":
	asyncio.run(main())

