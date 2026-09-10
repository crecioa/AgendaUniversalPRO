from __future__ import annotations

from pathlib import Path

from config.agenda_config import AgendaConfig
from config.app_config import AppConfig
from config.settings import create_directories
from services.agenda_application import AgendaApplication
from services.config_service import ConfigService
from services.logger_service import LoggerService

logger = LoggerService.get_logger()


def listar_arquivos_modelos(
    diretorio_origem: Path,
) -> list[Path]:
    """Lista os arquivos DOCX disponíveis no diretório de origem."""
    if not diretorio_origem.exists():
        return []

    if not diretorio_origem.is_dir():
        return []

    arquivos = [
        arquivo
        for arquivo in diretorio_origem.glob("*.docx")
        if arquivo.is_file()
        and not arquivo.name.startswith("~$")
    ]

    return sorted(arquivos)


def selecionar_arquivo_modelo(
    diretorio_origem: Path,
) -> Path | None:
    """Permite selecionar um arquivo DOCX ou cancelar a operação."""
    arquivos = listar_arquivos_modelos(diretorio_origem)

    print()
    print("ARQUIVOS DE MODELO")
    print("-" * 60)

    if not arquivos:
        print(
            f"Nenhum arquivo DOCX encontrado em: "
            f"{diretorio_origem}"
        )
    else:
        for indice, arquivo in enumerate(arquivos, start=1):
            print(f"{indice} - {arquivo.name}")

    print()
    print("M - Informar outro arquivo manualmente")
    print("0 - Voltar")

    while True:
        escolha = input("\nEscolha uma opção: ").strip()

        if escolha == "0":
            return None

        if escolha.upper() == "M":
            caminho = input(
                "Informe o caminho completo do arquivo DOCX: "
            ).strip()

            if not caminho:
                print("Caminho não informado.")
                continue

            arquivo = Path(caminho)

            if not arquivo.exists():
                print("Arquivo não encontrado.")
                continue

            if not arquivo.is_file():
                print("O caminho informado não é um arquivo.")
                continue

            if arquivo.suffix.lower() != ".docx":
                print("O arquivo precisa ter extensão .docx.")
                continue

            return arquivo

        if escolha.isdigit():
            indice = int(escolha)

            if 1 <= indice <= len(arquivos):
                return arquivos[indice - 1]

        print("Opção inválida. Tente novamente.")


def ler_arquivo_origem(
    diretorio_origem: Path,
) -> Path | None:
    """Obtém o arquivo de origem da atualização."""
    if not diretorio_origem.exists():
        print()
        print(
            f"O diretório de origem não existe: "
            f"{diretorio_origem}"
        )
        print()
        return None

    if not diretorio_origem.is_dir():
        print()
        print(
            f"O caminho de origem não é um diretório: "
            f"{diretorio_origem}"
        )
        print()
        return None

    return selecionar_arquivo_modelo(diretorio_origem)


def ler_arquivo_destino(
    diretorio_destino: Path,
) -> Path | None:
    """Obtém o nome do arquivo de destino."""
    print()
    print("ARQUIVO DE DESTINO")
    print("-" * 60)
    print(
        f"Diretório de destino configurado: "
        f"{diretorio_destino}"
    )
    print()
    print("Informe apenas o nome do arquivo.")
    print("Exemplo: agenda_2027.docx")
    print("0 - Voltar")

    while True:
        nome_arquivo = input(
            "\nNome do arquivo de destino: "
        ).strip()

        if nome_arquivo == "0":
            return None

        if not nome_arquivo:
            print("Nome do arquivo não informado.")
            continue

        caminho = Path(nome_arquivo)

        if caminho.name != nome_arquivo:
            print(
                "Informe somente o nome do arquivo, "
                "sem outro diretório."
            )
            continue

        if caminho.suffix.lower() != ".docx":
            print("O arquivo de destino precisa ser .docx.")
            continue

        return diretorio_destino / caminho.name


def ler_configuracao(
    config_app: AppConfig,
    arquivo_origem: Path,
    arquivo_destino: Path,
) -> AgendaConfig:
    """Monta a configuração da atualização da agenda."""
    print()
    print("CONFIGURAÇÃO DA ATUALIZAÇÃO")
    print("-" * 60)

    while True:
        try:
            ano_origem = int(
                input("Informe o ano atual da agenda: ").strip()
            )
            break
        except ValueError:
            print("Informe um ano válido.")

    while True:
        try:
            ano_destino = int(
                input("Informe o novo ano da agenda: ").strip()
            )

            if ano_destino == ano_origem:
                print(
                    "O ano de origem e o ano de destino "
                    "devem ser diferentes."
                )
                continue

            break

        except ValueError:
            print("Informe um ano válido.")

    return AgendaConfig(
        arquivo_origem=arquivo_origem,
        arquivo_destino=arquivo_destino,
        ano_origem=ano_origem,
        ano_destino=ano_destino,
    )


