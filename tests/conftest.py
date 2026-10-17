import pytest


@pytest.fixture(scope="session")
def faker_locale():
    """Faz o Faker gerar nomes, CEPs e frases em português do Brasil."""
    return ["pt_BR"]
