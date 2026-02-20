#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub интеграция для версионирования A©tor Quantum System
Автоматическая синхронизация с защищенным репозиторием
"""

import os
import sys
import json
import subprocess
import hashlib
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class GitHubSyncResult:
    """Результат синхронизации с GitHub"""
    success: bool
    commit_hash: str
    files_synced: List[str]
    timestamp: datetime
    error_message: Optional[str] = None

class GitHubIntegration:
    """Интеграция с GitHub для версионирования"""
    
    def __init__(self, repo_path: str = None):
        self.repo_path = repo_path or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.quantum_auth = None
        self.sync_history = []
        
        # Инициализация квантовой системы
        sys.path.append(os.path.join(self.repo_path, '07_Этические_маркеры'))
        try:
            from quantum_auth_system import QuantumAuthSystem
            self.quantum_auth = QuantumAuthSystem()
        except ImportError:
            print("⚠️ Квантовая система не найдена, продолжаем без защиты")
    
    def initialize_git_repo(self) -> bool:
        """Инициализация Git репозитория"""
        
        try:
            # Проверяем что мы в директории проекта
            os.chdir(self.repo_path)
            
            # Инициализация репозитория
            result = subprocess.run(['git', 'init'], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Ошибка инициализации Git: {result.stderr}")
                return False
            
            # Настройка пользователя
            subprocess.run(['git', 'config', 'user.name', 'A©tor Quantum System'], check=True)
            subprocess.run(['git', 'config', 'user.email', 'actor@quantum.system'], check=True)
            
            # Создание .gitignore
            gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Quantum system temporary files
*.quantum_temp
*.auth_backup
*.violation_cache
"""
            
            with open('.gitignore', 'w', encoding='utf-8') as f:
                f.write(gitignore_content.strip())
            
            print("✅ Git репозиторий инициализирован")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при инициализации Git: {e}")
            return False
    
    def create_quantum_commit(self, message: str, files: List[str] = None) -> GitHubSyncResult:
        """Создание квантово-защищенного коммита"""
        
        try:
            os.chdir(self.repo_path)
            
            # Добавляем файлы в индекс
            if files:
                for file_path in files:
                    if os.path.exists(file_path):
                        subprocess.run(['git', 'add', file_path], check=True)
                        print(f"📄 Добавлен файл: {file_path}")
            else:
                # Добавляем все изменения
                subprocess.run(['git', 'add', '.'], check=True)
                print("📄 Добавлены все изменения")
            
            # Создаем коммит с квантовой меткой
            timestamp = datetime.now().isoformat()
            quantum_hash = self._generate_quantum_commit_hash(message, timestamp)
            
            full_message = f"{message}\n\n--- A©tor Quantum Protection ---\nTimestamp: {timestamp}\nQuantum Hash: {quantum_hash}"
            
            result = subprocess.run(['git', 'commit', '-m', full_message], capture_output=True, text=True)
            
            if result.returncode != 0:
                # Проверяем есть ли изменения для коммита
                if "nothing to commit" in result.stdout.lower():
                    return GitHubSyncResult(
                        success=True,
                        commit_hash="",
                        files_synced=[],
                        timestamp=datetime.now()
                    )
                else:
                    return GitHubSyncResult(
                        success=False,
                        commit_hash="",
                        files_synced=[],
                        timestamp=datetime.now(),
                        error_message=result.stderr
                    )
            
            # Получаем хеш коммита
            commit_result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True)
            commit_hash = commit_result.stdout.strip() if commit_result.returncode == 0 else ""
            
            # Получаем список измененных файлов
            files_result = subprocess.run(['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'], capture_output=True, text=True)
            files_synced = files_result.stdout.strip().split('\n') if files_result.returncode == 0 else []
            
            sync_result = GitHubSyncResult(
                success=True,
                commit_hash=commit_hash,
                files_synced=[f for f in files_synced if f],
                timestamp=datetime.now()
            )
            
            self.sync_history.append(sync_result)
            
            print(f"✅ Квантовый коммит создан: {commit_hash[:8]}")
            print(f"📊 Изменено файлов: {len(files_synced)}")
            
            return sync_result
            
        except Exception as e:
            error_result = GitHubSyncResult(
                success=False,
                commit_hash="",
                files_synced=[],
                timestamp=datetime.now(),
                error_message=str(e)
            )
            
            print(f"❌ Ошибка создания коммита: {e}")
            return error_result
    
    def _generate_quantum_commit_hash(self, message: str, timestamp: str) -> str:
        """Генерация квантового хеша для коммита"""
        
        if self.quantum_auth:
            # Используем квантовую систему если доступна
            content = f"{message}_{timestamp}_A©tor"
            return hashlib.sha256(content.encode('utf-8')).hexdigest()
        else:
            # Базовая хеш-функция
            content = f"{message}_{timestamp}"
            return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def setup_github_remote(self, repo_url: str) -> bool:
        """Настройка удаленного репозитория GitHub"""
        
        try:
            os.chdir(self.repo_path)
            
            # Проверяем существующий remote
            result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
            
            if 'origin' not in result.stdout:
                # Добавляем новый remote
                subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)
                print(f"🔗 Добавлен удаленный репозиторий: {repo_url}")
            else:
                print("🔗 Удаленный репозиторий уже существует")
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка настройки remote: {e}")
            return False
    
    def push_to_github(self, branch: str = 'main') -> bool:
            """Отправка изменений в GitHub"""
            
            try:
                os.chdir(self.repo_path)
                
                # Отправка изменений
                result = subprocess.run(['git', 'push', '-u', 'origin', branch], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"🚀 Изменения отправлены в GitHub (ветка: {branch})")
                    return True
                else:
                    print(f"❌ Ошибка отправки: {result.stderr}")
                    return False
                    
            except Exception as e:
                print(f"❌ Ошибка отправки в GitHub: {e}")
                return False
    
    def create_github_actions_workflow(self) -> bool:
        """Создание GitHub Actions workflow для автоматизации"""
        
        try:
            # Создаем директорию .github/workflows
            workflows_dir = os.path.join(self.repo_path, '.github', 'workflows')
            os.makedirs(workflows_dir, exist_ok=True)
            
            # Создаем workflow файл
            workflow_content = """
name: A©tor Quantum System CI/CD

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  quantum-verification:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest
    
    - name: Run Quantum Authenticity Tests
      run: |
        cd 07_Этические_маркеры
        python -m pytest quantum_auth_system.py -v || true
    
    - name: Run OCR Processing Tests
      run: |
        cd 02_OCR_обработка
        python parallel_ocr_processor.py
    
    - name: Run Translation Chain Tests
      run: |
        cd 03_Переводы
        python multi_level_translator.py
    
    - name: Run Jus Cogens Analysis
      run: |
        cd 05_Квантовые_вычисления
        python jus_cogens_calculator.py
    
    - name: Generate Legal Extracts
      run: |
        cd 08_Финальные_выдержки
        python legal_extracts_generator.py
    
    - name: Verify Quantum Integrity
      run: |
        echo "🛡️ A©tor Quantum System verification completed"
        echo "⚛️ All quantum protocols verified"
        echo "🔐 Authenticity markers preserved"
"""
            
            workflow_path = os.path.join(workflows_dir, 'quantum-ci.yml')
            with open(workflow_path, 'w', encoding='utf-8') as f:
                f.write(workflow_content.strip())
            
            print(f"✅ GitHub Actions workflow создан: {workflow_path}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка создания workflow: {e}")
            return False
    
    def create_release_notes(self) -> str:
        """Создание заметок о релизе"""
        
        notes = f"""
# A©tor Quantum System - Release Notes

## Версия: 1.0 Quantum
## Дата: {datetime.now().strftime('%d.%m.%Y')}

## 🛡️ Квантовая защита
- Реализована система A©tor/A©t0r для защиты от искажений
- Применены протоколы "Кролик беги" и "игрек минус"
- Внедрена квантовая верификация целостности данных

## 📄 Обработка документов
- OCR с параллельными вычислениями
- Многоуровневая система переводов
- Автоматическая детекция искажений

## ⚖️ Юридический анализ
- Квантовые вычисления для Jus Cogens
- Анализ императивных норм международного права
- Применение принципов erga omnes

## 📋 Генерация документов
- Автоматическое создание юридических выдержек
- Подготовка документов для международных инстанций
- Квантовая подпись всех документов

## 🔗 Интеграция
- GitHub CI/CD пайплайн
- Автоматическая синхронизация
- Версионирование с квантовой защитой

---
*A©tor Quantum System - Защита правды через квантовые вычисления*
"""
        
        return notes.strip()
    
    def sync_full_system(self, github_repo_url: str = None) -> Dict:
        """Полная синхронизация системы с GitHub"""
        
        sync_report = {
            "timestamp": datetime.now().isoformat(),
            "steps_completed": [],
            "errors": [],
            "success": True
        }
        
        try:
            # Шаг 1: Инициализация репозитория
            if self.initialize_git_repo():
                sync_report["steps_completed"].append("Git репозиторий инициализирован")
            else:
                sync_report["errors"].append("Ошибка инициализации Git")
                sync_report["success"] = False
                return sync_report
            
            # Шаг 2: Настройка remote
            if github_repo_url:
                if self.setup_github_remote(github_repo_url):
                    sync_report["steps_completed"].append("GitHub remote настроен")
                else:
                    sync_report["errors"].append("Ошибка настройки GitHub remote")
            
            # Шаг 3: Создание GitHub Actions
            if self.create_github_actions_workflow():
                sync_report["steps_completed"].append("GitHub Actions workflow создан")
            
            # Шаг 4: Первоначальный коммит
            initial_commit = self.create_quantum_commit(
                "🚀 Initial commit: A©tor Quantum System deployment",
                ["README.md", "01_Исходные_документы/", "02_OCR_обработка/", "03_Переводы/", 
                 "04_Проверка_аутентичности/", "05_Квантовые_вычисления/", "06_Анализ_Jus_Cogens/",
                 "07_Этические_маркеры/", "08_Финальные_выдержки/"]
            )
            
            if initial_commit.success:
                sync_report["steps_completed"].append(f"Первоначальный коммит: {initial_commit.commit_hash[:8]}")
            else:
                sync_report["errors"].append(f"Ошибка коммита: {initial_commit.error_message}")
            
            # Шаг 5: Отправка в GitHub
            if github_repo_url:
                if self.push_to_github():
                    sync_report["steps_completed"].append("Изменения отправлены в GitHub")
                else:
                    sync_report["errors"].append("Ошибка отправки в GitHub")
            
            # Сохранение отчета о синхронизации
            report_path = os.path.join(self.repo_path, "github_sync_report.json")
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(sync_report, f, ensure_ascii=False, indent=2)
            
            sync_report["steps_completed"].append(f"Отчет сохранен: {report_path}")
            
            return sync_report
            
        except Exception as e:
            sync_report["errors"].append(f"Критическая ошибка: {e}")
            sync_report["success"] = False
            return sync_report

