import re

import pytest
from playwright.sync_api import Page, expect

from pages.pagina_login import PaginaLogin

pytestmark = pytest.mark.ui


def test_login_com_sucesso_abre_a_lista_de_produtos(produtos, page: Page):
    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(produtos.titulo).to_have_text("Products")


@pytest.mark.parametrize(
    "usuario, senha, mensagem",
    [
        ("", "secret_sauce", "Epic sadface: Username is required"),
        ("standard_user", "", "Epic sadface: Password is required"),
        ("standard_user", "senha_errada", "Epic sadface: Username and password do not match any user in this service"),
        ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out."),
    ],
    ids=["sem-usuario", "sem-senha", "senha-errada", "usuario-bloqueado"],
)
def test_login_invalido_mostra_erro_e_nao_entra(pagina_login, page: Page, usuario, senha, mensagem):
    pagina_login.entrar(usuario, senha)

    expect(pagina_login.mensagem_erro).to_have_text(mensagem)
    expect(page).not_to_have_url(re.compile(r"/inventory\.html"))


def test_logout_volta_para_a_tela_de_login(produtos, page: Page):
    produtos.sair()

    expect(PaginaLogin(page).botao_entrar).to_be_visible()
