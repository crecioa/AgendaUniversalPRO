"""
Agenda Universal PRO
Arquivo: services/word_service.py

Serviço responsável pela manipulação de documentos Word (.docx).
"""

from __future__ import annotations

from pathlib import Path

from docx import Document

from services.logger_service import LoggerService


class WordService:
    """Serviço para abrir e salvar documentos do Word."""

    def __init__(self) -> None:
        self.logger = LoggerService.get_logger()

    def abrir_documento(self, arquivo: str | Path) -> Document:
        """
        Abre um documento do Word.

        Args:
            arquivo: Caminho do arquivo .docx.

        Returns:
            Objeto Document.
        """

        arquivo = Path(arquivo)

        if not arquivo.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")

        self.logger.info(f"Abrindo documento: {arquivo.name}")

        return Document(arquivo)

    def salvar_documento(self, documento: Document, destino: str | Path) -> None:
        """
        Salva o documento.

        Args:
            documento: Documento aberto.
            destino: Caminho onde será salvo.
        """

        destino = Path(destino)

        documento.save(destino)

        self.logger.info(f"Documento salvo: {destino.name}")

    @staticmethod
    def contar_paragrafos(documento: Document) -> int:
        """Retorna a quantidade de parágrafos do documento."""

        return len(documento.paragraphs)

    @staticmethod
    def contar_tabelas(documento: Document) -> int:
        """Retorna a quantidade de tabelas do documento."""

        return len(documento.tables)