from playwright.sync_api import Page

from pages.utils import extrair_valor


class PaginaProdutos:
    """Lista de produtos exibida depois do login."""

    def __init__(self, page: Page):
        self.page = page
        self.titulo = page.get_by_test_id("title")
        self.contador_carrinho = page.get_by_test_id("shopping-cart-badge")
        self.link_carrinho = page.get_by_test_id("shopping-cart-link")
        self.ordenacao = page.get_by_test_id("product-sort-container")
        self.precos = page.get_by_test_id("inventory-item-price")

    def adicionar_ao_carrinho(self, produto: str):
        # "produto" é o identificador usado no site, ex.: "sauce-labs-backpack"
        self.page.get_by_test_id(f"add-to-cart-{produto}").click()

    def remover_do_carrinho(self, produto: str):
        self.page.get_by_test_id(f"remove-{produto}").click()

    def ordenar_por(self, opcao: str):
        # Opções do site: "az", "za", "lohi" (menor preço) e "hilo" (maior preço)
        self.ordenacao.select_option(opcao)

    def listar_precos(self) -> list[float]:
        return [extrair_valor(texto) for texto in self.precos.all_inner_texts()]

    def abrir_carrinho(self):
        self.link_carrinho.click()

    def sair(self):
        self.page.get_by_role("button", name="Open Menu").click()
        self.page.get_by_test_id("logout-sidebar-link").click()
