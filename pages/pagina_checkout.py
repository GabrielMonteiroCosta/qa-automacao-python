from playwright.sync_api import Page

from pages.utils import extrair_valor


class PaginaCheckout:
    """As três etapas finais da compra: dados do comprador, resumo e confirmação."""

    def __init__(self, page: Page):
        self.page = page
        # Etapa 1: dados do comprador
        self.campo_nome = page.get_by_test_id("firstName")
        self.campo_sobrenome = page.get_by_test_id("lastName")
        self.campo_cep = page.get_by_test_id("postalCode")
        self.botao_continuar = page.get_by_test_id("continue")
        self.mensagem_erro = page.get_by_test_id("error")
        # Etapa 2: resumo com os valores
        self.subtotal = page.get_by_test_id("subtotal-label")
        self.imposto = page.get_by_test_id("tax-label")
        self.total = page.get_by_test_id("total-label")
        self.botao_concluir = page.get_by_test_id("finish")
        # Etapa 3: confirmação
        self.mensagem_sucesso = page.get_by_test_id("complete-header")

    def preencher_dados(self, nome: str, sobrenome: str, cep: str):
        self.campo_nome.fill(nome)
        self.campo_sobrenome.fill(sobrenome)
        self.campo_cep.fill(cep)
        self.botao_continuar.click()

    def valores_do_resumo(self) -> dict[str, float]:
        return {
            "subtotal": extrair_valor(self.subtotal.inner_text()),
            "imposto": extrair_valor(self.imposto.inner_text()),
            "total": extrair_valor(self.total.inner_text()),
        }

    def concluir(self):
        self.botao_concluir.click()
