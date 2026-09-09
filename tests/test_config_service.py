"""
Agenda Universal PRO
Arquivo: tests/test_config_service.py

Testes do serviço de configurações persistentes.

Sprint 4.1:
- Testa carregamento e salvamento das configurações.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from config.app_config import AppConfig
from services.config_service import ConfigService


def testar_configuracao_padrao() -> None:
    """Testa o carregamento da configuração padrão."""

    with TemporaryDirectory() as diretorio_temporario:
        arquivo_config = (
            Path(diretorio_temporario)
            / "app_config.json"
        )

        service = ConfigService(arquivo_config)
        config = service.carregar()

        assert config.diretorio_origem == Path(
            "modelos"
        )

        assert config.diretorio_destino == Path(
            "output"
        )


def testar_salvar_e_carregar_configuracao() -> None:
    """Testa o salvamento e carregamento da configuração."""

    with TemporaryDirectory() as diretorio_temporario:
        arquivo_config = (
            Path(diretorio_temporario)
            / "config"
            / "app_config.json"
        )

        service = ConfigService(arquivo_config)

        config_original = AppConfig(
            diretorio_origem=Path("meus_modelos"),
            diretorio_destino=Path("meus_arquivos"),
        )

        service.salvar(config_original)

        assert arquivo_config.exists()

        config_carregada = service.carregar()

        assert (
            config_carregada.diretorio_origem
            == Path("meus_modelos")
        )

        assert (
            config_carregada.diretorio_destino
            == Path("meus_arquivos")
        )


def main() -> None:
    """Executa os testes do ConfigService."""

    print()
    print("=== TESTE CONFIG SERVICE ===")
    print()

    testar_configuracao_padrao()
    print("Configuração padrão: OK")

    testar_salvar_e_carregar_configuracao()
    print("Salvamento e carregamento: OK")

    print()
    print("Teste concluído com sucesso.")


if __name__ == "__main__":
    main()
