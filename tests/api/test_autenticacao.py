import uuid

import pytest

pytestmark = pytest.mark.api


def test_login_com_sucesso_devolve_token(api, usuario):
    resposta = api.login(usuario["email"], usuario["password"])

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["message"] == "Login realizado com sucesso"
    assert corpo["authorization"].startswith("Bearer ")


@pytest.mark.parametrize("campo_errado", ["email", "senha"])
def test_login_com_credenciais_erradas(api, usuario, campo_errado):
    email = f"inexistente.{uuid.uuid4().hex[:8]}@teste.com.br" if campo_errado == "email" else usuario["email"]
    senha = "senha-errada" if campo_errado == "senha" else usuario["password"]

    resposta = api.login(email, senha)

    assert resposta.status_code == 401
    assert resposta.json() == {"message": "Email e/ou senha inválidos"}
