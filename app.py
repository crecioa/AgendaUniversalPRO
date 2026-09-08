"""
Agenda Universal PRO
Arquivo: app.py

Ponto de entrada principal da aplicação.

Sprint 3.9:

* Menu interativo.
* Validação dos dados informados.
* Resumo da configuração.
* Confirmação da atualização.
* Cancelamento seguro.
* Proteção contra sobrescrita de arquivos.
* Criação automática do diretório de destino.
* Proteção contra origem e destino iguais.
* Listagem de arquivos disponíveis na pasta modelos.
* Seleção interativa do arquivo de origem.
* Possibilidade de informar o caminho manualmente.
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


def listar_arquivos_modelos() -> list[Path]:
    """Retorna os arquivos DOCX disponíveis na pasta modelos."""
    pasta_modelos = Path("modelos")

    if not pasta_modelos.exists():
        return []

    arquivos = [
        arquivo
        for arquivo in pasta_modelos.glob("*.docx")
        if arquivo.is_file() and not arquivo.name.startswith("~$")
    ]

    return sorted(arquivos)


def exibir_arquivos_modelos(arquivos: list[Path]) -> None:
    """Exibe os arquivos disponíveis para seleção."""
    print()
    print("ARQUIVOS DISPONÍVEIS")
    print("-" * 60)

    for indice, arquivo in enumerate(arquivos, start=1):
        print(f"{indice} - {arquivo.name}")

    print()
    print("M - Informar um caminho manualmente")
    print("0 - Voltar")
    print()


def selecionar_arquivo_modelo() -> Path | None:
    """Permite selecionar um arquivo disponível na pasta modelos."""
    arquivos = listar_arquivos_modelos()

    if not arquivos:
        return None

    while True:
        exibir_arquivos_modelos(arquivos)

        escolha = input("Escolha o arquivo de origem: ").strip()

        if escolha == "0":
            return None

        if escolha.upper() == "M":
            return Path(
                input("Informe o caminho do arquivo de origem: ").strip()
            )

        try:
            indice = int(escolha)

            if 1 <= indice <= len(arquivos):
                return arquivos[indice - 1]

            print()
            print("Opção inválida. Escolha um número da lista.")
            print()

        except ValueError:
            print()
            print("Opção inválida. Informe um número, M ou 0.")
            print()


def validar_arquivo_origem(caminho: Path) -> Path | None:
    """Valida um arquivo informado como origem."""
    if not caminho.exists():
        print()
        print("Erro: o arquivo informado não existe.")
        print()
        return None

    if not caminho.is_file():
        print()
        print("Erro: o caminho informado não corresponde a um arquivo.")
        print()
        return None

    if caminho.suffix.lower() != ".docx":
        print()
        print("Erro: o arquivo deve possuir a extensão .docx.")
        print()
        return None

    return caminho


def ler_arquivo_origem() -> Path:
    """Solicita e valida o arquivo de origem."""
    while True:
        caminho = selecionar_arquivo_modelo()

        if caminho is None:
            print()
            print("Informe o caminho do arquivo de origem.")
            print()
            caminho = Path(input("Informe o caminho do arquivo de origem: ").strip())

        arquivo = validar_arquivo_origem(caminho)

        if arquivo is not None:
            return arquivo


def confirmar_sobrescrita(caminho: Path) -> bool:
    """Solicita confirmação para sobrescrever um arquivo."""
    print()
    print("O arquivo de destino já existe:")
    print(caminho)
    print()

    while True:
        resposta = input("Deseja sobrescrever o arquivo? (S/N): ").strip().upper()

        if resposta == "S":
            return True

        if resposta == "N":
            return False

        print()
        print("Resposta inválida. Digite S para confirmar ou N para cancelar.")
        print()


def ler_arquivo_destino() -> Path:
    """Solicita, valida e protege o arquivo de destino."""
    while True:
        caminho = Path(input("Informe o caminho do arquivo de destino: ").strip())

        if not caminho.name:
            print()
            print("Erro: informe um caminho válido.")
            print()
            continue

        if caminho.suffix.lower() != ".docx":
            print()
            print("Erro: o arquivo de destino deve possuir a extensão .docx.")
            print()
            continue

        if caminho.exists():
            if confirmar_sobrescrita(caminho):
                return caminho

            print()
            print("Informe outro arquivo de destino.")
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

    ano_origem = ler_ano("Informe o ano de origem: ")
    ano_destino = ler_ano("Informe o ano de destino: ")

    while ano_origem == ano_destino:
        print()
        print("O ano de destino deve ser diferente do ano de origem.")
        print()
        ano_destino = ler_ano("Informe novamente o ano de destino: ")

    return AgendaConfig(
        arquivo_origem=arquivo_origem,
        arquivo_destino=arquivo_destino,
        ano_origem=ano_origem,
        ano_destino=ano_destino,
    )


def exibir_resumo_configuracao(config: AgendaConfig) -> None:
    """Exibe um resumo da atualização configurada."""
    print()
    print("RESUMO DA ATUALIZAÇÃO")
    print("-" * 60)

    print(f"Arquivo de origem: {config.arquivo_origem}")
    print(f"Arquivo de destino: {config.arquivo_destino}")
    print(f"Ano de origem: {config.ano_origem}")
    print(f"Ano de destino: {config.ano_destino}")

    print("-" * 60)
    print()


def confirmar_atualizacao() -> bool:
    """Solicita confirmação do usuário para iniciar a atualização."""
    while True:
        resposta = input("Deseja confirmar a atualização? (S/N): ").strip().upper()

        if resposta == "S":
            return True

        if resposta == "N":
            return False

        print()
        print("Resposta inválida. Digite S para confirmar ou N para cancelar.")
        print()


def executar_atualizacao(aplicacao: AgendaApplication) -> None:
    """Executa o processo de atualização da agenda."""
    logger = LoggerService.get_logger()

    try:
        config = ler_configuracao()

        exibir_resumo_configuracao(config)

        if not confirmar_atualizacao():
            print()
            print("Atualização cancelada pelo usuário.")
            logger.info("Atualização cancelada pelo usuário.")
            print()
            return

        print()
        print("Iniciando atualização da agenda...")
        print()

        quantidade = aplicacao.atualizar(config)

        print()
        print("=" * 60)
        print("Atualização concluída com sucesso.")
        print(f"Substituições realizadas: {quantidade}")
        print(f"Arquivo gerado: {config.arquivo_destino}")
        print("=" * 60)
        print()

    except (
        FileNotFoundError,
        FileExistsError,
        PermissionError,
        ValueError,
    ) as erro:
        logger.error("Erro durante a atualização: %s", erro)
        print()
        print(f"Erro: {erro}")
        print()

    except Exception:
        logger.exception("Erro inesperado durante a atualização.")
        print()
        print("Ocorreu um erro inesperado durante a atualização.")
        print("Consulte o arquivo de log para mais detalhes.")
        print()


def main() -> None:
    """Executa o fluxo principal da aplicação."""
    create_directories()

    logger = LoggerService.get_logger()

    logger.info("=" * 60)
    logger.info("%s v%s iniciado.", APP_NAME, APP_VERSION)
    logger.info("=" * 60)

    aplicacao = AgendaApplication()

    while True:
        exibir_cabecalho()
        exibir_menu()

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            executar_atualizacao(aplicacao)
            input("Pressione ENTER para voltar ao menu...")

        elif opcao == "0":
            print()
            print("Encerrando o programa...")
            logger.info("Agenda Universal PRO encerrado.")
            break

        else:
            print()
            print("Opção inválida. Escolha uma opção do menu.")
            input("Pressione ENTER para continuar...")


if __name__ == "__main__":
    main()
