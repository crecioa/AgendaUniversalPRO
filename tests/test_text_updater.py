"""
Agenda Universal PRO
Arquivo: tests/test_text_updater.py

Teste do serviço TextUpdater.
"""

from pathlib import Path

from services.word_service import WordService
from services.text_updater import TextUpdater


def main() -> None:
    arquivo = Path("modelos") / "teste_text_updater.docx"

    word_service = WordService()
    documento = word_service.abrir_documento(arquivo)

    text_updater = TextUpdater()
    ocorrencias = text_updater.localizar_datas(documento)

    print("\n=== DATAS ENCONTRADAS ===\n")

    for indice, texto, datas in ocorrencias:
        print(f"Parágrafo {indice}:")
        print(f"Texto: {texto}")
        print(f"Datas: {', '.join(datas)}")
        print("-" * 50)

    print(f"\nTotal de parágrafos com datas: {len(ocorrencias)}")


if __name__ == "__main__":
    main()