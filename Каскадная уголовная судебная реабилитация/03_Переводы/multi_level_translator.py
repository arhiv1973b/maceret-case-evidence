#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Многоуровневая система переводов с квантовой защитой
A©tor Quantum System - Цепочка переводов для детекции искажений
"""

import os
import sys
import json
import re
import hashlib
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import tempfile

# Импорт квантовой системы
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '07_Этические_маркеры'))
from quantum_auth_system import QuantumAuthSystem

@dataclass
class TranslationResult:
    """Результат перевода"""
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence: float
    quantum_hash: str
    auth_markers: List[str]
    distortion_detected: bool

class MultiLevelTranslationSystem:
    """Система многоуровневых переводов с квантовой защитой"""
    
    def __init__(self):
        self.quantum_auth = QuantumAuthSystem()
        self.translation_chain = []
        self.auth_markers = ["A©tor", "A©t0r"]
        
        # Цепочка языков для детекции искажений
        self.language_chain = [
            ("ron", "eng"),  # Румынский → Английский
            ("eng", "rus"),  # Английский → Русский  
            ("rus", "eng"),  # Русский → Английский
            ("eng", "ron")   # Английский → Румынский (для сравнения)
        ]
        
        # Юридически значимые термины для мониторинга
        self.legal_terms = {
            "ron": ["articolul", "codul", "penal", "procesual", "curtea", "judecătoriei", "procuror"],
            "eng": ["article", "code", "criminal", "procedural", "court", "prosecutor", "judge"],
            "rus": ["статья", "кодекс", "уголовный", "процессуальный", "суд", "прокурор", "судья"]
        }
    
    def simulate_translation(self, text: str, source_lang: str, target_lang: str) -> Tuple[str, float]:
        """Симуляция перевода с детекцией искажений"""
        
        # Базовый перевод (в реальной системе здесь был бы API вызов)
        translation_map = {
            ("ron", "eng"): {
                "Cerere de chemare în judecată": "Summons to court",
                "articolul": "article", 
                "codul penal": "criminal code",
                "procuror": "prosecutor",
                "judecător": "judge"
            },
            ("eng", "rus"): {
                "Summons to court": "Вызов в суд",
                "article": "статья",
                "criminal code": "уголовный кодекс", 
                "prosecutor": "прокурор",
                "judge": "судья"
            },
            ("rus", "eng"): {
                "Вызов в суд": "Summons to court",
                "статья": "article",
                "уголовный кодекс": "criminal code",
                "прокурор": "prosecutor", 
                "судья": "judge"
            },
            ("eng", "ron"): {
                "Summons to court": "Cerere de chemare în judecată",
                "article": "articolul",
                "criminal code": "codul penal",
                "prosecutor": "procuror",
                "judge": "judecător"
            }
        }
        
        translated = text
        confidence = 0.95
        
        # Применяем перевод
        for source_phrase, target_phrase in translation_map.get((source_lang, target_lang), {}).items():
            if source_phrase.lower() in translated.lower():
                translated = translated.replace(source_phrase, target_phrase)
                confidence *= 0.98  # Небольшое снижение уверенности при каждой замене
        
        # Детекция искажений юридических терминов
        legal_terms_source = self.legal_terms.get(source_lang, [])
        legal_terms_target = self.legal_terms.get(target_lang, [])
        
        for term in legal_terms_source:
            if term.lower() in text.lower():
                # Проверяем что термин правильно переведен
                found_correct_translation = any(
                    target_term.lower() in translated.lower() 
                    for target_term in legal_terms_target
                )
                if not found_correct_translation:
                    confidence *= 0.7  # Снижаем уверенность при потере юридических терминов
        
        return translated, confidence
    
    def apply_quantum_protection(self, text: str, stage: str) -> Tuple[str, str]:
        """Применение квантовой защиты к тексту"""
        
        # Создаем квантовый хеш
        timestamp = datetime.now().isoformat()
        content = f"{text}_{stage}_{timestamp}"
        quantum_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        
        # Добавляем маркеры защиты
        protected_text = f"{text}\n\n--- A©tor Quantum Protection ---\nStage: {stage}\nHash: {quantum_hash}\nTimestamp: {timestamp}"
        
        return protected_text, quantum_hash
    
    def detect_distortion(self, original: str, final: str) -> bool:
        """Детекция искажений в цепочке переводов"""
        
        # Извлекаем основной текст (без квантовых маркеров)
        def extract_main_text(text: str) -> str:
            lines = text.split('\n')
            main_lines = [line for line in lines if not line.startswith('---') and not line.startswith('Stage:') and not line.startswith('Hash:')]
            return '\n'.join(main_lines).strip()
        
        original_clean = extract_main_text(original)
        final_clean = extract_main_text(final)
        
        # Проверяем ключевые юридические термины
        original_terms = set()
        final_terms = set()
        
        for lang_terms in self.legal_terms.values():
            for term in lang_terms:
                if term.lower() in original_clean.lower():
                    original_terms.add(term.lower())
                if term.lower() in final_clean.lower():
                    final_terms.add(term.lower())
        
        # Детекция потери юридических терминов
        lost_terms = original_terms - final_terms
        if lost_terms:
            print(f"⚠️ Обнаружена потеря юридических терминов: {lost_terms}")
            return True
        
        # Проверка структурных изменений
        original_words = len(original_clean.split())
        final_words = len(final_clean.split())
        
        if abs(original_words - final_words) / original_words > 0.3:  # 30% изменение длины
            print("⚠️ Обнаружено значительное изменение длины текста")
            return True
        
        return False
    
    def process_translation_chain(self, original_text: str, source_language: str = "ron") -> Dict:
        """Обработка полной цепочки переводов"""
        
        print(f"🔄 Запуск цепочки переводов для текста на {source_language}")
        print(f"📝 Длина текста: {len(original_text)} символов")
        
        results = []
        current_text = original_text
        current_lang = source_language
        
        # Применяем начальную квантовую защиту
        protected_text, initial_hash = self.apply_quantum_protection(current_text, "original")
        
        for i, (src_lang, target_lang) in enumerate(self.language_chain):
            if current_lang != src_lang:
                continue
                
            print(f"🔄 Шаг {i+1}: {src_lang} → {target_lang}")
            
            # Выполняем перевод
            translated, confidence = self.simulate_translation(current_text, src_lang, target_lang)
            
            # Применяем квантовую защиту
            protected_translated, quantum_hash = self.apply_quantum_protection(translated, f"step_{i+1}")
            
            # Проверяем квантовую целостность
            quantum_verified = self.quantum_auth._verify_quantum_integrity(protected_translated)
            
            # Сохраняем результат
            result = TranslationResult(
                original_text=current_text,
                translated_text=translated,
                source_language=src_lang,
                target_language=target_lang,
                confidence=confidence,
                quantum_hash=quantum_hash,
                auth_markers=self.auth_markers.copy(),
                distortion_detected=False
            )
            
            results.append(result)
            current_text = translated
            current_lang = target_lang
            
            print(f"✅ Уверенность перевода: {confidence:.3f}")
            print(f"🛡️ Квантовая верификация: {'Пройдена' if quantum_verified else 'Не пройдена'}")
        
        # Финальная детекция искажений
        final_text = results[-1].translated_text if results else current_text
        distortion_detected = self.detect_distortion(original_text, final_text)
        
        # Обновляем последний результат
        if results:
            results[-1].distortion_detected = distortion_detected
        
        # Генерируем отчет
        report = {
            "translation_chain_summary": {
                "total_steps": len(results),
                "source_language": source_language,
                "final_language": current_lang,
                "original_length": len(original_text),
                "final_length": len(final_text),
                "distortion_detected": distortion_detected,
                "quantum_protection": True
            },
            "step_by_step_results": [
                {
                    "step": i + 1,
                    "source_lang": result.source_language,
                    "target_lang": result.target_language,
                    "confidence": result.confidence,
                    "quantum_hash": result.quantum_hash,
                    "text_length": len(result.translated_text)
                }
                for i, result in enumerate(results)
            ],
            "auth_markers_used": self.auth_markers,
            "processing_timestamp": datetime.now().isoformat(),
            "final_assessment": {
                "integrity_preserved": not distortion_detected,
                "average_confidence": sum(r.confidence for r in results) / len(results) if results else 0,
                "quantum_verified": all(self.quantum_auth._verify_quantum_integrity(r.translated_text) for r in results)
            }
        }
        
        return report
    
    def save_translation_results(self, report: Dict, filename: str = None):
        """Сохранение результатов переводов"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"translation_chain_{timestamp}.json"
        
        output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "03_Переводы", filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Результаты сохранены: {output_path}")
        return output_path

def main():
    """Основная функция"""
    
    print("🌐 Запуск Multi-Level Translation System...")
    print("🛡️ A©tor Quantum Protection Enabled")
    
    # Создаем систему переводов
    translation_system = MultiLevelTranslationSystem()
    
    # Тестовый текст (в реальной системе здесь был бы текст из OCR)
    test_text = "Cerere de chemare în judecată conform articolul 22 din codul penal. Procurorul a prezentat acuzațiile în fața judecătorului."
    
    print(f"📝 Тестовый текст: {test_text}")
    
    # Обрабатываем цепочку переводов
    report = translation_system.process_translation_chain(test_text, "ron")
    
    # Выводим отчет
    print("\n📊 Отчет цепочки переводов:")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    
    # Сохраняем результаты
    translation_system.save_translation_results(report)
    
    print("\n🔚 Multi-Level Translation System готова к работе")

if __name__ == "__main__":
    main()