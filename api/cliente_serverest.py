import os

import requests

# Pode apontar para outra instância (ex.: ServeRest rodando localmente) pela variável de ambiente
URL_SERVEREST = os.getenv("SERVEREST_URL", "https://serverest.dev")
TEMPO_LIMITE = 15  # segundos


class ClienteServeRest:
    """Reúne as chamadas à API ServeRest usadas nos testes.

    Os testes ficam focados no que é verificado; os detalhes de URL,
    método HTTP e cabeçalhos ficam aqui.
    """

    def __init__(self, url_base: str = URL_SERVEREST):
        self.url_base = url_base
        self.sessao = requests.Session()

    def _chamar(self, metodo: str, caminho: str, token: str | None = None, **kwargs) -> requests.Response:
        headers = {"Authorization": token} if token else {}
        return self.sessao.request(metodo, f"{self.url_base}{caminho}", headers=headers, timeout=TEMPO_LIMITE, **kwargs)

    # Usuários
    def criar_usuario(self, dados: dict):
        return self._chamar("POST", "/usuarios", json=dados)

    def listar_usuarios(self, **filtros):
        return self._chamar("GET", "/usuarios", params=filtros)

    def buscar_usuario(self, id_usuario: str):
        return self._chamar("GET", f"/usuarios/{id_usuario}")

    def atualizar_usuario(self, id_usuario: str, dados: dict):
        return self._chamar("PUT", f"/usuarios/{id_usuario}", json=dados)

    def excluir_usuario(self, id_usuario: str):
        return self._chamar("DELETE", f"/usuarios/{id_usuario}")

    # Login
    def login(self, email: str, senha: str):
        return self._chamar("POST", "/login", json={"email": email, "password": senha})

    # Produtos (cadastro e exclusão exigem token de administrador)
    def criar_produto(self, dados: dict, token: str | None = None):
        return self._chamar("POST", "/produtos", token=token, json=dados)

    def buscar_produto(self, id_produto: str):
        return self._chamar("GET", f"/produtos/{id_produto}")

    def excluir_produto(self, id_produto: str, token: str):
        return self._chamar("DELETE", f"/produtos/{id_produto}", token=token)
