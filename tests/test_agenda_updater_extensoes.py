"""
Agenda Universal PRO
Arquivo: tests/test_agenda_updater_extensoes.py

Testes das validações de extensão e destino do AgendaUpdater.
"""

from pathlib import Path

from docx import Document

from core.agenda_updater import AgendaUpdater


def criar_documento_teste(
    arquivo: Path,
) -> None:
    """Cria um documento Word utilizado pelos testes."""

    arquivo.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    documento = Document()

    documento.add_paragraph("Agenda Universal PRO")
    documento.add_paragraph("Audiência em 05/01/2026.")

    documento.save(str(arquivo))


def testar_extensao_origem(
    tmp_path: Path,
) -> None:
    """Verifica rejeição de arquivo de origem sem .docx."""

    updater = AgendaUpdater()

    arquivo = tmp_path / "documento.txt"
    destino = tmp_path / "destino.docx"

    arquivo.write_text(
        "arquivo de teste",
        encoding="utf-8",
    )

    try:
        updater.atualizar_ano(
            arquivo,
            2026,
            2027,
            destino,
        )
    except ValueError:
        print("✓ Extensão da origem rejeitada corretamente.")
    else:
        raise AssertionError(
            "Era esperado ValueError para extensão inválida."
        )
    finally:
        arquivo.unlink(missing_ok=True)


def testar_extensao_destino(
    tmp_path: Path,
) -> None:
    """Verifica rejeição de destino sem .docx."""

    arquivo_origem = tmp_path / "teste_extensoes_agenda.docx"
    criar_documento_teste(arquivo_origem)

    updater = AgendaUpdater()

    destino = tmp_path / "destino_invalido.txt"

    try:
        updater.atualizar_ano(
            arquivo_origem,
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


def testar_origem_diretorio(
    tmp_path: Path,
) -> None:
    """Verifica rejeição de diretório como arquivo de origem."""

    updater = AgendaUpdater()

    diretorio = tmp_path / "modelos"
    diretorio.mkdir()

    destino = tmp_path / "destino.docx"

    try:
        updater.atualizar_ano(
            diretorio,
            2026,
            2027,
            destino,
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

    print(
        "Os testes são executados pelo pytest "
        "utilizando diretórios temporários."
    )


if __name__ == "__main__":
    main()