def executar_atualizacao(
    aplicacao: AgendaApplication,
    config_app: AppConfig,
) -> None:
    """Executa o processo completo de atualização."""
    arquivo_origem = ler_arquivo_origem(
        config_app.diretorio_origem
    )

    if arquivo_origem is None:
        print()
        print("Operação cancelada.")
        return

    arquivo_destino = ler_arquivo_destino(
        config_app.diretorio_destino
    )

    if arquivo_destino is None:
        print()
        print("Operação cancelada.")
        return

    config = ler_configuracao(
        config_app,
        arquivo_origem,
        arquivo_destino,
    )

    print()
    print("CONFIGURAÇÃO SELECIONADA")
    print("-" * 60)
    print(f"Arquivo de origem: {config.arquivo_origem}")
    print(f"Arquivo de destino: {config.arquivo_destino}")
    print(f"Ano de origem: {config.ano_origem}")
    print(f"Ano de destino: {config.ano_destino}")
    print("-" * 60)

    confirmar = input(
        "Deseja iniciar a atualização? (S/N): "
    ).strip().upper()

    if confirmar != "S":
        print()
        print("Operação cancelada pelo usuário.")
        return

    try:
        print()
        print("Iniciando atualização da agenda...")

        resultado = aplicacao.atualizar(config)

        print()
        print("Atualização concluída com sucesso.")

        print(
            f"Substituições realizadas: {resultado}"
        )
        print(
            f"Arquivo gerado: {config.arquivo_destino}"
        )

    except Exception as exc:
        logger.exception(
            "Erro durante a atualização da agenda."
        )

        print()
        print("ERRO DURANTE A ATUALIZAÇÃO")
        print("-" * 60)
        print(str(exc))
        print("-" * 60)


def exibir_configuracoes(
    config_app: AppConfig,
) -> None:
    """Exibe as configurações persistentes atuais."""
    print()
    print("CONFIGURAÇÕES ATUAIS")
    print("-" * 60)
    print(
        f"Diretório de origem: "
        f"{config_app.diretorio_origem}"
    )
    print(
        f"Diretório de destino: "
        f"{config_app.diretorio_destino}"
    )
    print("-" * 60)


def ler_novo_diretorio_origem() -> Path | None:
    """Solicita e valida um novo diretório de origem."""
    print()
    print("ALTERAR DIRETÓRIO DE ORIGEM")
    print("-" * 60)
    print("0 - Cancelar")

    while True:
        entrada = input(
            "\nInforme o novo diretório de origem: "
        ).strip()

        if entrada == "0":
            return None

        if not entrada:
            print("Diretório não informado.")
            continue

        diretorio = Path(entrada)

        if not diretorio.exists():
            print(
                "O diretório informado não existe."
            )
            continue

        if not diretorio.is_dir():
            print(
                "O caminho informado não é um diretório."
            )
            continue

        return diretorio


def ler_novo_diretorio_destino() -> Path | None:
    """Solicita e valida um novo diretório de destino."""
    print()
    print("ALTERAR DIRETÓRIO DE DESTINO")
    print("-" * 60)
    print("0 - Cancelar")

    while True:
        entrada = input(
            "\nInforme o novo diretório de destino: "
        ).strip()

        if entrada == "0":
            return None

        if not entrada:
            print("Diretório não informado.")
            continue

        diretorio = Path(entrada)

        if diretorio.exists():
            if not diretorio.is_dir():
                print(
                    "O caminho informado existe, "
                    "mas não é um diretório."
                )
                continue

            return diretorio

        print()
        print(
            f"O diretório '{diretorio}' ainda não existe."
        )

        criar = input(
            "Deseja criá-lo? (S/N): "
        ).strip().upper()

        if criar != "S":
            print("Diretório não alterado.")
            continue

        try:
            diretorio.mkdir(
                parents=True,
                exist_ok=True,
            )

            print(
                f"Diretório criado: {diretorio}"
            )

            return diretorio

        except OSError as exc:
            print(
                f"Não foi possível criar o diretório: "
                f"{exc}"
            )


def alterar_configuracoes(
    config_service: ConfigService,
    config_app: AppConfig,
) -> None:
    """Permite alterar e salvar as configurações."""
    while True:
        exibir_configuracoes(config_app)

        print()
        print("1 - Alterar diretório de origem")
        print("2 - Alterar diretório de destino")
        print("0 - Voltar")

        escolha = input(
            "\nEscolha uma opção: "
        ).strip()

        if escolha == "0":
            return

        if escolha == "1":
            novo_diretorio = (
                ler_novo_diretorio_origem()
            )

            if novo_diretorio is None:
                continue

            config_app.diretorio_origem = novo_diretorio

            config_service.salvar(config_app)

            print()
            print(
                "Diretório de origem atualizado "
                "com sucesso."
            )
            continue

        if escolha == "2":
            novo_diretorio = (
                ler_novo_diretorio_destino()
            )

            if novo_diretorio is None:
                continue

            config_app.diretorio_destino = (
                novo_diretorio
            )

            config_service.salvar(config_app)

            print()
            print(
                "Diretório de destino atualizado "
                "com sucesso."
            )
            continue

        print()
        print("Opção inválida.")


def exibir_menu_principal() -> None:
    """Exibe o menu principal."""
    print()
    print("MENU PRINCIPAL")
    print()
    print("1 - Atualizar agenda para um novo ano")
    print("2 - Configurações")
    print("0 - Sair")


def main() -> None:
    """Ponto de entrada da aplicação."""
    create_directories()

    config_service = ConfigService()
    config_app = config_service.carregar()

    aplicacao = AgendaApplication()

    logger.info("=" * 60)
    logger.info("Agenda Universal PRO iniciado.")
    logger.info("=" * 60)

    print()
    print("=" * 60)
    print("Agenda Universal PRO v1.0.0")
    print("=" * 60)

    while True:
        exibir_menu_principal()

        escolha = input(
            "\nEscolha uma opção: "
        ).strip()

        if escolha == "0":
            logger.info(
                "Agenda Universal PRO encerrado."
            )

            print()
            print("Aplicação encerrada.")
            break

        if escolha == "1":
            executar_atualizacao(
                aplicacao,
                config_app,
            )
            continue

        if escolha == "2":
            alterar_configuracoes(
                config_service,
                config_app,
            )
            continue

        print()
        print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        logger.exception("Erro durante a execução da aplicação.")
        print()
        print("ERRO DURANTE A EXECUÇÃO")
        print("-" * 60)
        print(str(exc))
        print("-" * 60)
