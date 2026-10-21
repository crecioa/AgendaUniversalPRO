"""Histórico append-only dos processamentos do Agenda Universal PRO."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from config.settings import LOGS_DIR


class ProcessingHistoryService:
    """Registra eventos em JSONL sem reescrever eventos anteriores."""

    def __init__(self, caminho: str | Path | None = None) -> None:
        self.caminho = Path(caminho) if caminho is not None else (
            LOGS_DIR / "historico_processamentos.jsonl"
        )

    def registrar(
        self,
        *,
        operacao: str,
        origem: str | Path,
        destino: str | Path,
        status: str,
        atualizadas: int | None = None,
        previstas: int | None = None,
        erro: str | None = None,
        relatorio: str | Path | None = None,
    ) -> dict[str, object]:
        """Acrescenta um evento; não trunca nem sobrescreve o histórico."""
        if status not in {"sucesso", "falha"}:
            raise ValueError("Status de histórico inválido.")
        registro: dict[str, object] = {
            "data_hora_utc": datetime.now(timezone.utc).isoformat(),
            "operacao": operacao,
            "origem": str(origem),
            "destino": str(destino),
            "status": status,
            "previstas": previstas,
            "atualizadas": atualizadas,
            "erro": erro,
            "relatorio": str(relatorio) if relatorio is not None else None,
        }
        conteudo = (json.dumps(registro, ensure_ascii=False) + "\n").encode("utf-8")
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        descritor = os.open(
            self.caminho,
            os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, "O_BINARY", 0),
            0o600,
        )
        try:
            escritos = os.write(descritor, conteudo)
            if escritos != len(conteudo):
                raise OSError("Gravação incompleta do histórico.")
        finally:
            os.close(descritor)
        return registro

    def consultar(self) -> list[dict[str, object]]:
        """Lê os registros existentes em ordem de gravação."""
        if not self.caminho.exists():
            return []
        with self.caminho.open("r", encoding="utf-8") as arquivo:
            return [json.loads(linha) for linha in arquivo if linha.strip()]
