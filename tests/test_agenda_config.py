"""
Agenda Universal PRO
Arquivo: tests/test_agenda_config.py

Testes da configuração de execução da agenda.
"""

from pathlib import Path

from config.agenda_config import AgendaConfig


def main() -> None:
    """Executa os testes da AgendaConfig."""

    print("\n=== TESTE DA AGENDACONFIG ===\n")

    origem = Path("modelos") / "agenda_2026.docx"
    destino = Path("output") / "agenda_2027.docx"

    configuracao = AgendaConfig(
        arquivo_origem=origem,
        arquivo_destino=destino,
        ano_origem=2026,
        ano_destino=2027,
    )

    assert configuracao.arquivo_origem == origem
    assert configuracao.arquivo_destino == destino

    assert configuracao.ano_origem == 2026
    assert configuracao.ano_destino == 2027

    assert (
        configuracao.nome_arquivo_origem
        == "agenda_2026.docx"
    )

    assert (
        configuracao.nome_arquivo_destino
        == "agenda_2027.docx"
    )

    print(
        "Arquivo de origem:",
        configuracao.arquivo_origem,
    )

    print(
        "Arquivo de destino:",
        configuracao.arquivo_destino,
    )

    print(
        "Ano de origem:",
        configuracao.ano_origem,
    )

    print(
        "Ano de destino:",
        configuracao.ano_destino,
    )

    print(
        "Nome da origem:",
        configuracao.nome_arquivo_origem,
    )

    print(
        "Nome do destino:",
        configuracao.nome_arquivo_destino,
    )

    print("\nConfiguração validada com sucesso.")
    print("Teste concluído com sucesso.")


if __name__ == "__main__":
    main()