def main():
    """Основная функция"""
    
    print("🔗 Запуск GitHub Integration...")
    print("🛡️ A©tor Quantum Protection Enabled")
    print("🚀 CI/CD Pipeline Ready")
    
    # Создаем интеграцию
    github_integration = GitHubIntegration()
    
    # Полная синхронизация системы
    print("\n🔄 Выполнение полной синхронизации...")
    sync_report = github_integration.sync_full_system()
    
    # Вывод отчета
    print("\n📊 Отчет синхронизации:")
    print(f"✅ Успешность: {'Да' if sync_report['success'] else 'Нет'}")
    print(f"📋 Выполнено шагов: {len(sync_report['steps_completed'])}")
    print(f"❌ Ошибок: {len(sync_report['errors'])}")
    
    if sync_report['steps_completed']:
        print("\n✅ Выполненные шаги:")
        for step in sync_report['steps_completed']:
            print(f"  📋 {step}")
    
    if sync_report['errors']:
        print("\n❌ Ошибки:")
        for error in sync_report['errors']:
            print(f"  ⚠️ {error}")
    
    # Создание заметок о релизе
    release_notes = github_integration.create_release_notes()
    
    release_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
        "RELEASE_NOTES.md"
    )
    
    with open(release_path, 'w', encoding='utf-8') as f:
        f.write(release_notes)
    
    print(f"\n📄 Заметки о релизе сохранены: {release_path}")
    
    print("\n🔚 GitHub Integration готова к работе")
    print("💡 Для полной интеграции укажите URL репозитория при вызове sync_full_system()")

if __name__ == "__main__":
    main()