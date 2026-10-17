from playwright.sync_api import Page


class PaginaCarrinho:
    """Carrinho de compras."""

    def __init__(self, page: Page):
        self.page = page
        self.itens = page.get_by_test_id("inventory-item")
        self.botao_finalizar = page.get_by_test_id("checkout")

    def ir_para_checkout(self):
        self.botao_finalizar.click()
