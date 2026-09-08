"""
Agenda Universal PRO
Arquivo: app.py

Ponto de entrada principal da aplicação.

Sprint 3.8:

* Menu interativo.
* Validação dos dados informados.
* Resumo da configuração.
* Confirmação da atualização.
* Cancelamento seguro.
* Proteção contra sobrescrita de arquivos.
* Criação automática do diretório de destino.
* Proteção contra origem e destino iguais.
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
                print()
                print("Informe um ano válido.")
                print()
                continue

            return ano

        except ValueError:
            print()
            print(
                "Valor inválido. "
                "Informe o ano utilizando apenas números."
            )
            print()


def ler_arquivo_origem() -> Path:
    """Solicita e valida o arquivo de origem."""
    while True:
        valor = input(
            "Informe o caminho do arquivo de origem: "
        ).strip()

        if not valor:
            print()
            print(
                "Erro: informe o caminho do arquivo de origem."
            )
            print()
            continue

        caminho = Path(valor)

        if not caminho.exists():
            print()
            print(
                "Erro: o arquivo informado não existe."
            )
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


def confirmar_sobrescrita(caminho: Path) -> bool:
    """Solicita confirmação para sobrescrever um arquivo."""
    print()
    print(
        "O arquivo de destino já existe:"
    )
    print(caminho)
    print()

    while True:
        resposta = input(
            "Deseja sobrescrever o arquivo? (S/N): "
        ).strip().upper()

        if resposta == "S":
            return True

        if resposta == "N":
            return False

        print()
        print(
            "Resposta inválida. "
            "Digite S para confirmar ou N para cancelar."
        )
        print()


def criar_diretorio_destino(caminho: Path) -> None:
    """Cria o diretório de destino quando necessário."""
    diretorio = caminho.parent

    if diretorio == Path("."):
        return

    diretorio.mkdir(
        parents=True,
        exist_ok=True,
    )


def caminhos_sao_iguais(
    arquivo_origem: Path,
    arquivo_destino: Path,
) -> bool:
    """Verifica se origem e destino representam o mesmo arquivo."""
    try:
        return (
            arquivo_origem.resolve()
            == arquivo_destino.resolve()
        )

    except OSError:
        return (
            arquivo_origem.absolute()
            == arquivo_destino.absolute()
        )


def ler_arquivo_destino(
    arquivo_origem: Path,
) -> Path:
    """Solicita, valida e prepara o arquivo de destino."""
    while True:
        valor = input(
            "Informe o caminho do arquivo de destino: "
        ).strip()

        if not valor:
            print()
            print(
                "Erro: informe o caminho do arquivo de destino."
            )
            print()
            continue

        caminho = Path(valor)

        if not caminho.name:
            print()
            print(
                "Erro: informe um caminho válido."
            )
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

        if caminhos_sao_iguais(
            arquivo_origem,
            caminho,
        ):
            print()
            print(
                "Erro: o arquivo de destino não pode ser "
                "o mesmo arquivo de origem."
            )
            print()
            continue

        if caminho.exists():
            if confirmar_sobrescrita(
                caminho
            ):
                criar_diretorio_destino(
                    caminho
                )
                return caminho

            print()
            print(
                "Informe outro arquivo de destino."
            )
            print()
            continue

        criar_diretorio_destino(caminho)

        return caminho


def ler_configuracao() -> AgendaConfig:
    """Solicita os dados necessários para atualizar uma agenda."""
    print()
    print("CONFIGURAÇÃO DA ATUALIZAÇÃO")
    print("-" * 60)

    arquivo_origem = ler_arquivo_origem()

    arquivo_destino = ler_arquivo_destino(
        arquivo_origem
    )

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


def exibir_resumo_configuracao(
    config: AgendaConfig,
) -> None:
    """Exibe um resumo da atualização configurada."""
    print()
    print("RESUMO DA ATUALIZAÇÃO")
    print("-" * 60)

    print(
        f"Arquivo de origem: "
        f"{config.arquivo_origem}"
    )

    print(
        f"Arquivo de destino: "
        f"{config.arquivo_destino}"
    )

    print(
        f"Ano de origem: "
        f"{config.ano_origem}"
    )

    print(
        f"Ano de destino: "
        f"{config.ano_destino}"
    )

    print("-" * 60)
    print()


def confirmar_atualizacao() -> bool:
    """Solicita confirmação para iniciar a atualização."""
    while True:
        resposta = input(
            "Deseja confirmar a atualização? (S/N): "
        ).strip().upper()

        if resposta == "S":
            return True

        if resposta == "N":
            return False

        print()
        print(
            "Resposta inválida. "
            "Digite S para confirmar ou N para cancelar."
        )
        print()


def executar_atualizacao(
    aplicacao: AgendaApplication,
) -> None:
    """Executa o processo de atualização da agenda."""
    logger = LoggerService.get_logger()

    try:
        config = ler_configuracao()

        exibir_resumo_configuracao(
            config
        )

        if not confirmar_atualizacao():
            print()
            print(
                "Atualização cancelada pelo usuário."
            )

            logger.info(
                "Atualização cancelada pelo usuário."
            )

            print()

            return

        print()
        print(
            "Iniciando atualização da agenda..."
        )
        print()

        quantidade = aplicacao.atualizar(
            config
        )

        print()
        print("=" * 60)
        print(
            "Atualização concluída com sucesso."
        )

        print(
            f"Substituições realizadas: "
            f"{quantidade}"
        )

        print(
            f"Arquivo gerado: "
            f"{config.arquivo_destino}"
        )

        print("=" * 60)
        print()

    except (
        FileNotFoundError,
        FileExistsError,
        PermissionError,
        ValueError,
        OSError,
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
            executar_atualizacao(
                aplicacao
            )

            input(
                "Pressione ENTER para voltar ao menu..."
            )

        elif opcao == "0":
            print()
            print(
                "Encerrando o programa..."
            )

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
