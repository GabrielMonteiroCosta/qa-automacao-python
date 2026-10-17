import pytest
from playwright.sync_api import expect

from pages.pagina_carrinho import PaginaCarrinho
from pages.pagina_checkout import PaginaCheckout

pytestmark = pytest.mark.ui

# Produtos usados na compra e seus preços no site (em dólar)
PRODUTOS = {"sauce-labs-backpack": 29.99, "sauce-labs-bike-light": 9.99}


@pytest.fixture
def checkout(produtos, page):
    """Coloca os produtos no carrinho e abre a etapa de dados do comprador."""
    for produto in PRODUTOS:
        produtos.adicionar_ao_carrinho(produto)
    produtos.abrir_carrinho()

    carrinho = PaginaCarrinho(page)
    expect(carrinho.itens).to_have_count(len(PRODUTOS))
    carrinho.ir_para_checkout()
    return PaginaCheckout(page)


def test_compra_completa_com_valores_corretos(checkout, faker):
    checkout.preencher_dados(faker.first_name(), faker.last_name(), faker.postcode())

    # Regras de negócio do resumo: subtotal = soma dos itens; total = subtotal + imposto
    valores = checkout.valores_do_resumo()
    assert valores["subtotal"] == pytest.approx(sum(PRODUTOS.values()))
    assert valores["total"] == pytest.approx(valores["subtotal"] + valores["imposto"])

    checkout.concluir()
    expect(checkout.mensagem_sucesso).to_have_text("Thank you for your order!")


@pytest.mark.parametrize(
    "nome, sobrenome, cep, mensagem",
    [
        ("", "Silva", "01001-000", "Error: First Name is required"),
        ("Ana", "", "01001-000", "Error: Last Name is required"),
        ("Ana", "Silva", "", "Error: Postal Code is required"),
    ],
    ids=["sem-nome", "sem-sobrenome", "sem-cep"],
)
def test_checkout_exige_os_dados_do_comprador(checkout, nome, sobrenome, cep, mensagem):
    checkout.preencher_dados(nome, sobrenome, cep)

    expect(checkout.mensagem_erro).to_have_text(mensagem)
