"""
Agenda Universal PRO
Arquivo: app.py

Ponto de entrada principal da aplicação.

Sprint 3.6:
- Menu interativo.
- Leitura e validação das configurações.
- Tratamento amigável de erros.
- Execução da atualização de agendas.
"""

from __future__ import annotations

from pathlib import Path

from config.agenda_config import AgendaConfig
from config.settings import (
    APP_NAME,
    APP_VERSION,
    create_directories,
)
from services.agenda_application import AgendaApplication
from services.logger_service import LoggerService


def exibir_cabecalho() -> None:
    """Exibe o cabeçalho principal da aplicação."""

    print()
    print("=" * 60)
    print(f"{APP_NAME} v{APP_VERSION}")
    print("=" * 60)
    print()


def exibir_menu() -> None:
    """Exibe o menu principal da aplicação."""

    print("MENU PRINCIPAL")
    print()
    print("1 - Atualizar agenda para um novo ano")
    print("0 - Sair")
    print()


def ler_ano(mensagem: str) -> int:
    """Solicita e valida um ano informado pelo usuário."""

    while True:
        valor = input(mensagem).strip()

        try:
            ano = int(valor)

            if ano < 1:
                print("Informe um ano válido.")
                continue

            return ano

        except ValueError:
            print(
                "Valor inválido. "
                "Informe o ano utilizando apenas números."
            )


def ler_arquivo_origem() -> Path:
    """Solicita e valida o arquivo de origem."""

    while True:
        caminho = Path(
            input(
                "Informe o caminho do arquivo de origem: "
            ).strip()
        )

        if not caminho.exists():
            print()
            print("Erro: o arquivo informado não existe.")
            print()
            continue

        if not caminho.is_file():
            print()
            print(
                "Erro: o caminho informado não corresponde "
                "a um arquivo."
            )
            print()
            continue

        if caminho.suffix.lower() != ".docx":
            print()
            print(
                "Erro: o arquivo deve possuir a extensão "
                ".docx."
            )
            print()
            continue

        return caminho


def ler_arquivo_destino() -> Path:
    """Solicita e valida o caminho do arquivo de destino."""

    while True:
        caminho = Path(
            input(
                "Informe o caminho do arquivo de destino: "
            ).strip()
        )

        if not caminho.name:
            print()
            print("Erro: informe um caminho válido.")
            print()
            continue

        if caminho.suffix.lower() != ".docx":
            print()
            print(
                "Erro: o arquivo de destino deve possuir "
                "a extensão .docx."
            )
            print()
            continue

        return caminho


def ler_configuracao() -> AgendaConfig:
    """Solicita os dados necessários para atualizar uma agenda."""

    print()
    print("CONFIGURAÇÃO DA ATUALIZAÇÃO")
    print("-" * 60)

    arquivo_origem = ler_arquivo_origem()
    arquivo_destino = ler_arquivo_destino()

    ano_origem = ler_ano(
        "Informe o ano de origem: "
    )

    ano_destino = ler_ano(
        "Informe o ano de destino: "
    )

    while ano_origem == ano_destino:
        print()
        print(
            "O ano de destino deve ser diferente "
            "do ano de origem."
        )
        print()

        ano_destino = ler_ano(
            "Informe novamente o ano de destino: "
        )

    return AgendaConfig(
        arquivo_origem=arquivo_origem,
        arquivo_destino=arquivo_destino,
        ano_origem=ano_origem,
        ano_destino=ano_destino,
    )


def executar_atualizacao(
    aplicacao: AgendaApplication,
) -> None:
    """Executa o processo de atualização da agenda."""

    logger = LoggerService.get_logger()

    try:
        config = ler_configuracao()

        print()
        print("Iniciando atualização da agenda...")
        print()

        quantidade = aplicacao.atualizar(config)

        print()
        print("=" * 60)
        print("Atualização concluída com sucesso.")
        print(
            f"Substituições realizadas: {quantidade}"
        )
        print(
            f"Arquivo gerado: {config.arquivo_destino}"
        )
        print("=" * 60)
        print()

    except (
        FileNotFoundError,
        FileExistsError,
        PermissionError,
        ValueError,
    ) as erro:
        logger.error(
            "Erro durante a atualização: %s",
            erro,
        )

        print()
        print(f"Erro: {erro}")
        print()

    except Exception:
        logger.exception(
            "Erro inesperado durante a atualização."
        )

        print()
        print(
            "Ocorreu um erro inesperado durante "
            "a atualização."
        )
        print(
            "Consulte o arquivo de log para "
            "mais detalhes."
        )
        print()


def main() -> None:
    """Executa o fluxo principal da aplicação."""

    create_directories()

    logger = LoggerService.get_logger()

    logger.info("=" * 60)
    logger.info(
        "%s v%s iniciado.",
        APP_NAME,
        APP_VERSION,
    )
    logger.info("=" * 60)

    aplicacao = AgendaApplication()

    while True:
        exibir_cabecalho()
        exibir_menu()

        opcao = input(
            "Escolha uma opção: "
        ).strip()

        if opcao == "1":
            executar_atualizacao(aplicacao)

            input(
                "Pressione ENTER para voltar ao menu..."
            )

        elif opcao == "0":
            print()
            print("Encerrando o programa...")

            logger.info(
                "Agenda Universal PRO encerrado."
            )

            break

        else:
            print()
            print(
                "Opção inválida. "
                "Escolha uma opção do menu."
            )

            input(
                "Pressione ENTER para continuar..."
            )


if __name__ == "__main__":
    main()