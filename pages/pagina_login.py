from playwright.sync_api import Page


class PaginaLogin:
    """Tela inicial do Sauce Demo, onde o usuário faz login."""

    def __init__(self, page: Page):
        self.page = page
        self.campo_usuario = page.get_by_test_id("username")
        self.campo_senha = page.get_by_test_id("password")
        self.botao_entrar = page.get_by_test_id("login-button")
        self.mensagem_erro = page.get_by_test_id("error")

    def abrir(self):
        self.page.goto("/")

    def entrar(self, usuario: str, senha: str):
        self.campo_usuario.fill(usuario)
        self.campo_senha.fill(senha)
        self.botao_entrar.click()
