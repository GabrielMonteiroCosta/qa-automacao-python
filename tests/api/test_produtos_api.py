import pytest
from jsonschema import validate

from api import esquemas

pytestmark = pytest.mark.api


def test_administrador_cadastra_produto(api, token_admin, dados_produto, produtos_para_excluir):
    resposta = api.criar_produto(dados_produto, token_admin)

    assert resposta.status_code == 201
    corpo = resposta.json()
    produtos_para_excluir.append(corpo["_id"])
    assert corpo["message"] == "Cadastro realizado com sucesso"


def test_buscar_produto_respeita_o_contrato(api, produto):
    resposta = api.buscar_produto(produto["_id"])

    assert resposta.status_code == 200
    corpo = resposta.json()
    validate(instance=corpo, schema=esquemas.PRODUTO)
    assert corpo == produto


def test_cadastro_de_produto_sem_token_e_recusado(api, dados_produto):
    resposta = api.criar_produto(dados_produto)

    assert resposta.status_code == 401
    assert resposta.json() == {
        "message": "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"
    }


def test_usuario_comum_nao_cadastra_produto(api, token_usuario_comum, dados_produto):
    resposta = api.criar_produto(dados_produto, token_usuario_comum)

    assert resposta.status_code == 403
    assert resposta.json() == {"message": "Rota exclusiva para administradores"}


def test_nao_permite_produto_com_nome_repetido(api, produto, token_admin, produtos_para_excluir):
    dados_repetidos = {campo: valor for campo, valor in produto.items() if campo != "_id"}

    resposta = api.criar_produto(dados_repetidos, token_admin)

    if resposta.status_code == 201:  # se a regra falhar, não deixa lixo na API
        produtos_para_excluir.append(resposta.json()["_id"])
    assert resposta.status_code == 400
    assert resposta.json() == {"message": "Já existe produto com esse nome"}


def test_excluir_produto(api, token_admin, dados_produto, produtos_para_excluir):
    criado = api.criar_produto(dados_produto, token_admin)
    assert criado.status_code == 201
    id_produto = criado.json()["_id"]
    produtos_para_excluir.append(id_produto)

    resposta = api.excluir_produto(id_produto, token_admin)

    assert resposta.status_code == 200
    assert resposta.json() == {"message": "Registro excluído com sucesso"}
    assert api.buscar_produto(id_produto).status_code == 400
