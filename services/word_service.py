
"""
Agenda Universal PRO
Arquivo: services/word_service.py

Serviço responsável pela manipulação de documentos Word (.docx).
"""

from __future__ import annotations

import os
import tempfile
from io import BytesIO
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from docx import Document
from docx.document import Document as DocxDocument
from docx.opc.exceptions import PackageNotFoundError

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
        """Salva em arquivo temporário e publica sem sobrescrever destino."""
        caminho = Path(destino)

        if caminho.exists():
            raise FileExistsError(f"O arquivo de destino já existe: {caminho}")

        descritor, nome_temporario = tempfile.mkstemp(
            prefix=f".{caminho.stem}.",
            suffix=".docx",
            dir=str(caminho.parent),
        )
        os.close(descritor)
        temporario = Path(nome_temporario)

        try:
            documento.save(str(temporario))
            self._validar_documento_temporario(temporario)
            # Um hard link cria o destino somente se ele ainda não existir.
            # Diferentemente de os.replace(), não sobrescreve arquivos.
            os.link(temporario, caminho)
        finally:
            temporario.unlink(missing_ok=True)

        self.logger.info("Documento salvo: %s", caminho.name)

    @staticmethod
    def _validar_documento_temporario(caminho: Path) -> None:
        """Confere o pacote ZIP e a abertura do Word antes da publicação."""
        try:
            conteudo = caminho.read_bytes()
            with ZipFile(BytesIO(conteudo)) as pacote:
                if pacote.testzip() is not None:
                    raise ValueError("Documento Word gerado está corrompido.")
                partes = set(pacote.namelist())
                obrigatorias = {
                    "[Content_Types].xml",
                    "_rels/.rels",
                    "word/document.xml",
                }
                if not obrigatorias.issubset(partes):
                    raise ValueError("Estrutura DOCX obrigatória ausente.")

            # A leitura em memória evita bloqueios do temporário no Windows,
            # inclusive quando python-docx rejeita um pacote malformado.
            Document(BytesIO(conteudo))
        except (BadZipFile, KeyError, ValueError, PackageNotFoundError) as erro:
            raise ValueError(
                "Documento Word gerado é inválido ou está corrompido."
            ) from erro

    @staticmethod
    def contar_paragrafos(documento: DocxDocument) -> int:
        """Retorna a quantidade de parágrafos."""
        return len(documento.paragraphs)

    @staticmethod
    def contar_tabelas(documento: DocxDocument) -> int:
        """Retorna a quantidade de tabelas."""
        return len(documento.tables)
