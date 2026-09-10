"""
Agenda Universal PRO
Arquivo: tests/test_agenda_updater_validacoes.py

Testes das validações do AgendaUpdater.
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
    documento.add_paragraph("Reunião em 10/02/2026.")

    documento.save(str(arquivo))


def testar_arquivo_inexistente(
    tmp_path: Path,
) -> None:
    """Verifica rejeição de arquivo inexistente."""

    updater = AgendaUpdater()

    arquivo = tmp_path / "arquivo_que_nao_existe.docx"
    destino = tmp_path / "destino.docx"

    try:
        updater.atualizar_ano(
            arquivo,
            2026,
            2027,
            destino,
        )
    except FileNotFoundError:
        print("✓ Arquivo inexistente rejeitado corretamente.")
    else:
        raise AssertionError(
            "Era esperado FileNotFoundError para arquivo inexistente."
        )


def testar_destino_igual_origem(
    tmp_path: Path,
) -> None:
    """Verifica proteção contra sobrescrita do original."""

    arquivo_origem = tmp_path / "teste_validacoes_agenda.docx"
    criar_documento_teste(arquivo_origem)

    updater = AgendaUpdater()

    try:
        updater.atualizar_ano(
            arquivo_origem,
            2026,
            2027,
            arquivo_origem,
        )
    except ValueError:
        print("✓ Sobrescrita do arquivo original bloqueada.")
    else:
        raise AssertionError(
            "Era esperado ValueError para destino igual à origem."
        )


def testar_anos_iguais(
    tmp_path: Path,
) -> None:
    """Verifica rejeição de anos iguais."""

    arquivo_origem = tmp_path / "teste_validacoes_agenda.docx"
    criar_documento_teste(arquivo_origem)

    destino = tmp_path / "destino.docx"

    updater = AgendaUpdater()

    try:
        updater.atualizar_ano(
            arquivo_origem,
            2026,
            2026,
            destino,
        )
    except ValueError:
        print("✓ Anos iguais rejeitados corretamente.")
    else:
        raise AssertionError(
            "Era esperado ValueError para anos iguais."
        )


def testar_ano_invalido(
    tmp_path: Path,
) -> None:
    """Verifica rejeição de ano fora do intervalo válido."""

    arquivo_origem = tmp_path / "teste_validacoes_agenda.docx"
    criar_documento_teste(arquivo_origem)

    destino = tmp_path / "destino.docx"

    updater = AgendaUpdater()

    try:
        updater.atualizar_ano(
            arquivo_origem,
            0,
            2027,
            destino,
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

    print(
        "Os testes são executados pelo pytest "
        "utilizando diretórios temporários."
    )


if __name__ == "__main__":
    main()