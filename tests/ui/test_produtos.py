import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

MOCHILA = "sauce-labs-backpack"


def test_adicionar_produto_atualiza_o_contador_do_carrinho(produtos):
    produtos.adicionar_ao_carrinho(MOCHILA)

    expect(produtos.contador_carrinho).to_have_text("1")


def test_remover_produto_esconde_o_contador_do_carrinho(produtos):
    produtos.adicionar_ao_carrinho(MOCHILA)
    produtos.remover_do_carrinho(MOCHILA)

    expect(produtos.contador_carrinho).to_be_hidden()


@pytest.mark.parametrize(
    "opcao, decrescente",
    [("lohi", False), ("hilo", True)],
    ids=["menor-preco-primeiro", "maior-preco-primeiro"],
)
def test_ordenar_produtos_por_preco(produtos, opcao, decrescente):
    produtos.ordenar_por(opcao)

    precos = produtos.listar_precos()
    assert precos, "Nenhum preço encontrado na tela"
    assert precos == sorted(precos, reverse=decrescente)
