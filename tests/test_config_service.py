"""
Agenda Universal PRO
Arquivo: tests/test_config_service.py

Testes do serviço de configurações persistentes.

Sprint 4.9:
- Testa carregamento da configuração padrão.
- Testa salvamento e carregamento.
- Testa JSON inválido.
- Testa JSON que não contém um objeto.
- Testa campos inválidos.
- Testa campos vazios.
- Testa configuração incompleta.
"""

import json
from pathlib import Path

import pytest

from config.app_config import AppConfig
from services.config_service import ConfigService


def test_carregar_configuracao_padrao(tmp_path: Path) -> None:
    """Testa o carregamento da configuração padrão."""

    arquivo_config = tmp_path / "app_config.json"

    service = ConfigService(arquivo_config)

    config = service.carregar()

    assert config.diretorio_origem == Path("modelos")
    assert config.diretorio_destino == Path("output")


def test_salvar_e_carregar_configuracao(tmp_path: Path) -> None:
    """Testa o salvamento e carregamento da configuração."""

    arquivo_config = (
        tmp_path / "config" / "app_config.json"
    )

    service = ConfigService(arquivo_config)

    config_original = AppConfig(
        diretorio_origem=Path("meus_modelos"),
        diretorio_destino=Path("meus_arquivos"),
    )

    service.salvar(config_original)

    assert arquivo_config.exists()

    config_carregada = service.carregar()

    assert config_carregada.diretorio_origem == Path(
        "meus_modelos"
    )
    assert config_carregada.diretorio_destino == Path(
        "meus_arquivos"
    )


def test_carregar_json_invalido(tmp_path: Path) -> None:
    """Testa recuperação após JSON inválido."""

    arquivo_config = tmp_path / "app_config.json"

    arquivo_config.write_text(
        "{ json inválido",
        encoding="utf-8",
    )

    service = ConfigService(arquivo_config)

    config = service.carregar()

    assert config.diretorio_origem == Path("modelos")
    assert config.diretorio_destino == Path("output")


def test_carregar_json_nao_objeto(tmp_path: Path) -> None:
    """Testa recuperação quando o JSON não é um objeto."""

    arquivo_config = tmp_path / "app_config.json"

    arquivo_config.write_text(
        json.dumps(["modelos", "output"]),
        encoding="utf-8",
    )

    service = ConfigService(arquivo_config)

    config = service.carregar()

    assert config.diretorio_origem == Path("modelos")
    assert config.diretorio_destino == Path("output")


@pytest.mark.parametrize(
    "dados, origem_esperada, destino_esperado",
    [
        (
            {
                "diretorio_origem": 123,
                "diretorio_destino": "output",
            },
            Path("modelos"),
            Path("output"),
        ),
        (
            {
                "diretorio_origem": "modelos",
                "diretorio_destino": 456,
            },
            Path("modelos"),
            Path("output"),
        ),
        (
            {
                "diretorio_origem": None,
                "diretorio_destino": "output",
            },
            Path("modelos"),
            Path("output"),
        ),
        (
            {
                "diretorio_origem": "modelos",
                "diretorio_destino": None,
            },
            Path("modelos"),
            Path("output"),
        ),
    ],
)
def test_carregar_campos_invalidos(
    tmp_path: Path,
    dados: dict[str, object],
    origem_esperada: Path,
    destino_esperado: Path,
) -> None:
    """Testa recuperação de campos com tipos inválidos."""

    arquivo_config = tmp_path / "app_config.json"

    arquivo_config.write_text(
        json.dumps(dados),
        encoding="utf-8",
    )

    service = ConfigService(arquivo_config)

    config = service.carregar()

    assert config.diretorio_origem == origem_esperada
    assert config.diretorio_destino == destino_esperado


@pytest.mark.parametrize(
    "dados, origem_esperada, destino_esperado",
    [
        (
            {
                "diretorio_origem": "",
                "diretorio_destino": "output",
            },
            Path("modelos"),
            Path("output"),
        ),
        (
            {
                "diretorio_origem": "   ",
                "diretorio_destino": "output",
            },
            Path("modelos"),
            Path("output"),
        ),
        (
            {
                "diretorio_origem": "modelos",
                "diretorio_destino": "",
            },
            Path("modelos"),
            Path("output"),
        ),
        (
            {
                "diretorio_origem": "modelos",
                "diretorio_destino": "   ",
            },
            Path("modelos"),
            Path("output"),
        ),
    ],
)
def test_carregar_campos_vazios(
    tmp_path: Path,
    dados: dict[str, str],
    origem_esperada: Path,
    destino_esperado: Path,
) -> None:
    """Testa recuperação de campos vazios."""

    arquivo_config = tmp_path / "app_config.json"

    arquivo_config.write_text(
        json.dumps(dados),
        encoding="utf-8",
    )

    service = ConfigService(arquivo_config)

    config = service.carregar()

    assert config.diretorio_origem == origem_esperada
    assert config.diretorio_destino == destino_esperado


def test_carregar_configuracao_incompleta(
    tmp_path: Path,
) -> None:
    """Testa configuração com campo ausente."""

    arquivo_config = tmp_path / "app_config.json"

    dados = {
        "diretorio_origem": "meus_modelos",
    }

    arquivo_config.write_text(
        json.dumps(dados),
        encoding="utf-8",
    )

    service = ConfigService(arquivo_config)

    config = service.carregar()

    assert config.diretorio_origem == Path(
        "meus_modelos"
    )
    assert config.diretorio_destino == Path("output")