import pytest
from jsonschema import validate

from api import esquemas

pytestmark = pytest.mark.api


def test_cadastrar_usuario_com_sucesso(api, dados_usuario, ids_para_excluir):
    resposta = api.criar_usuario(dados_usuario)

    assert resposta.status_code == 201
    corpo = resposta.json()
    ids_para_excluir.append(corpo["_id"])
    assert corpo["message"] == "Cadastro realizado com sucesso"


def test_nao_permite_cadastrar_email_repetido(api, usuario, ids_para_excluir):
    dados_repetidos = {campo: valor for campo, valor in usuario.items() if campo != "_id"}

    resposta = api.criar_usuario(dados_repetidos)

    if resposta.status_code == 201:  # se a regra falhar, não deixa lixo na API
        ids_para_excluir.append(resposta.json()["_id"])
    assert resposta.status_code == 400
    assert resposta.json() == {"message": "Este email já está sendo usado"}


def test_cadastro_vazio_informa_os_campos_obrigatorios(api):
    resposta = api.criar_usuario({})

    assert resposta.status_code == 400
    assert resposta.json() == {
        "nome": "nome é obrigatório",
        "email": "email é obrigatório",
        "password": "password é obrigatório",
        "administrador": "administrador é obrigatório",
    }


def test_cadastro_com_email_invalido(api, dados_usuario):
    resposta = api.criar_usuario({**dados_usuario, "email": "email-sem-arroba"})

    assert resposta.status_code == 400
    assert resposta.json() == {"email": "email deve ser um email válido"}


def test_buscar_usuario_por_id_respeita_o_contrato(api, usuario):
    resposta = api.buscar_usuario(usuario["_id"])

    assert resposta.status_code == 200
    corpo = resposta.json()
    validate(instance=corpo, schema=esquemas.USUARIO)
    assert corpo == usuario


def test_buscar_usuario_inexistente(api):
    # O ServeRest responde 400 (e não 404) quando o id não existe
    resposta = api.buscar_usuario("0000000000000000")

    assert resposta.status_code == 400
    assert resposta.json() == {"message": "Usuário não encontrado"}


def test_listar_usuarios_filtrando_por_email(api, usuario):
    resposta = api.listar_usuarios(email=usuario["email"])

    assert resposta.status_code == 200
    corpo = resposta.json()
    validate(instance=corpo, schema=esquemas.LISTA_DE_USUARIOS)
    assert corpo["quantidade"] == 1
    assert corpo["usuarios"][0]["_id"] == usuario["_id"]


def test_atualizar_nome_do_usuario(api, usuario):
    novo_nome = f"{usuario['nome']} Alterado"
    dados = {**usuario, "nome": novo_nome}
    del dados["_id"]

    resposta = api.atualizar_usuario(usuario["_id"], dados)

    assert resposta.status_code == 200
    assert resposta.json() == {"message": "Registro alterado com sucesso"}
    assert api.buscar_usuario(usuario["_id"]).json()["nome"] == novo_nome


def test_excluir_usuario(api, dados_usuario, ids_para_excluir):
    criado = api.criar_usuario(dados_usuario)
    assert criado.status_code == 201
    id_usuario = criado.json()["_id"]
    ids_para_excluir.append(id_usuario)

    resposta = api.excluir_usuario(id_usuario)

    assert resposta.status_code == 200
    assert resposta.json() == {"message": "Registro excluído com sucesso"}
    assert api.buscar_usuario(id_usuario).status_code == 400
