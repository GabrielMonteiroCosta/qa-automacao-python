"""Contratos (JSON Schema) das respostas da API.

Se a API mudar o formato de uma resposta (tirar um campo, trocar o tipo,
incluir um campo novo), o teste de contrato falha e avisa.
"""

USUARIO = {
    "type": "object",
    "required": ["nome", "email", "password", "administrador", "_id"],
    "properties": {
        "nome": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"},
        "administrador": {"type": "string", "enum": ["true", "false"]},
        "_id": {"type": "string"},
    },
    "additionalProperties": False,
}

LISTA_DE_USUARIOS = {
    "type": "object",
    "required": ["quantidade", "usuarios"],
    "properties": {
        "quantidade": {"type": "integer", "minimum": 0},
        "usuarios": {"type": "array", "items": USUARIO},
    },
    "additionalProperties": False,
}

PRODUTO = {
    "type": "object",
    "required": ["nome", "preco", "descricao", "quantidade", "_id"],
    "properties": {
        "nome": {"type": "string"},
        "preco": {"type": "integer", "minimum": 1},
        "descricao": {"type": "string"},
        "quantidade": {"type": "integer", "minimum": 0},
        "_id": {"type": "string"},
    },
    "additionalProperties": False,
}
