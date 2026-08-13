"""
Agenda Universal PRO
Arquivo: tests/test_text_updater_update.py

Teste da atualização de datas pelo TextUpdater.
"""

from pathlib import Path

from services.text_updater import TextUpdater
from services.word_service import WordService


def main() -> None:
    arquivo = Path("modelos") / "teste_text_updater.docx"

    word_service = WordService()
    documento = word_service.abrir_documento(arquivo)

    text_updater = TextUpdater()

    substituicoes = {
        "05/01/2027": "05/01/2028",
        "10/02/2027": "10/02/2028",
        "15/03/2027": "15/03/2028",
    }

    quantidade = text_updater.atualizar_datas(
        documento,
        substituicoes,
    )

    print("\n=== TESTE DE ATUALIZAÇÃO DE DATAS ===\n")

    print(f"Substituições realizadas: {quantidade}")

    for paragrafo in documento.paragraphs:
        texto = paragrafo.text.strip()

        if texto:
            print(f"Texto: {texto}")

    print("\nTeste concluído.")


if __name__ == "__main__":
    main()