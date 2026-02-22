#!/usr/bin/env python3
"""
Jus Cogens Project Integrity Checker
Prevents deployment if any links in index.html are broken
"""

import os
import re
import sys

def check_integrity():
    print("=" * 60)
    print("🔍 АУДИТ ЦЕЛОСТНОСТИ ПРОЕКТА")
    print("=" * 60)
    
    # Read index.html
    if not os.path.exists('index.html'):
        print("❌ ОШИБКА: index.html не найден!")
        return False
    
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Find all local href links (not http, not #, not //)
    links = re.findall(r'href="([^"http#][^"]+)"', html)
    
    # Add onclick links that reference files
    onclick_links = re.findall(r'onclick="[^"]*open\([\'"]([^\'"]+)[\'"]\)', html)
    
    all_links = list(set(links + onclick_links))
    
    errors = 0
    print(f"\n📋 Проверяем {len(all_links)} ссылок...\n")
    
    for link in all_links:
        # Skip external URLs
        if link.startswith('http') or link.startswith('//') or link.startswith('#'):
            continue
            
        # Clean the link
        clean_link = link.split('#')[0]
        
        # Skip JS function calls and template strings
        if '(' in clean_link or clean_link.startswith('function') or '+' in clean_link or 'pdfName' in clean_link:
            continue
            
        if not os.path.exists(clean_link):
            print(f"❌ БИТАЯ ССЫЛКА: {clean_link}")
            errors += 1
        else:
            print(f"✅ {clean_link}")
    
    print("\n" + "=" * 60)
    
    if errors > 0:
        print(f"❌ НАЙДЕНО ОШИБОК: {errors}")
        print("⛔ ДЕПЛОЙ ЗАБЛОКИРОВАН!")
        print("=" * 60)
        return False
    else:
        print("✅ ВСЕ ССЫЛКИ ЦЕЛЫ!")
        print("🚀 ДЕПЛОЙ РАЗРЕШЁН")
        print("=" * 60)
        return True

if __name__ == "__main__":
    success = check_integrity()
    sys.exit(0 if success else 1)
