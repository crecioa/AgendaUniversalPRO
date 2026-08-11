"""
Agenda Universal PRO
Arquivo: tests/test_agenda_updater.py

Teste da integração do AgendaUpdater com o TextUpdater.
"""

from pathlib import Path

from core.agenda_updater import AgendaUpdater


def main() -> None:
    arquivo = Path("modelos") / "teste_text_updater.docx"

    agenda_updater = AgendaUpdater()

    documento = agenda_updater.abrir_agenda(arquivo)

    print("\n=== TESTE DO AGENDA UPDATER ===\n")

    print(f"Documento aberto: {arquivo.name}")
    print(f"Parágrafos encontrados: {len(documento.paragraphs)}")

    print("\nTeste concluído com sucesso.")


if __name__ == "__main__":
    main()