"""Testes do relatório consolidado de auditoria (Sprint 5.18)."""

import json
from datetime import date, datetime, timezone
from pathlib import Path

import pytest

from services.processing_history import ProcessingHistoryService


def _servico(tmp_path: Path) -> ProcessingHistoryService:
    servico = ProcessingHistoryService(tmp_path / "histórico.jsonl")
    servico.registrar(
        operacao="ano", origem="Audiência.docx", destino="saída.docx",
        status="sucesso", atualizadas=3,
    )
    servico.registrar(
        operacao="substituicoes", origem="entrada.docx", destino="saída.docx",
        status="falha", erro="Data inválida",
    )
    servico.registrar(
        operacao="exportacao_relatorio", origem="entrada.docx",
        destino="relatório.json", status="sucesso",
    )
    return servico


def test_relatorio_contem_todas_as_secoes(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / "consolidado.json"
    assert servico.exportar_relatorio_consolidado(destino) == destino
    dados = json.loads(destino.read_text(encoding="utf-8"))
    assert dados["versao_relatorio"] == 1
    assert dados["resumo"] == servico.resumir()
    assert dados["registros"] == servico.consultar()
    assert dados["auditoria"]["quantidade_registros"] == 3
    assert dados["auditoria"]["arquivo_historico"] == str(servico.caminho)


def test_auditoria_tem_instante_utc(tmp_path: Path) -> None:
    destino = tmp_path / "consolidado.json"
    _servico(tmp_path).exportar_relatorio_consolidado(destino)
    dados = json.loads(destino.read_text(encoding="utf-8"))
    instante = datetime.fromisoformat(dados["gerado_em_utc"])
    assert instante.tzinfo is not None
    assert instante.utcoffset() == timezone.utc.utcoffset(instante)


def test_estatisticas_nao_contam_exportacao_como_atualizacao(tmp_path: Path) -> None:
    destino = tmp_path / "consolidado.json"
    _servico(tmp_path).exportar_relatorio_consolidado(destino)
    resumo = json.loads(destino.read_text(encoding="utf-8"))["resumo"]
    assert resumo["total_operacoes"] == 3
    assert resumo["sucessos"] == 2
    assert resumo["falhas"] == 1
    assert resumo["atualizacoes_documentos"] == 1
    assert resumo["datas_atualizadas"] == 3


def test_filtros_combinados(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / "filtrado.json"
    servico.exportar_relatorio_consolidado(destino, status="sucesso", operacao="ano")
    dados = json.loads(destino.read_text(encoding="utf-8"))
    assert dados["auditoria"]["filtros"]["status"] == "sucesso"
    assert dados["auditoria"]["filtros"]["operacao"] == "ano"
    assert dados["auditoria"]["quantidade_registros"] == 1
    assert dados["resumo"]["total_operacoes"] == 1
    assert len(dados["registros"]) == 1


def test_filtro_periodo_sem_registros(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / "periodo.json"
    servico.exportar_relatorio_consolidado(
        destino, inicio=date(2000, 1, 1), fim=date(2000, 1, 2)
    )
    dados = json.loads(destino.read_text(encoding="utf-8"))
    assert dados["auditoria"]["filtros"]["inicio"] == "2000-01-01"
    assert dados["auditoria"]["filtros"]["fim"] == "2000-01-02"
    assert dados["resumo"]["total_operacoes"] == 0
    assert dados["registros"] == []


def test_historico_inexistente(tmp_path: Path) -> None:
    servico = ProcessingHistoryService(tmp_path / "ausente.jsonl")
    destino = tmp_path / "vazio.json"
    servico.exportar_relatorio_consolidado(destino)
    dados = json.loads(destino.read_text(encoding="utf-8"))
    assert dados["auditoria"]["quantidade_registros"] == 0
    assert dados["resumo"] == servico.resumir()
    assert dados["registros"] == []
    assert not servico.caminho.exists()


def test_preserva_historico_original(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    original = servico.caminho.read_bytes()
    servico.exportar_relatorio_consolidado(tmp_path / "consolidado.json")
    assert servico.caminho.read_bytes() == original


def test_nao_sobrescreve_destino(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / "consolidado.json"
    destino.write_bytes(b"preservar")
    with pytest.raises(FileExistsError):
        servico.exportar_relatorio_consolidado(destino)
    assert destino.read_bytes() == b"preservar"


def test_extensao_invalida(tmp_path: Path) -> None:
    destino = tmp_path / "consolidado.csv"
    with pytest.raises(ValueError, match="extensão"):
        _servico(tmp_path).exportar_relatorio_consolidado(destino)
    assert not destino.exists()


def test_filtro_invalido_nao_cria_arquivo(tmp_path: Path) -> None:
    destino = tmp_path / "consolidado.json"
    with pytest.raises(ValueError, match="Status"):
        _servico(tmp_path).exportar_relatorio_consolidado(destino, status="pendente")
    assert not destino.exists()


def test_json_invalido_nao_cria_relatorio(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    with servico.caminho.open("a", encoding="utf-8") as arquivo:
        arquivo.write("{invalido}\n")
    destino = tmp_path / "consolidado.json"
    with pytest.raises(ValueError, match="linha 4"):
        servico.exportar_relatorio_consolidado(destino)
    assert not destino.exists()


def test_quantidade_invalida_nao_cria_relatorio(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    eventos = [json.loads(linha) for linha in servico.caminho.read_text(encoding="utf-8").splitlines()]
    eventos[0]["atualizadas"] = -1
    servico.caminho.write_text(
        "".join(json.dumps(evento, ensure_ascii=False) + "\n" for evento in eventos),
        encoding="utf-8",
    )
    destino = tmp_path / "consolidado.json"
    with pytest.raises(ValueError, match="Quantidade atualizada inválida"):
        servico.exportar_relatorio_consolidado(destino)
    assert not destino.exists()


def test_json_utf8_preserva_acentos(tmp_path: Path) -> None:
    destino = tmp_path / "consolidado.json"
    _servico(tmp_path).exportar_relatorio_consolidado(destino)
    texto = destino.read_text(encoding="utf-8")
    assert "Audiência.docx" in texto
    assert "Data inválida" in texto


def test_filtro_datetime_com_fuso(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / "consolidado.json"
    limite = datetime(2000, 1, 1, tzinfo=timezone.utc)
    servico.exportar_relatorio_consolidado(destino, inicio=limite)
    dados = json.loads(destino.read_text(encoding="utf-8"))
    assert dados["auditoria"]["filtros"]["inicio"] == limite.isoformat()
    assert dados["resumo"]["total_operacoes"] == 3
