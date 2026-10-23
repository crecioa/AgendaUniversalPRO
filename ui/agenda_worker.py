"""
Agenda Universal PRO
Arquivo: ui/agenda_worker.py

Worker responsável por atualizar documentos Word
em uma thread separada da interface gráfica.
"""

from __future__ import annotations

from PySide6.QtCore import QThread, Signal

from config.agenda_config import AgendaConfig
from services.agenda_application import AgendaApplication


class AgendaWorker(QThread):
    """Executa a atualização de agendas em segundo plano."""

    sucesso = Signal(int)
    erro = Signal(str)

    def __init__(self, config: AgendaConfig) -> None:
        super().__init__()
        self.config = config

    def run(self) -> None:
        """Executa o processamento fora da thread principal."""

        try:
            aplicacao = AgendaApplication()
            quantidade = aplicacao.atualizar(self.config)

        except Exception as exc:
            self.erro.emit(str(exc))
            return

        self.sucesso.emit(quantidade)