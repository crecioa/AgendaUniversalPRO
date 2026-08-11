"""
Agenda Universal PRO
Arquivo: core/agenda_updater.py

Responsável por coordenar a atualização da agenda.
"""

from __future__ import annotations

from pathlib import Path

from services.backup_service import BackupService
from services.logger_service import LoggerService
from services.text_updater import TextUpdater
from services.word_service import WordService


class AgendaUpdater:
    """Coordena o processo de atualização da agenda."""

    def __init__(self) -> None:
        self.logger = LoggerService.get_logger()
        self.word_service = WordService()
        self.backup_service = BackupService()
        self.text_updater = TextUpdater()

    def abrir_agenda(self, arquivo: str | Path):
        """
        Cria um backup, abre o documento Word e localiza as datas.

        Args:
            arquivo: Caminho do documento.

        Returns:
            Documento Word aberto.
        """

        caminho = Path(arquivo)

        self.logger.info("Iniciando processamento: %s", caminho.name)

        self.backup_service.criar_backup(caminho)

        documento = self.word_service.abrir_documento(caminho)

        self.logger.info("Documento carregado com sucesso.")

        ocorrencias = self.text_updater.localizar_datas(documento)

        self.logger.info(
            "Processamento concluído. %d parágrafo(s) com datas.",
            len(ocorrencias),
        )

        return documento