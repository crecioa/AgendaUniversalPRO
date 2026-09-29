from pathlib import Path

from docx import Document

from services.text_updater import TextUpdater


def test_atualizar_ano_preserva_data_e_atualiza_dia_da_semana(tmp_path: Path):
    origem = tmp_path / "agenda_2026.docx"
    destino = tmp_path / "agenda_2027.docx"

    documento = Document()

    documento.add_paragraph(
        "AUDIÊNCIAS – Quinta-feira, 01/01/2026"
    )
    documento.add_paragraph(
        "ACORDO – Quinta-feira, 01/01/2026"
    )

    documento.save(origem)

    documento = Document(origem)

    updater = TextUpdater()
    total = updater.atualizar_ano(documento, 2026, 2027)

    documento.save(destino)

    assert total == 2

    resultado = Document(destino)
    textos = [paragrafo.text for paragrafo in resultado.paragraphs]

    assert (
        "AUDIÊNCIAS – Sexta-feira, 01/01/2027"
        in textos
    )
    assert (
        "ACORDO – Sexta-feira, 01/01/2027"
        in textos
    )

    assert all("01/01/2026" not in texto for texto in textos)


def test_atualizar_ano_recalcula_dias_em_varias_datas(tmp_path: Path):
    origem = tmp_path / "agenda_varias_datas_2026.docx"
    destino = tmp_path / "agenda_varias_datas_2027.docx"

    documento = Document()

    documento.add_paragraph(
        "AUDIÊNCIAS – Segunda-feira, 05/01/2026"
    )
    documento.add_paragraph(
        "ACORDO – Terça-feira, 10/02/2026"
    )
    documento.add_paragraph(
        "AUDIÊNCIAS – Domingo, 15/03/2026"
    )

    documento.save(origem)

    documento = Document(origem)

    updater = TextUpdater()
    total = updater.atualizar_ano(documento, 2026, 2027)

    documento.save(destino)

    assert total == 3

    resultado = Document(destino)
    textos = [paragrafo.text for paragrafo in resultado.paragraphs]

    assert (
        "AUDIÊNCIAS – Terça-feira, 05/01/2027"
        in textos
    )
    assert (
        "ACORDO – Quarta-feira, 10/02/2027"
        in textos
    )
    assert (
        "AUDIÊNCIAS – Segunda-feira, 15/03/2027"
        in textos
    )