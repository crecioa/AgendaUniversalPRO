"""
Agenda Universal PRO
Arquivo: tests/test_word_service.py

Testes do serviço responsável pela manipulação de documentos Word.

Sprint 4.11:
- Testa abertura de documentos.
- Testa abertura com arquivo inexistente.
- Testa salvamento de documentos.
- Testa contagem de parágrafos.
- Testa contagem de tabelas.
- Testa registro das operações no logger.
"""

from pathlib import Path
from typing import Any

from docx import Document

from services.word_service import WordService


def test_abrir_documento(tmp_path: Path) -> None:
    """Testa a abertura de um documento Word."""

    arquivo = tmp_path / "agenda.docx"

    documento = Document()
    documento.add_paragraph("Agenda Universal PRO")
    documento.save(str(arquivo))

    service = WordService()

    resultado = service.abrir_documento(arquivo)

    assert resultado is not None
    assert len(resultado.paragraphs) == 1
    assert resultado.paragraphs[0].text == "Agenda Universal PRO"


def test_abrir_documento_com_string(tmp_path: Path) -> None:
    """Testa a abertura utilizando caminho em formato string."""

    arquivo = tmp_path / "agenda.docx"

    documento = Document()
    documento.add_paragraph("Documento de teste")
    documento.save(str(arquivo))

    service = WordService()

    resultado = service.abrir_documento(str(arquivo))

    assert resultado is not None
    assert resultado.paragraphs[0].text == "Documento de teste"


def test_abrir_documento_inexistente(tmp_path: Path) -> None:
    """Testa erro ao tentar abrir arquivo inexistente."""

    arquivo = tmp_path / "nao_existe.docx"

    service = WordService()

    try:
        service.abrir_documento(arquivo)
        assert False, "Era esperada uma exceção FileNotFoundError."
    except FileNotFoundError as erro:
        assert "Arquivo não encontrado" in str(erro)


def test_salvar_documento(tmp_path: Path) -> None:
    """Testa o salvamento de um documento Word."""

    destino = tmp_path / "agenda_salva.docx"

    documento = Document()
    documento.add_paragraph("Documento salvo com sucesso.")

    service = WordService()

    service.salvar_documento(documento, destino)

    assert destino.exists()

    documento_salvo = Document(str(destino))

    assert len(documento_salvo.paragraphs) == 1
    assert (
        documento_salvo.paragraphs[0].text
        == "Documento salvo com sucesso."
    )


def test_salvar_documento_com_string(tmp_path: Path) -> None:
    """Testa o salvamento utilizando caminho em formato string."""

    destino = tmp_path / "agenda_string.docx"

    documento = Document()
    documento.add_paragraph("Salvamento com string.")

    service = WordService()

    service.salvar_documento(documento, str(destino))

    assert destino.exists()

    documento_salvo = Document(str(destino))

    assert (
        documento_salvo.paragraphs[0].text
        == "Salvamento com string."
    )


def test_contar_paragrafos() -> None:
    """Testa a contagem de parágrafos."""

    documento = Document()

    documento.add_paragraph("Primeiro parágrafo.")
    documento.add_paragraph("Segundo parágrafo.")
    documento.add_paragraph("Terceiro parágrafo.")

    resultado = WordService.contar_paragrafos(documento)

    assert resultado == 3


def test_contar_tabelas() -> None:
    """Testa a contagem de tabelas."""

    documento = Document()

    documento.add_table(rows=2, cols=2)
    documento.add_table(rows=3, cols=3)

    resultado = WordService.contar_tabelas(documento)

    assert resultado == 2


def test_contar_paragrafos_documento_vazio() -> None:
    """Testa a contagem de parágrafos em documento vazio."""

    documento = Document()

    resultado = WordService.contar_paragrafos(documento)

    assert resultado == 0


def test_contar_tabelas_documento_sem_tabelas() -> None:
    """Testa a contagem quando não existem tabelas."""

    documento = Document()

    resultado = WordService.contar_tabelas(documento)

    assert resultado == 0


def test_abrir_documento_registra_log(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Testa o registro de log ao abrir um documento."""

    arquivo = tmp_path / "agenda.log.docx"

    documento = Document()
    documento.add_paragraph("Teste de log.")
    documento.save(str(arquivo))

    mensagens: list[str] = []

    class LoggerFalso:
        def info(
            self,
            mensagem: str,
            *args: object,
        ) -> None:
            mensagens.append(
                mensagem % args if args else mensagem
            )

    monkeypatch.setattr(
        "services.word_service.LoggerService.get_logger",
        lambda: LoggerFalso(),
    )

    service = WordService()
    service.abrir_documento(arquivo)

    assert any(
        "Abrindo documento: agenda.log.docx" in mensagem
        for mensagem in mensagens
    )


def test_salvar_documento_registra_log(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Testa o registro de log ao salvar um documento."""

    destino = tmp_path / "salvo.log.docx"

    documento = Document()
    documento.add_paragraph("Teste de salvamento.")

    mensagens: list[str] = []

    class LoggerFalso:
        def info(
            self,
            mensagem: str,
            *args: object,
        ) -> None:
            mensagens.append(
                mensagem % args if args else mensagem
            )

    monkeypatch.setattr(
        "services.word_service.LoggerService.get_logger",
        lambda: LoggerFalso(),
    )

    service = WordService()
    service.salvar_documento(documento, destino)

    assert destino.exists()

    assert any(
        "Documento salvo: salvo.log.docx" in mensagem
        for mensagem in mensagens
    )