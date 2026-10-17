import uuid

import pytest

from api.cliente_serverest import ClienteServeRest


@pytest.fixture(scope="session")
def api():
    return ClienteServeRest()


def _email_unico() -> str:
    # A API é pública e compartilhada: um e-mail aleatório evita colisão com dados de outras pessoas
    return f"qa.{uuid.uuid4().hex[:12]}@teste.com.br"


@pytest.fixture
def dados_usuario(faker):
    return {
        "nome": faker.name(),
        "email": _email_unico(),
        "password": faker.password(length=10),
        "administrador": "true",
    }


@pytest.fixture
def ids_para_excluir(api):
    """Guarda os usuários criados dentro de um teste e apaga todos no final, mesmo se o teste falhar."""
    ids = []
    yield ids
    for id_usuario in ids:
        api.excluir_usuario(id_usuario)


def _criar_usuario(api, dados):
    resposta = api.criar_usuario(dados)
    assert resposta.status_code == 201, resposta.text
    return {**dados, "_id": resposta.json()["_id"]}


@pytest.fixture
def usuario(api, dados_usuario):
    """Usuário administrador criado antes do teste e apagado depois."""
    usuario = _criar_usuario(api, dados_usuario)
    yield usuario
    api.excluir_usuario(usuario["_id"])


@pytest.fixture
def usuario_comum(api, faker):
    """Usuário sem permissão de administrador."""
    dados = {"nome": faker.name(), "email": _email_unico(), "password": faker.password(length=10), "administrador": "false"}
    usuario = _criar_usuario(api, dados)
    yield usuario
    api.excluir_usuario(usuario["_id"])


def _token(api, usuario):
    resposta = api.login(usuario["email"], usuario["password"])
    assert resposta.status_code == 200, resposta.text
    return resposta.json()["authorization"]


@pytest.fixture
def token_admin(api, usuario):
    return _token(api, usuario)


@pytest.fixture
def token_usuario_comum(api, usuario_comum):
    return _token(api, usuario_comum)


@pytest.fixture
def dados_produto(faker):
    return {
        "nome": f"Produto QA {uuid.uuid4().hex[:8]}",
        "preco": faker.random_int(min=10, max=500),
        "descricao": faker.sentence(nb_words=4),
        "quantidade": faker.random_int(min=1, max=50),
    }


@pytest.fixture
def produtos_para_excluir(api, token_admin):
    """Guarda os produtos criados dentro de um teste e apaga todos no final."""
    ids = []
    yield ids
    for id_produto in ids:
        api.excluir_produto(id_produto, token_admin)


@pytest.fixture
def produto(api, token_admin, dados_produto):
    """Produto cadastrado por um administrador e apagado depois do teste."""
    resposta = api.criar_produto(dados_produto, token_admin)
    assert resposta.status_code == 201, resposta.text
    produto = {**dados_produto, "_id": resposta.json()["_id"]}
    yield produto
    api.excluir_produto(produto["_id"], token_admin)
