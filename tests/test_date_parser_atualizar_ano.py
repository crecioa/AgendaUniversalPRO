"""
Agenda Universal PRO
Arquivo: tests/test_date_parser_atualizar_ano.py

Testes do método atualizar_ano do DateParser.
"""

from core.date_parser import DateParser


def main() -> None:
    print("\n=== TESTE DO DateParser.atualizar_ano ===\n")

    resultado = DateParser.atualizar_ano(
        "05/01/2026",
        2027,
    )

    assert resultado == "05/01/2027"

    print("05/01/2026 ->", resultado)

    resultado_invalido = DateParser.atualizar_ano(
        "29/02/2024",
        2025,
    )

    assert resultado_invalido is None

    print("29/02/2024 -> 2025:", resultado_invalido)

    print("\nTeste concluído com sucesso.")


if __name__ == "__main__":
    main()