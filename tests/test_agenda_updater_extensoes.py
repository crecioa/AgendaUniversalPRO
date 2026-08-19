"""
Agenda Universal PRO
Arquivo: tests/test_agenda_updater_extensoes.py

Testes das validações de extensão e destino do AgendaUpdater.
"""

from pathlib import Path

from docx import Document

from core.agenda_updater import AgendaUpdater


ARQUIVO_TESTE = Path("modelos") / "teste_extensoes_agenda.docx"
DESTINO_TESTE = Path("modelos") / "teste_extensoes_agenda_atualizada.docx"


def criar_documento_teste() -> None:
    """Cria um documento Word utilizado pelos testes."""

    documento = Document()

    documento.add_paragraph("Agenda Universal PRO")
    documento.add_paragraph("Audiência em 05/01/2026.")

    documento.save(str(ARQUIVO_TESTE))


def testar_extensao_origem() -> None:
    """Verifica rejeição de arquivo de origem sem .docx."""

    updater = AgendaUpdater()

    arquivo = Path("modelos") / "documento.txt"

    arquivo.write_text(
        "arquivo de teste",
        encoding="utf-8",
    )

    try:
        updater.atualizar_ano(
            arquivo,
            2026,
            2027,
            DESTINO_TESTE,
        )
    except ValueError:
        print("✓ Extensão da origem rejeitada corretamente.")
    else:
        raise AssertionError(
            "Era esperado ValueError para extensão inválida."
        )
    finally:
        arquivo.unlink(missing_ok=True)


def testar_extensao_destino() -> None:
    """Verifica rejeição de destino sem .docx."""

    updater = AgendaUpdater()

    destino = Path("modelos") / "destino_invalido.txt"

    try:
        updater.atualizar_ano(
            ARQUIVO_TESTE,
            2026,
            2027,
            destino,
        )
    except ValueError:
        print("✓ Extensão do destino rejeitada corretamente.")
    else:
        raise AssertionError(
            "Era esperado ValueError para extensão inválida do destino."
        )


def testar_origem_diretorio() -> None:
    """Verifica rejeição de diretório como arquivo de origem."""

    updater = AgendaUpdater()

    diretorio = Path("modelos")

    try:
        updater.atualizar_ano(
            diretorio,
            2026,
            2027,
            DESTINO_TESTE,
        )
    except ValueError:
        print("✓ Diretório rejeitado como arquivo de origem.")
    else:
        raise AssertionError(
            "Era esperado ValueError para diretório de origem."
        )


def main() -> None:
    """Executa todos os testes."""

    print("\n=== TESTE DAS EXTENSÕES DO AGENDAUPDATER ===\n")

    ARQUIVO_TESTE.parent.mkdir(parents=True, exist_ok=True)

    criar_documento_teste()

    testar_extensao_origem()
    testar_extensao_destino()
    testar_origem_diretorio()

    print("\nTodos os testes de extensão foram concluídos com sucesso.")


if __name__ == "__main__":
    main()