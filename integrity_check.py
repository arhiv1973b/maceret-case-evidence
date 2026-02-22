#!/usr/bin/env python3
"""
Jus Cogens Project - Full Project Auditor with Self-Healing
Checks HTML syntax, JS functions, file links, and can auto-fix issues
"""

import os
import re
import sys
import shutil
from difflib import get_close_matches
from html.parser import HTMLParser

class FullProjectAuditor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
        self.tag_stack = []
        self.defined_functions = set()
        self.called_functions = []

    def handle_starttag(self, tag, attrs):
        if tag not in ['img', 'br', 'hr', 'input', 'link', 'meta', 'area', 'base', 'col', 'embed', 'param', 'source', 'track', 'wbr']:
            self.tag_stack.append(tag)
        
        for attr, value in attrs:
            if attr == 'onclick':
                match = re.search(r'(\w+)\s*\(', value)
                if match:
                    self.called_functions.append((match.group(1), self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag not in ['img', 'br', 'hr', 'input', 'link', 'meta', 'area', 'base', 'col', 'embed', 'param', 'source', 'track', 'wbr']:
            if self.tag_stack and self.tag_stack[-1] == tag:
                self.tag_stack.pop()

def create_backup(filename):
    backup_name = f"{filename}.bak"
    try:
        shutil.copy2(filename, backup_name)
        print(f"📦 Бэкап: {backup_name}")
        return True
    except Exception as e:
        print(f"⚠️ Ошибка бэкапа: {e}")
        return False

def auto_fix_project():
    html_file = 'index.html'
    if not os.path.exists(html_file):
        print("❌ index.html не найден!")
        return False

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print("\n--- 🛠 РЕЖИМ АВТО-ИСПРАВЛЕНИЯ ---")
    
    # Create backup first
    create_backup(html_file)
    
    # 1. Collect all files for fuzzy matching
    all_files = []
    for root, dirs, files in os.walk('.'):
        for f in files:
            if not f.endswith('.bak') and f != 'integrity_check.py':
                path = os.path.join(root, f).replace('./', '')
                all_files.append(path)

    # 2. Fix broken links
    def fix_links(match):
        link = match.group(1)
        # Skip external URLs and JS template strings
        if link.startswith(('http', 'https', '#')) or '+' in link or 'pdfName' in link:
            return match.group(0)
        
        if os.path.exists(link.replace('%20', ' ')):
            return match.group(0)
        
        # Try fuzzy match
        clean_link = link.replace('%20', ' ')
        matches = get_close_matches(clean_link, all_files, n=1, cutoff=0.7)
        if matches:
            print(f"🔧 Исправлено: {link} -> {matches[0]}")
            return f'href="{matches[0]}"'
        return match.group(0)

    new_content = re.sub(r'href="([^"]+)"', fix_links, content)

    # 3. Fix missing closing DIVs
    open_divs = new_content.count('<div')
    close_divs = new_content.count('</div>')
    if open_divs > close_divs:
        missing = open_divs - close_divs
        print(f"🔧 Добавлено {missing} закрывающих </div>")
        new_content += '</div>' * missing

    # 4. Save changes
    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ Изменения сохранены!")
        return True
    else:
        print("✅ Исправлений не требуется.")
        return False

def check_project():
    print("=" * 60)
    print("🔍 FULL PROJECT AUDIT - Jus Cogens Effect")
    print("=" * 60)
    
    html_file = 'index.html'
    if not os.path.exists(html_file):
        print("❌ index.html не найден!")
        sys.exit(1)

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    auditor = FullProjectAuditor()
    
    print("\n--- 1. Сбор JS функций ---")
    patterns = [
        r'function\s+(\w+)\s*\(',
        r'(?:const|let|var)\s+(\w+)\s*=\s*(?:function|\()',
        r'async\s+function\s+(\w+)\s*\('
    ]
    for p in patterns:
        funcs = re.findall(p, content)
        auditor.defined_functions.update(funcs)
    
    print(f"✅ Найдено функций: {len(auditor.defined_functions)}")

    print("\n--- 2. Аудит HTML/JS ---")
    auditor.feed(content)
    
    err_count = 0
    
    if auditor.tag_stack:
        print(f"❌ Не закрыты теги: {auditor.tag_stack}")
        err_count += 1

    safe_methods = {'open', 'alert', 'log', 'preventDefault', 'stopPropagation', 
                   'getElementById', 'querySelector', 'getAttribute', 'addEventListener',
                   'setAttribute', 'classList', 'push', 'filter', 'map', 'forEach',
                   'includes', 'indexOf', 'toUpperCase', 'toLowerCase', 'trim', 'split'}

    for func, line in auditor.called_functions:
        if func not in auditor.defined_functions and func not in safe_methods:
            print(f"❌ ОШИБКА: Строка {line}: Функция '{func}()' не найдена")
            err_count += 1
        elif func in auditor.defined_functions:
            print(f"✅ JS: {func}()")

    print("\n--- 3. Проверка ссылок ---")
    links = re.findall(r'href="([^"http#][^"]+)"', content)
    for link in set(links):
        if '+' in link or 'pdfName' in link or "'" in link:
            continue
        if not os.path.exists(link.replace('%20', ' ')):
            print(f"❌ БИТАЯ: {link}")
            err_count += 1
        else:
            print(f"✅ {link}")
    
    print("\n" + "=" * 60)
    if err_count > 0:
        print(f"❌ ИТОГ: {err_count} ошибок")
        print("🛑 ДЕПЛОЙ ЗАБЛОКИРОВАН!")
        print("\n💡 Запустите: python3 integrity_check.py --fix")
        print("=" * 60)
        sys.exit(1)
    else:
        print("✅ АУДИТ ПРОЙДЕН!")
        print("🚀 ДЕПЛОЙ РАЗРЕШЁН!")
        print("=" * 60)
        sys.exit(0)

if __name__ == "__main__":
    if "--fix" in sys.argv:
        auto_fix_project()
    else:
        check_project()
