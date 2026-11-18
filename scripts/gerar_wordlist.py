#!/usr/bin/env python3
"""Gerador didático de wordlists personalizadas para testes em laboratório.

Uso educacional em ambientes controlados e autorizados.
Exemplo:
    python3 scripts/gerar_wordlist.py --palavras lab dvwa admin --anos 2024 2025 2026 --saida wordlists/custom.txt
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable


def gerar_variacoes(palavras: Iterable[str], anos: Iterable[str], sufixos: Iterable[str]) -> list[str]:
    """Gera variações simples (capitalização, anos e sufixos) sem duplicatas."""
    resultados: list[str] = []
    vistos: set[str] = set()

    def adicionar(candidato: str) -> None:
        if candidato and candidato not in vistos:
            vistos.add(candidato)
            resultados.append(candidato)

    for palavra in palavras:
        limpa = palavra.strip()
        if not limpa:
            continue

        formas = [limpa.lower(), limpa.capitalize(), limpa.upper()]
        for forma in formas:
            adicionar(forma)
            for ano in anos:
                adicionar(f"{forma}{ano}")
                adicionar(f"{forma}@{ano}")
            for sufixo in sufixos:
                adicionar(f"{forma}{sufixo}")

    return resultados


def parse_args() -> argparse.Namespace:
    """Interpreta argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        description="Gera uma wordlist enxuta e controlada para estudo em laboratório."
    )
    parser.add_argument(
        "--palavras",
        nargs="+",
        required=True,
        help="Palavras-base relacionadas ao ambiente de laboratório (ex.: admin dvwa lab).",
    )
    parser.add_argument(
        "--anos",
        nargs="*",
        default=["123", "2024", "2025", "2026"],
        help="Sufixos numéricos ou anos a combinar com cada palavra-base.",
    )
    parser.add_argument(
        "--sufixos",
        nargs="*",
        default=["!", "@123", "_admin"],
        help="Sufixos simbólicos curtos para combinar com as palavras-base.",
    )
    parser.add_argument(
        "--saida",
        type=Path,
        default=Path("wordlists/custom_wordlist.txt"),
        help="Caminho do arquivo de saída.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    combinacoes = gerar_variacoes(args.palavras, args.anos, args.sufixos)

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    args.saida.write_text("\n".join(combinacoes) + "\n", encoding="utf-8")
    print(f"[+] Geradas {len(combinacoes)} entradas em: {args.saida}")


if __name__ == "__main__":
    main()
