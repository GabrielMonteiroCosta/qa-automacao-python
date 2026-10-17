import pytest

from pages.pagina_login import PaginaLogin
from pages.pagina_produtos import PaginaProdutos

# Usuário e senha de demonstração divulgados na própria tela do Sauce Demo
USUARIO_PADRAO = "standard_user"
SENHA_PADRAO = "secret_sauce"


@pytest.fixture(scope="session", autouse=True)
def usar_atributo_data_test(playwright):
    """O Sauce Demo marca os elementos com data-test; get_by_test_id passa a procurar por ele."""
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture
def pagina_login(page):
    login = PaginaLogin(page)
    login.abrir()
    return login


@pytest.fixture
def produtos(pagina_login, page):
    """Entra com o usuário padrão e devolve a tela de produtos."""
    pagina_login.entrar(USUARIO_PADRAO, SENHA_PADRAO)
    return PaginaProdutos(page)
