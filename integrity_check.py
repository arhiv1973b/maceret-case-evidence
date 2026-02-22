#!/usr/bin/env python3
"""
Jus Cogens Project - Full Project Auditor
Checks HTML syntax, JS functions, and file links
"""

import os
import re
import sys
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
    
    print("\n--- 1. Сбор объявленных функций JS ---")
    patterns = [
        r'function\s+(\w+)\s*\(',
        r'(?:const|let|var)\s+(\w+)\s*=\s*(?:function|\()',
        r'async\s+function\s+(\w+)\s*\('
    ]
    for p in patterns:
        funcs = re.findall(p, content)
        auditor.defined_functions.update(funcs)
    
    print(f"✅ Найдено функций в коде: {len(auditor.defined_functions)}")
    for f in sorted(auditor.defined_functions):
        print(f"   - {f}()")

    print("\n--- 2. Аудит HTML и JS-связей ---")
    auditor.feed(content)
    
    err_count = 0
    
    if auditor.tag_stack:
        print(f"❌ ОШИБКА: Не закрыты теги: {auditor.tag_stack}")
        err_count += 1

    # Known safe JS methods that aren't defined as functions
    safe_methods = {'open', 'alert', 'log', 'preventDefault', 'stopPropagation', 
                   'getElementById', 'querySelector', 'getAttribute', 'addEventListener',
                   'setAttribute', 'classList', 'push', 'filter', 'map', 'forEach',
                   'includes', 'indexOf', 'toUpperCase', 'toLowerCase', 'trim', 'split'}

    for func, line in auditor.called_functions:
        if func not in auditor.defined_functions and func not in safe_methods:
            print(f"❌ ОШИБКА: Строка {line}: Вызвана несуществующая функция '{func}()'")
            err_count += 1
        elif func in auditor.defined_functions:
            print(f"✅ JS: {func}()")

    print("\n--- 3. Проверка файловых ссылок ---")
    links = re.findall(r'href="([^"http#][^"]+)"', content)
    broken = 0
    for link in set(links):
        # Skip JS template strings
        if '+' in link or 'pdfName' in link or 'code' in link or "'" in link:
            continue
        if not os.path.exists(link.replace('%20', ' ')):
            print(f"❌ БИТАЯ: {link}")
            broken += 1
            err_count += 1
        else:
            print(f"✅ {link}")
    
    print("\n" + "=" * 60)
    if err_count > 0:
        print(f"❌ ИТОГ: {err_count} критических ошибок")
        print("🛑 ДЕПЛОЙ ЗАБЛОКИРОВАН!")
        print("=" * 60)
        sys.exit(1)
    else:
        print("✅ ПОЛНЫЙ АУДИТ ПРОЙДЕН!")
        print("🚀 ДЕПЛОЙ РАЗРЕШЁН!")
        print("=" * 60)
        sys.exit(0)

if __name__ == "__main__":
    check_project()
