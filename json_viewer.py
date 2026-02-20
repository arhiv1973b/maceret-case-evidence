#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON Viewer for combined_pdf_summaries.json
Allows searching and viewing PDF data from the consolidated JSON.
"""

import json
from pathlib import Path

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: file '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error reading JSON from file '{file_path}': {e}")
        return None

def search_pdfs(data, query):
    results = {}
    query_lower = query.lower()
    for pdf_name, info in data.items():
        if query_lower in pdf_name.lower() or query_lower in info.get('raw_text', '').lower() or query_lower in info.get('cleaned_text', '').lower():
            results[pdf_name] = info
    return results

def get_pdf_from_user(data):
    pdf_name = input("Enter PDF name: ").strip()
    if pdf_name in data:
        return pdf_name, data[pdf_name]
    print("PDF not found.")
    return None, None

def display_pdf_info(pdf_name, info):
    print(f"\n=== {pdf_name} ===")
    print(f"Path: {info.get('pdf_path', 'N/A')}")
    print(f"Raw text length: {len(info.get('raw_text', ''))} chars")
    print(f"Cleaned text length: {len(info.get('cleaned_text', ''))} chars")
    print(f"Russian summary: {len(info.get('summary_ru', []))} items")
    print(f"Romanian summary: {len(info.get('summary_ro', []))} items")
    print(f"Translations: {len(info.get('translations', {}))} items")
    print("Raw text (first 500 chars):")
    print(info.get('raw_text', '')[:500] + "...")
    print("Cleaned text (first 500 chars):")
    print(info.get('cleaned_text', '')[:500] + "...")
    print("Russian summary:")
    for i, s in enumerate(info.get('summary_ru', []), 1):
        print(f"  {i}. {s}")
    print("Romanian summary:")
    for i, s in enumerate(info.get('summary_ro', []), 1):
        print(f"  {i}. {s}")

def main():
    json_path = Path(__file__).parent / "combined_pdf_summaries.json"
    if not json_path.exists():
        print(f"JSON file not found at {json_path}. Please specify path.")
        json_path = input("Enter JSON file path: ")
        json_path = Path(json_path)
    
    data = load_json(json_path)
    if data is None:
        return
    
    print(f"Loaded data for {len(data)} PDFs.")
    
    while True:
        print("\nCommands:")
        print("1. List all PDFs")
        print("2. Search PDFs by query")
        print("3. View PDF details")
        print("4. Export PDF text to file")
        print("5. Exit")
        
        choice = input("Choose: ").strip()
        
        if choice == '1':
            for i, pdf in enumerate(data.keys(), 1):
                print(f"{i}. {pdf}")
        
        elif choice == '2':
            query = input("Enter search query: ").strip()
            results = search_pdfs(data, query)
            if results:
                print(f"Found {len(results)} matches:")
                for pdf in results.keys():
                    print(f"  - {pdf}")
            else:
                print("No matches found.")
        
        elif choice == '3':
            pdf_name, pdf_info = get_pdf_from_user(data)
            if pdf_name:
                display_pdf_info(pdf_name, pdf_info)

        elif choice == '4':
            pdf_name, pdf_info = get_pdf_from_user(data)
            if pdf_name:
                # Normalize filename and save to 'exports' directory
                output_dir = Path("exports")
                output_dir.mkdir(parents=True, exist_ok=True)
                safe_filename = Path(pdf_name).name
                output_file = output_dir / Path(safe_filename).with_suffix('.txt')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(pdf_info.get('cleaned_text', ''))
                print(f"Exported to {output_file}")
        
        elif choice == '5':
            break
        
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()