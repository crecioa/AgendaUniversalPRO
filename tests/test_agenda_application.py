"""
Agenda Universal PRO
Arquivo: tests/test_agenda_application.py

Teste de integração da camada AgendaApplication.
"""

from pathlib import Path

from docx import Document

from services.agenda_application import AgendaApplication


def criar_documento_teste(arquivo: Path) -> None:
    """Cria um documento Word para o teste."""

    documento = Document()

    documento.add_paragraph(
        "Audiência em 05/01/2026."
    )

    documento.add_paragraph(
        "Reunião em 10/02/2026."
    )

    documento.add_paragraph(
        "Prazo em 15/03/2027."
    )

    documento.add_paragraph(
        "Texto sem data."
    )

    tabela = documento.add_table(
        rows=2,
        cols=2,
    )

    tabela.cell(0, 0).text = "Data"
    tabela.cell(0, 1).text = "Evento"
    tabela.cell(1, 0).text = "20/04/2026"
    tabela.cell(1, 1).text = "Sessão"

    documento.save(str(arquivo))


def validar_documento(arquivo: Path) -> None:
    """Valida o conteúdo do documento atualizado."""

    documento = Document(str(arquivo))

    assert (
        documento.paragraphs[0].text
        == "Audiência em 05/01/2027."
    )

    assert (
        documento.paragraphs[1].text
        == "Reunião em 10/02/2027."
    )

    assert (
        documento.paragraphs[2].text
        == "Prazo em 15/03/2027."
    )

    assert (
        documento.paragraphs[3].text
        == "Texto sem data."
    )

    assert len(documento.tables) == 1

    tabela = documento.tables[0]

    assert tabela.cell(0, 0).text == "Data"
    assert tabela.cell(0, 1).text == "Evento"
    assert tabela.cell(1, 0).text == "20/04/2027"
    assert tabela.cell(1, 1).text == "Sessão"


def main() -> None:
    """Executa o teste da AgendaApplication."""

    print(
        "\n=== TESTE DA AGENDAAPPLICATION ===\n"
    )

    pasta_modelos = Path("modelos")

    pasta_modelos.mkdir(
        parents=True,
        exist_ok=True,
    )

    arquivo_origem = (
        pasta_modelos
        / "teste_agenda_application.docx"
    )

    arquivo_destino = (
        pasta_modelos
        / "teste_agenda_application_atualizada.docx"
    )

    criar_documento_teste(
        arquivo_origem
    )

    aplicacao = AgendaApplication()

    quantidade = aplicacao.atualizar_ano(
        arquivo=arquivo_origem,
        ano_origem=2026,
        ano_destino=2027,
        destino=arquivo_destino,
    )

    print(
        f"Substituições realizadas: {quantidade}"
    )

    assert quantidade == 3

    assert arquivo_destino.exists()

    validar_documento(
        arquivo_destino
    )

    print(
        "Parágrafos atualizados corretamente."
    )

    print(
        "Tabela atualizada corretamente."
    )

    print(
        "Documento validado com sucesso."
    )

    print(
        "\nTeste concluído com sucesso."
    )


if __name__ == "__main__":
    main()
