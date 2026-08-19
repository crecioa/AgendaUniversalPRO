"""
Agenda Universal PRO
Arquivo: tests/test_agenda_updater_validacoes.py

Testes das validações do AgendaUpdater.
"""

from pathlib import Path

from docx import Document

from core.agenda_updater import AgendaUpdater


ARQUIVO_TESTE = Path("modelos") / "teste_validacoes_agenda.docx"
DESTINO_TESTE = Path("modelos") / "teste_validacoes_agenda_atualizada.docx"


def criar_documento_teste() -> None:
    """Cria um documento Word utilizado pelos testes."""

    documento = Document()

    documento.add_paragraph("Agenda Universal PRO")
    documento.add_paragraph("Audiência em 05/01/2026.")
    documento.add_paragraph("Reunião em 10/02/2026.")

    documento.save(str(ARQUIVO_TESTE))


def testar_arquivo_inexistente() -> None:
    """Verifica rejeição de arquivo inexistente."""

    updater = AgendaUpdater()

    arquivo = Path("modelos") / "arquivo_que_nao_existe.docx"

    try:
        updater.atualizar_ano(
            arquivo,
            2026,
            2027,
            DESTINO_TESTE,
        )
    except FileNotFoundError:
        print("✓ Arquivo inexistente rejeitado corretamente.")
    else:
        raise AssertionError(
            "Era esperado FileNotFoundError para arquivo inexistente."
        )


def testar_destino_igual_origem() -> None:
    """Verifica proteção contra sobrescrita do original."""

    updater = AgendaUpdater()

    try:
        updater.atualizar_ano(
            ARQUIVO_TESTE,
            2026,
            2027,
            ARQUIVO_TESTE,
        )
    except ValueError:
        print("✓ Sobrescrita do arquivo original bloqueada.")
    else:
        raise AssertionError(
            "Era esperado ValueError para destino igual à origem."
        )


def testar_anos_iguais() -> None:
    """Verifica rejeição de anos iguais."""

    updater = AgendaUpdater()

    try:
        updater.atualizar_ano(
            ARQUIVO_TESTE,
            2026,
            2026,
            DESTINO_TESTE,
        )
    except ValueError:
        print("✓ Anos iguais rejeitados corretamente.")
    else:
        raise AssertionError(
            "Era esperado ValueError para anos iguais."
        )


def testar_ano_invalido() -> None:
    """Verifica rejeição de ano fora do intervalo válido."""

    updater = AgendaUpdater()

    try:
        updater.atualizar_ano(
            ARQUIVO_TESTE,
            0,
            2027,
            DESTINO_TESTE,
        )
    except ValueError:
        print("✓ Ano inválido rejeitado corretamente.")
    else:
        raise AssertionError(
            "Era esperado ValueError para ano inválido."
        )


def main() -> None:
    """Executa todos os testes."""

    print("\n=== TESTE DAS VALIDAÇÕES DO AGENDAUPDATER ===\n")

    ARQUIVO_TESTE.parent.mkdir(parents=True, exist_ok=True)

    criar_documento_teste()

    testar_arquivo_inexistente()
    testar_destino_igual_origem()
    testar_anos_iguais()
    testar_ano_invalido()

    print("\nTodos os testes de validação foram concluídos com sucesso.")


if __name__ == "__main__":
    main()