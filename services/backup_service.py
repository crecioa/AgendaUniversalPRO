"""
Agenda Universal PRO
Arquivo: services/backup_service.py

Responsável por criar backups automáticos dos documentos.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil

from config.settings import BACKUP_DIR
from services.logger_service import LoggerService


class BackupService:
    """Serviço responsável pela criação de backups."""

    @staticmethod
    def criar_backup(arquivo: str | Path) -> Path:
        """
        Cria uma cópia do arquivo na pasta 'backup'.

        Args:
            arquivo: Caminho do arquivo original.

        Returns:
            Caminho completo do arquivo de backup.
        """

        logger = LoggerService.get_logger()

        arquivo = Path(arquivo)

        if not arquivo.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")

        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        destino = BACKUP_DIR / f"{arquivo.stem}_{timestamp}{arquivo.suffix}"

        shutil.copy2(arquivo, destino)

        logger.info(f"Backup criado: {destino.name}")

        return destino