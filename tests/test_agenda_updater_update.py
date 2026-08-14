"""
Agenda Universal PRO
Arquivo: tests/test_agenda_updater_update.py

Teste da atualização completa da agenda.
"""

from pathlib import Path

from core.agenda_updater import AgendaUpdater


def main() -> None:
    arquivo = Path("modelos") / "teste_text_updater.docx"
    destino = Path("modelos") / "teste_agenda_atualizada.docx"

    substituicoes = {
        "05/01/2027": "05/01/2028",
        "10/02/2027": "10/02/2028",
        "15/03/2027": "15/03/2028",
    }

    agenda_updater = AgendaUpdater()

    quantidade = agenda_updater.atualizar_agenda(
        arquivo,
        substituicoes,
        destino,
    )

    print("\n=== TESTE DE ATUALIZAÇÃO DA AGENDA ===\n")

    print(f"Arquivo original: {arquivo}")
    print(f"Arquivo atualizado: {destino}")
    print(f"Substituições realizadas: {quantidade}")

    print("\nTeste concluído com sucesso.")


if __name__ == "__main__":
    main()