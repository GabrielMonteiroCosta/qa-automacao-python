"""Lê o resultado do JMeter (.jtl em CSV) e confere os critérios de aceite do teste de carga.

Uso:
    python scripts/verificar_carga.py resultados.jtl --max-erros 1 --p95 2000

Termina com código 1 se algum critério não for atendido, o que faz o GitHub Actions marcar falha.
"""

import argparse
import csv
import math
import sys


def percentil(valores: list[int], p: float) -> int:
    ordenados = sorted(valores)
    posicao = math.ceil(p / 100 * len(ordenados)) - 1
    return ordenados[max(posicao, 0)]


def main() -> int:
    parser = argparse.ArgumentParser(description="Confere os critérios de aceite do teste de carga.")
    parser.add_argument("arquivo_jtl")
    parser.add_argument("--max-erros", type=float, default=1.0, help="taxa máxima de erros, em %% (padrão: 1)")
    parser.add_argument("--p95", type=int, default=2000, help="tempo máximo do percentil 95, em ms (padrão: 2000)")
    args = parser.parse_args()

    with open(args.arquivo_jtl, newline="", encoding="utf-8-sig") as arquivo:
        amostras = list(csv.DictReader(arquivo))

    if not amostras:
        print("Nenhuma requisição encontrada no arquivo.")
        return 1

    tempos = [int(linha["elapsed"]) for linha in amostras]
    erros = sum(1 for linha in amostras if linha["success"].lower() != "true")
    taxa_erros = erros / len(amostras) * 100
    p95 = percentil(tempos, 95)

    print(f"Requisições: {len(amostras)}")
    print(f"Erros: {erros} ({taxa_erros:.2f}%) | limite: {args.max_erros}%")
    print(f"Tempo médio: {sum(tempos) / len(tempos):.0f} ms | p95: {p95} ms | limite p95: {args.p95} ms")

    aprovado = taxa_erros <= args.max_erros and p95 <= args.p95
    print("Resultado: APROVADO" if aprovado else "Resultado: REPROVADO")
    return 0 if aprovado else 1


if __name__ == "__main__":
    sys.exit(main())
