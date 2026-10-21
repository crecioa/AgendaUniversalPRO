"""Histórico append-only dos processamentos do Agenda Universal PRO."""

from __future__ import annotations

import csv
import json
import os
from datetime import date, datetime, time, timezone
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

    @staticmethod
    def _normalizar_limite(valor: date | datetime | None, *, fim: bool) -> datetime | None:
        """Converte datas e instantes para UTC; datas incluem o dia inteiro."""
        if valor is None:
            return None
        if isinstance(valor, datetime):
            if valor.tzinfo is None or valor.utcoffset() is None:
                raise ValueError("O horário do filtro deve possuir fuso horário.")
            return valor.astimezone(timezone.utc)
        if isinstance(valor, date):
            horario = time.max if fim else time.min
            return datetime.combine(valor, horario, tzinfo=timezone.utc)
        raise TypeError("O filtro de período deve ser date ou datetime.")

    def consultar(
        self,
        *,
        inicio: date | datetime | None = None,
        fim: date | datetime | None = None,
        status: str | None = None,
        operacao: str | None = None,
    ) -> list[dict[str, object]]:
        """Consulta em ordem original, com limites inclusivos em UTC."""
        de = self._normalizar_limite(inicio, fim=False)
        ate = self._normalizar_limite(fim, fim=True)
        if de is not None and ate is not None and de > ate:
            raise ValueError("O início do período não pode ser posterior ao fim.")
        if status is not None and status not in {"sucesso", "falha"}:
            raise ValueError("Status de filtro inválido.")
        if operacao is not None and not operacao:
            raise ValueError("A operação não pode ser vazia.")
        if not self.caminho.exists():
            return []
        resultado: list[dict[str, object]] = []
        with self.caminho.open("r", encoding="utf-8") as arquivo:
            for numero, linha in enumerate(arquivo, start=1):
                if not linha.strip():
                    continue
                try:
                    registro = json.loads(linha)
                    if not isinstance(registro, dict):
                        raise ValueError("Registro não é um objeto JSON.")
                    if status is not None and registro.get("status") != status:
                        continue
                    if operacao is not None and registro.get("operacao") != operacao:
                        continue
                    if de is not None or ate is not None:
                        instante = registro.get("data_hora_utc")
                        if not isinstance(instante, str):
                            raise ValueError("Data/hora ausente ou inválida.")
                        quando = datetime.fromisoformat(instante.replace("Z", "+00:00"))
                        if quando.tzinfo is None or quando.utcoffset() is None:
                            raise ValueError("Data/hora sem fuso horário.")
                        quando = quando.astimezone(timezone.utc)
                        if de is not None and quando < de:
                            continue
                        if ate is not None and quando > ate:
                            continue
                except (ValueError, TypeError, json.JSONDecodeError) as erro:
                    raise ValueError(
                        f"Registro inválido no histórico, linha {numero}."
                    ) from erro
                resultado.append(registro)
        return resultado

    def exportar_csv(
        self,
        destino: str | Path,
        *,
        inicio: date | datetime | None = None,
        fim: date | datetime | None = None,
        status: str | None = None,
        operacao: str | None = None,
    ) -> Path:
        """Exporta os registros filtrados sem alterar o JSONL ou sobrescrever CSV."""
        caminho = Path(destino)
        if caminho.suffix.lower() != ".csv":
            raise ValueError("A exportação deve possuir extensão .csv.")
        registros = self.consultar(inicio=inicio, fim=fim, status=status, operacao=operacao)
        colunas = (
            "data_hora_utc", "operacao", "origem", "destino", "status",
            "previstas", "atualizadas", "erro", "relatorio",
        )
        # 'x' garante criação exclusiva. newline evita linhas em branco no Windows.
        with caminho.open("x", encoding="utf-8-sig", newline="") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=colunas, extrasaction="ignore")
            escritor.writeheader()
            for registro in registros:
                escritor.writerow(registro)
        return caminho


    def resumir(
        self,
        *,
        inicio: date | datetime | None = None,
        fim: date | datetime | None = None,
        status: str | None = None,
        operacao: str | None = None,
    ) -> dict[str, object]:
        """Resume os eventos filtrados sem modificar o histórico original.

        A taxa de sucesso considera todos os eventos consultados.
        O total de datas atualizadas considera apenas atualizações de
        documentos bem-sucedidas, não exportações de relatórios.
        """
        registros = self.consultar(
            inicio=inicio, fim=fim, status=status, operacao=operacao
        )
        return self._resumir_registros(registros)

    @staticmethod
    def _resumir_registros(registros: list[dict[str, object]]) -> dict[str, object]:
        """Calcula os indicadores de uma única coleção de eventos."""
        por_operacao: dict[str, int] = {}
        sucessos = 0
        falhas = 0
        datas_atualizadas = 0
        atualizacoes_documentos = 0

        for registro in registros:
            tipo = registro.get("operacao")
            if not isinstance(tipo, str):
                raise ValueError("Operação inválida no registro do histórico.")
            por_operacao[tipo] = por_operacao.get(tipo, 0) + 1

            situacao = registro.get("status")
            if situacao == "sucesso":
                sucessos += 1
            elif situacao == "falha":
                falhas += 1
            else:
                raise ValueError("Status inválido no registro do histórico.")

            if situacao == "sucesso" and tipo in {"ano", "substituicoes"}:
                atualizacoes_documentos += 1
                quantidade = registro.get("atualizadas")
                if quantidade is not None:
                    if type(quantidade) is not int or quantidade < 0:
                        raise ValueError("Quantidade atualizada inválida no histórico.")
                    datas_atualizadas += quantidade

        total = len(registros)
        return {
            "total_operacoes": total,
            "sucessos": sucessos,
            "falhas": falhas,
            "taxa_sucesso_percentual": round(sucessos * 100 / total, 2) if total else 0.0,
            "atualizacoes_documentos": atualizacoes_documentos,
            "datas_atualizadas": datas_atualizadas,
            "por_operacao": por_operacao,
        }

    def exportar_resumo_json(
        self,
        destino: str | Path,
        *,
        inicio: date | datetime | None = None,
        fim: date | datetime | None = None,
        status: str | None = None,
        operacao: str | None = None,
    ) -> Path:
        """Exporta as estatísticas para JSON sem sobrescrever arquivos existentes."""
        caminho = Path(destino)
        if caminho.suffix.lower() != ".json":
            raise ValueError("A exportação do resumo deve possuir extensão .json.")
        resumo = self.resumir(inicio=inicio, fim=fim, status=status, operacao=operacao)
        with caminho.open("x", encoding="utf-8") as arquivo:
            json.dump(resumo, arquivo, ensure_ascii=False, indent=2)
            arquivo.write("\n")
        return caminho

    def exportar_resumo_csv(
        self,
        destino: str | Path,
        *,
        inicio: date | datetime | None = None,
        fim: date | datetime | None = None,
        status: str | None = None,
        operacao: str | None = None,
    ) -> Path:
        """Exporta as estatísticas em linhas indicador/valor, incluindo operações."""
        caminho = Path(destino)
        if caminho.suffix.lower() != ".csv":
            raise ValueError("A exportação do resumo deve possuir extensão .csv.")
        resumo = self.resumir(inicio=inicio, fim=fim, status=status, operacao=operacao)
        indicadores = (
            "total_operacoes", "sucessos", "falhas", "taxa_sucesso_percentual",
            "atualizacoes_documentos", "datas_atualizadas",
        )
        distribuicao = resumo["por_operacao"]
        if not isinstance(distribuicao, dict):
            raise ValueError("Distribuição de operações inválida no resumo.")
        with caminho.open("x", encoding="utf-8-sig", newline="") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(("indicador", "valor"))
            for indicador in indicadores:
                escritor.writerow((indicador, resumo[indicador]))
            for tipo, quantidade in sorted(distribuicao.items()):
                escritor.writerow((f"por_operacao:{tipo}", quantidade))
        return caminho

    def exportar_relatorio_consolidado(
        self,
        destino: str | Path,
        *,
        inicio: date | datetime | None = None,
        fim: date | datetime | None = None,
        status: str | None = None,
        operacao: str | None = None,
    ) -> Path:
        """Exporta histórico, indicadores e auditoria em JSON, sem sobrescrever.

        Os dados e as estatísticas são derivados da mesma consulta, para que
        o relatório represente um conjunto coerente de eventos filtrados.
        """
        caminho = Path(destino)
        if caminho.suffix.lower() != ".json":
            raise ValueError("O relatório consolidado deve possuir extensão .json.")

        registros = self.consultar(
            inicio=inicio, fim=fim, status=status, operacao=operacao
        )
        # Reaproveita a lógica estatística sem consultar o arquivo uma segunda vez.
        resumo = self._resumir_registros(registros)
        filtros: dict[str, str | None] = {
            "inicio": inicio.isoformat() if inicio is not None else None,
            "fim": fim.isoformat() if fim is not None else None,
            "status": status,
            "operacao": operacao,
        }
        relatorio: dict[str, object] = {
            "versao_relatorio": 1,
            "gerado_em_utc": datetime.now(timezone.utc).isoformat(),
            "auditoria": {
                "arquivo_historico": str(self.caminho),
                "quantidade_registros": len(registros),
                "filtros": filtros,
            },
            "resumo": resumo,
            "registros": registros,
        }
        # 'x' garante criação exclusiva mesmo em chamadas simultâneas.
        with caminho.open("x", encoding="utf-8") as arquivo:
            json.dump(relatorio, arquivo, ensure_ascii=False, indent=2)
            arquivo.write("\n")
        return caminho
