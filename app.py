from config.settings import (
    APP_NAME,
    APP_VERSION,
    create_directories,
)

from services.logger_service import LoggerService

def main() -> None:
    create_directories()

    logger = LoggerService.get_logger()

    logger.info(f"{APP_NAME} v{APP_VERSION}")

    print(f"{APP_NAME} v{APP_VERSION}")
    print("Projeto iniciado com sucesso.")


if __name__ == "__main__":
    main()