from config.settings import (
    APP_NAME,
    APP_VERSION,
    create_directories,
)


def main() -> None:
    create_directories()

    print(f"{APP_NAME} v{APP_VERSION}")
    print("Projeto iniciado com sucesso.")


if __name__ == "__main__":
    main()