
"""
Agenda Universal PRO
Arquivo: tests/test_config_service.py

Testes do serviço de configurações persistentes.

Valida:
- Caminho padrão do JSON.
- Diretórios padrão da aplicação.
- Salvamento e carregamento.
- JSON inválido ou incompleto.
- Campos inválidos ou vazios.
- Preservação dos caminhos personalizados.
"""

import json
from pathlib import Path

import pytest

from config.app_config import AppConfig
from config.settings import MODELOS_DIR, OUTPUT_DIR
from services.config_service import ConfigService


def test_inicializa_com_arquivo_padrao() -> None:
    """Verifica o caminho padrão no ambiente Python."""

    service = ConfigService()

    assert service.arquivo_config == (
        Path("data") / "app_config.json"
    )


def test_carregar_configuracao_padrao(
    tmp_path: Path,
) -> None:
    """Carrega os diretórios padrão quando não há JSON."""

    arquivo_config = tmp_path / "app_config.json"
    service = ConfigService(arquivo_config)

    config = service.carregar()

    assert config.diretorio_origem == MODELOS_DIR
    assert config.diretorio_destino == OUTPUT_DIR


def test_salvar_e_carregar_configuracao(
    tmp_path: Path,
) -> None:
    """Preserva diretórios personalizados."""

    arquivo_config = tmp_path / "config" / "app_config.json"
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


def test_carregar_json_invalido(
    tmp_path: Path,
) -> None:
    """Recupera os padrões após JSON inválido."""

    arquivo_config = tmp_path / "app_config.json"
    arquivo_config.write_text(
        "{ json inválido",
        encoding="utf-8",
    )

    config = ConfigService(arquivo_config).carregar()

    assert config.diretorio_origem == MODELOS_DIR
    assert config.diretorio_destino == OUTPUT_DIR


def test_carregar_json_nao_objeto(
    tmp_path: Path,
) -> None:
    """Recupera os padrões quando o JSON não é objeto."""

    arquivo_config = tmp_path / "app_config.json"
    arquivo_config.write_text(
        json.dumps(["modelos", "output"]),
        encoding="utf-8",
    )

    config = ConfigService(arquivo_config).carregar()

    assert config.diretorio_origem == MODELOS_DIR
    assert config.diretorio_destino == OUTPUT_DIR


@pytest.mark.parametrize(
    "dados, origem_esperada, destino_esperado",
    [
        (
            {
                "diretorio_origem": 123,
                "diretorio_destino": "output",
            },
            MODELOS_DIR,
            Path("output"),
        ),
        (
            {
                "diretorio_origem": "modelos",
                "diretorio_destino": 456,
            },
            Path("modelos"),
            OUTPUT_DIR,
        ),
        (
            {
                "diretorio_origem": None,
                "diretorio_destino": "output",
            },
            MODELOS_DIR,
            Path("output"),
        ),
        (
            {
                "diretorio_origem": "modelos",
                "diretorio_destino": None,
            },
            Path("modelos"),
            OUTPUT_DIR,
        ),
    ],
)
def test_carregar_campos_invalidos(
    tmp_path: Path,
    dados: dict[str, object],
    origem_esperada: Path,
    destino_esperado: Path,
) -> None:
    """Usa o padrão somente para o campo inválido."""

    arquivo_config = tmp_path / "app_config.json"
    arquivo_config.write_text(
        json.dumps(dados),
        encoding="utf-8",
    )

    config = ConfigService(arquivo_config).carregar()

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
            MODELOS_DIR,
            Path("output"),
        ),
        (
            {
                "diretorio_origem": " ",
                "diretorio_destino": "output",
            },
            MODELOS_DIR,
            Path("output"),
        ),
        (
            {
                "diretorio_origem": "modelos",
                "diretorio_destino": "",
            },
            Path("modelos"),
            OUTPUT_DIR,
        ),
        (
            {
                "diretorio_origem": "modelos",
                "diretorio_destino": " ",
            },
            Path("modelos"),
            OUTPUT_DIR,
        ),
    ],
)
def test_carregar_campos_vazios(
    tmp_path: Path,
    dados: dict[str, str],
    origem_esperada: Path,
    destino_esperado: Path,
) -> None:
    """Usa os padrões para campos vazios."""

    arquivo_config = tmp_path / "app_config.json"
    arquivo_config.write_text(
        json.dumps(dados),
        encoding="utf-8",
    )

    config = ConfigService(arquivo_config).carregar()

    assert config.diretorio_origem == origem_esperada
    assert config.diretorio_destino == destino_esperado


def test_carregar_configuracao_incompleta(
    tmp_path: Path,
) -> None:
    """Mantém o campo válido e preenche o ausente."""

    arquivo_config = tmp_path / "app_config.json"
    dados = {
        "diretorio_origem": "meus_modelos",
    }

    arquivo_config.write_text(
        json.dumps(dados),
        encoding="utf-8",
    )

    config = ConfigService(arquivo_config).carregar()

    assert config.diretorio_origem == Path("meus_modelos")
    assert config.diretorio_destino == OUTPUT_DIR


def test_app_config_utiliza_diretorios_padrao() -> None:
    """Verifica os valores padrão do modelo."""

    config = AppConfig()

    assert config.diretorio_origem == MODELOS_DIR
    assert config.diretorio_destino == OUTPUT_DIR
