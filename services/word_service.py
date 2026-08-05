"""
Agenda Universal PRO
Arquivo: services/word_service.py

Serviço responsável pela manipulação de documentos Word (.docx).
"""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.document import Document as DocxDocument

from services.logger_service import LoggerService


class WordService:
    """Serviço para abrir e salvar documentos Word."""

    def __init__(self) -> None:
        self.logger = LoggerService.get_logger()

    def abrir_documento(self, arquivo: str | Path) -> DocxDocument:
        """Abre um documento Word."""

        caminho = Path(arquivo)

        if not caminho.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

        self.logger.info("Abrindo documento: %s", caminho.name)

        return Document(str(caminho))

    def salvar_documento(
        self,
        documento: DocxDocument,
        destino: str | Path,
    ) -> None:
        """Salva o documento."""

        caminho = Path(destino)

        documento.save(str(caminho))

        self.logger.info("Documento salvo: %s", caminho.name)

    @staticmethod
    def contar_paragrafos(documento: DocxDocument) -> int:
        """Retorna a quantidade de parágrafos."""

        return len(documento.paragraphs)

    @staticmethod
    def contar_tabelas(documento: DocxDocument) -> int:
        """Retorna a quantidade de tabelas."""

        return len(documento.tables)