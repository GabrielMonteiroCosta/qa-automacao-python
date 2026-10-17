import re


def extrair_valor(texto: str) -> float:
    """Converte textos como "$29.99" ou "Item total: $39.98" em número."""
    encontrado = re.search(r"\$(\d+(?:\.\d+)?)", texto)
    if not encontrado:
        raise ValueError(f"Nenhum valor em dólar encontrado em: {texto!r}")
    return float(encontrado.group(1))
