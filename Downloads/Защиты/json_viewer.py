#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON Viewer for combined_pdf_summaries.json
Allows searching and viewing PDF data from the consolidated JSON.
"""

import json
import os
from pathlib import Path
from pdf2image import convert_from_path
import pytesseract


def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: file '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error reading JSON from file '{file_path}': {e}")
        return None


def extract_text_with_fallback(pdf_path: str, lang: str = "rus+ron") -> str:
    """
    Извлекает текст из PDF. Если текстовый слой отсутствует (0 символов),
    запускает OCR через pytesseract.
    """
    text = extract_text_standard(pdf_path)
    if len(text.strip()) == 0:
        print(
            f"⚠ PDF '{os.path.basename(pdf_path)}' содержит только изображения. Запуск OCR..."
        )
        try:
            pages = convert_from_path(pdf_path)
            ocr_text = ""
            for page in pages:
                ocr_text += pytesseract.image_to_string(page, lang=lang) + "\n"
            return ocr_text.strip()
        except Exception as e:
            print(f"❌ Ошибка OCR: {e}")
            return ""
    return text


def extract_text_standard(pdf_path: str) -> str:
    """
    Текущий метод извлечения текста (через pdfplumber).
    """
    try:
        import pdfplumber

        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"❌ Ошибка стандартного извлечения: {e}")
        return ""


def search_pdfs(data, query):
    results = {}
    query_lower = query.lower()
    for pdf_name, info in data.items():
        if (
            query_lower in pdf_name.lower()
            or query_lower in info.get("raw_text", "").lower()
            or query_lower in info.get("cleaned_text", "").lower()
        ):
            results[pdf_name] = info
    return results


def get_pdf_from_user(data, lang="en"):
    prompt = (
        "Enter PDF number or name: "
        if lang == "en"
        else "Введите номер или имя PDF: "
        if lang == "ru"
        else "Introduceți numărul sau numele PDF-ului: "
    )
    invalid_num = (
        "Invalid number."
        if lang == "en"
        else "Неверный номер."
        if lang == "ru"
        else "Număr invalid."
    )
    not_found = (
        "PDF not found."
        if lang == "en"
        else "PDF не найден."
        if lang == "ru"
        else "PDF nu a fost găsit."
    )
    choice = input(prompt).strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(data):
            pdf_name = list(data.keys())[idx]
            return pdf_name, data[pdf_name]
        else:
            print(invalid_num)
            return None, None
    else:
        if choice in data:
            return choice, data[choice]
        print(not_found)
        return None, None


def display_pdf_info(pdf_name, info):
    raw_text = info.get("raw_text", "")
    if not raw_text.strip():
        pdf_path = info.get("pdf_path", "")
        if pdf_path:
            raw_text = extract_text_with_fallback(pdf_path)
    print(f"\n=== {pdf_name} ===")
    print(f"Path: {info.get('pdf_path', 'N/A')}")
    print(f"Raw text length: {len(raw_text)} chars")
    print(f"Cleaned text length: {len(info.get('cleaned_text', ''))} chars")
    print(f"Russian summary: {len(info.get('summary_ru', []))} items")
    print(f"Romanian summary: {len(info.get('summary_ro', []))} items")
    print(f"Translations: {len(info.get('translations', {}))} items")
    print("Raw text (first 500 chars):")
    print(raw_text[:500] + "...")
    print("Cleaned text (first 500 chars):")
    print(info.get("cleaned_text", "")[:500] + "...")
    print("Russian summary:")
    for i, s in enumerate(info.get("summary_ru", []), 1):
        print(f"  {i}. {s}")
    print("Romanian summary:")
    for i, s in enumerate(info.get("summary_ro", []), 1):
        print(f"  {i}. {s}")


def main():
    lang = (
        input("Choose language / Выберите язык / Alegeți limba (en/ru/ro): ")
        .strip()
        .lower()
    )
    if lang not in ["en", "ru", "ro"]:
        lang = "en"

    print("Установка зависимостей: pip install pytesseract pdf2image pdfplumber")
    print("Установите Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki")

    json_path = Path(__file__).parent / "combined_pdf_summaries.json"
    if not json_path.exists():
        msg = (
            f"JSON file not found at {json_path}. Please specify path."
            if lang == "en"
            else f"Файл JSON не найден в {json_path}. Укажите путь."
            if lang == "ru"
            else f"Fișierul JSON nu a fost găsit în {json_path}. Specificați calea."
        )
        print(msg)
        prompt = (
            "Enter JSON file path: "
            if lang == "en"
            else "Введите путь к файлу JSON: "
            if lang == "ru"
            else "Introduceți calea fișierului JSON: "
        )
        json_path = input(prompt)
        json_path = Path(json_path)

    data = load_json(json_path)
    if data is None:
        return

    msg_loaded = (
        f"Loaded data for {len(data)} PDFs."
        if lang == "en"
        else f"Загружены данные для {len(data)} PDF."
    )
    print(msg_loaded)

    while True:
        if lang == "en":
            print("\nCommands:")
            print("1. List all PDFs")
            print("2. Search PDFs by query")
            print("3. View PDF details")
            print("4. Export PDF text to file")
            print("5. Exit")
            choice_prompt = "Choose: "
        elif lang == "ru":
            print("\nКоманды:")
            print("1. Перечислить все PDF")
            print("2. Искать PDF по запросу")
            print("3. Просмотреть детали PDF")
            print("4. Экспортировать текст PDF в файл")
            print("5. Выход")
            choice_prompt = "Выберите: "
        else:  # ro
            print("\nComenzi:")
            print("1. Listați toate PDF-urile")
            print("2. Căutați PDF după interogare")
            print("3. Vizualizați detaliile PDF")
            print("4. Exportați textul PDF în fișier")
            print("5. Ieșire")
            choice_prompt = "Alegeți: "

        choice = input(choice_prompt).strip()

        if choice == "1":
            for i, pdf in enumerate(data.keys(), 1):
                print(f"{i}. {pdf}")

        elif choice == "2":
            query_prompt = (
                "Enter search query: "
                if lang == "en"
                else "Введите поисковый запрос: "
                if lang == "ru"
                else "Introduceți interogarea de căutare: "
            )
            no_matches = (
                "No matches found."
                if lang == "en"
                else "Совпадений не найдено."
                if lang == "ru"
                else "Nu s-au găsit potriviri."
            )
            query = input(query_prompt).strip()
            results = search_pdfs(data, query)
            if results:
                found_msg = (
                    f"Found {len(results)} matches:"
                    if lang == "en"
                    else f"Найдено {len(results)} совпадений:"
                    if lang == "ru"
                    else f"Găsite {len(results)} potriviri:"
                )
                print(found_msg)
                for pdf in results.keys():
                    print(f"  - {pdf}")
            else:
                print(no_matches)

        elif choice == "3":
            pdf_name, pdf_info = get_pdf_from_user(data, lang)
            if pdf_name:
                display_pdf_info(pdf_name, pdf_info)

        elif choice == "4":
            pdf_name, pdf_info = get_pdf_from_user(data, lang)
            if pdf_name:
                # Normalize filename and save to 'exports' directory
                output_dir = Path("exports")
                output_dir.mkdir(parents=True, exist_ok=True)
                safe_filename = Path(pdf_name).name
                output_file = output_dir / Path(safe_filename).with_suffix(".txt")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(pdf_info.get("cleaned_text", ""))
                exported_msg = (
                    f"Exported to {output_file}"
                    if lang == "en"
                    else f"Экспортировано в {output_file}"
                    if lang == "ru"
                    else f"Exportat în {output_file}"
                )
                print(exported_msg)

        elif choice == "5":
            break

        else:
            invalid_msg = (
                "Invalid choice."
                if lang == "en"
                else "Неверный выбор."
                if lang == "ru"
                else "Alegere invalidă."
            )
            print(invalid_msg)


if __name__ == "__main__":
    main()
