"""
Agenda Universal PRO
Arquivo: app.py

Ponto de entrada principal da aplicação.
"""
from pathlib import Path
from config.agenda_config import AgendaConfig
from config.settings import (
APP_NAME,
APP_VERSION,
create_directories,
)
from services.agenda_application import AgendaApplication
from services.logger_service import LoggerService

def main() -> None:
    """Inicializa e executa a aplicação."""
    create_directories()

    logger = LoggerService.get_logger()

    logger.info("=" * 60)
    logger.info("%s v%s iniciado.", APP_NAME, APP_VERSION)
    logger.info("=" * 60)

    print()
    print("=" * 60)
    print(f"{APP_NAME} v{APP_VERSION}")
    print("=" * 60)
    print()

    arquivo_origem = input(
        "Informe o caminho do arquivo de origem: "
    ).strip()

    arquivo_destino = input(
        "Informe o caminho do arquivo de destino: "
    ).strip()

    ano_origem = int(
        input("Informe o ano de origem: ").strip()
    )

    ano_destino = int(
        input("Informe o ano de destino: ").strip()
    )

    config = AgendaConfig(
    arquivo_origem=Path(arquivo_origem),
    arquivo_destino=Path(arquivo_destino),
    ano_origem=ano_origem,
    ano_destino=ano_destino,
)

    aplicacao = AgendaApplication()

    try:
        quantidade = aplicacao.atualizar(config)

        print()
        print(
            "Atualização concluída com sucesso."
        )
        print(
            f"Substituições realizadas: {quantidade}"
        )

    except (
        FileNotFoundError,
        ValueError,
        PermissionError,
    ) as erro:
        logger.error(
            "Erro durante a atualização: %s",
            erro,
        )

        print()
        print(f"Erro: {erro}")


if __name__ == "__main__":
    main()
