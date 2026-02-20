#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Система проверки аутентичности текстов
Каскадная уголовная судебная реабилитация
A©tor Quantum System - Многоуровневая проверка
"""

import os
import sys
import json
import hashlib
import difflib
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

# Импорт наших систем
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from quantum_auth_system import QuantumAuthSystem, JusCogensCalculator
from OCR_обработка.parallel_ocr_processor import ParallelOCRProcessor

@dataclass
class AuthenticityCheck:
    """Результат проверки аутентичности"""
    document_id: str
    original_text: str
    translated_text: str
    back_translated: str
    authenticity_score: float
    distortion_detected: bool
    quantum_verified: bool
    font_conversion_issues: List[str]
    timestamp: datetime

class AuthenticityVerifier:
    """Верификатор аутентичности текстов"""
    
    def __init__(self):
        self.auth_system = QuantumAuthSystem()
        self.ocr_processor = ParallelOCRProcessor()
        self.jus_calculator = JusCogensCalculator(self.auth_system)
        self.verification_history = []
        
        # Пороги оценки
        self.thresholds = {
            'minimum_authenticity': 0.7,
            'high_authenticity': 0.9,
            'critical_distortion': 0.3
        }
        
        # Языковые пары для проверки
        self.language_pairs = [
            ('ron', 'eng'),  # Румынский → Английский
            ('eng', 'rus'),  # Английский → Русский
            ('rus', 'eng'),  # Русский → Английский
        ]
    
    def verify_document_authenticity(self, file_path: str, source_language: str = 'ron') -> AuthenticityCheck:
        """Полная проверка аутентичности документа"""
        print(f"🔍 Начало проверки аутентичности: {file_path}")
        
        # Шаг 1: OCR обработка с защитой
        ocr_result = self.ocr_processor.process_document(file_path, source_language)
        original_text = ocr_result.original_text
        
        # Шаг 2: Создание базового маркера аутентичности
        marked_original = self.auth_system.create_auth_marker(original_text, 'A©tor')
        
        # Шаг 3: Цепочка переводов для проверки
        translation_chain = self._perform_translation_chain(original_text, source_language)
        
        # Шаг 4: Анализ искажений
        distortion_analysis = self._analyze_distortions(original_text, translation_chain)
        
        # Шаг 5: Проверка квантовой целостности
        quantum_check = self._verify_quantum_integrity(marked_original, translation_chain)
        
        # Шаг 6: Проверка конвертации шрифтов
        font_issues = self._check_font_conversion_issues(original_text)
        
        # Шаг 7: Расчет итоговой оценки аутентичности
        authenticity_score = self._calculate_authenticity_score(
            ocr_result, distortion_analysis, quantum_check, font_issues
        )
        
        # Создание результата
        result = AuthenticityCheck(
            document_id=self._generate_document_id(file_path),
            original_text=original_text,
            translated_text=translation_chain.get('final_translation', ''),
            back_translated=translation_chain.get('back_translation', ''),
            authenticity_score=authenticity_score,
            distortion_detected=distortion_analysis['distortion_detected'],
            quantum_verified=quantum_check['integrity_preserved'],
            font_conversion_issues=font_issues,
            timestamp=datetime.now()
        )
        
        # Сохранение в историю
        self.verification_history.append(result)
        
        return result
    
    def _perform_translation_chain(self, text: str, source_lang: str) -> Dict:
        """Выполнение цепочки переводов для проверки"""
        print("🔄 Выполнение цепочки переводов...")
        
        chain_result = {
            'original': text,
            'translations': {},
            'final_translation': '',
            'back_translation': '',
            'chain_integrity': True
        }
        
        current_text = text
        current_lang = source_lang
        
        # Цепочка переводов
        for lang_pair in self.language_pairs:
            if current_lang == lang_pair[0]:
                # Перевод
                translation_result = self.ocr_processor.translate_and_verify(
                    current_text, current_lang, lang_pair[1]
                )
                
                if translation_result['translation_confidence'] > 0.5:
                    # В реальной системе здесь был бы вызов API перевода
                    translated = self._simulate_translation(current_text, lang_pair[1])
                    chain_result['translations'][f"{current_lang}_{lang_pair[1]}"] = translated
                    current_text = translated
                    current_lang = lang_pair[1]
                else:
                    chain_result['chain_integrity'] = False
                    break
        
        # Обратный перевод для проверки
        if current_lang != source_lang:
            back_translation = self._simulate_translation(current_text, source_lang)
            chain_result['back_translation'] = back_translation
        
        chain_result['final_translation'] = current_text
        
        return chain_result
    
    def _simulate_translation(self, text: str, target_lang: str) -> str:
        """Симуляция перевода"""
        lang_names = {
            'ron': 'Romanian',
            'rus': 'Russian', 
            'eng': 'English'
        }
        
        return f"[{lang_names.get(target_lang, target_lang)} translation]: {text[:100]}..."
    
    def _analyze_distortions(self, original: str, translation_chain: Dict) -> Dict:
        """Анализ искажений в цепочке переводов"""
        print("🔍 Анализ искажений...")
        
        analysis = {
            'distortion_detected': False,
            'distortion_score': 0.0,
            'distortion_types': [],
            'critical_changes': []
        }
        
        back_translation = translation_chain.get('back_translation', '')
        
        if back_translation:
            # Сравнение оригинала с обратным переводом
            similarity = difflib.SequenceMatcher(None, original, back_translation).ratio()
            
            # Определение уровня искажения
            if similarity < 0.7:
                analysis['distortion_detected'] = True
                analysis['distortion_score'] = 1.0 - similarity
                analysis['distortion_types'].append('significant_meaning_change')
            
            # Поиск критических изменений
            original_words = set(original.lower().split())
            back_words = set(back_translation.lower().split())
            
            missing_words = original_words - back_words
            new_words = back_words - original_words
            
            # Проверка на юридически значимые термины
            legal_terms = {'суд', 'дело', 'закон', 'право', 'реабилитация', 'жалоба', 'прокурор'}
            
            critical_missing = missing_words.intersection(legal_terms)
            critical_new = new_words.intersection(legal_terms)
            
            if critical_missing or critical_new:
                analysis['distortion_detected'] = True
                analysis['critical_changes'].extend(list(critical_missing))
                analysis['critical_changes'].extend(list(critical_new))
                analysis['distortion_types'].append('legal_terms_altered')
        
        return analysis
    
    def _verify_quantum_integrity(self, marked_text: str, translation_chain: Dict) -> Dict:
        """Проверка квантовой целостности"""
        print("⚛️ Проверка квантовой целостности...")
        
        integrity_check = {
            'integrity_preserved': True,
            'marker_intact': True,
            'quantum_hash_valid': True,
            'parallel_computation_ok': True
        }
        
        # Проверка маркера в оригинале
        original_verification = self.auth_system.verify_authenticity(marked_text)
        integrity_check['marker_intact'] = original_verification['authentic']
        
        # Проверка целостности в цепочке переводов
        for step, translation in translation_chain.get('translations', {}).items():
            step_verification = self.auth_system.verify_authenticity(translation)
            if not step_verification['authentic']:
                integrity_check['integrity_preserved'] = False
                break
        
        # Проверка параллельных вычислений
        parallel_check = self.auth_system.parallel_computation_check(marked_text)
        integrity_check['parallel_computation_ok'] = parallel_check['parallel_integrity']
        
        # Общая оценка
        integrity_check['integrity_preserved'] = all([
            integrity_check['marker_intact'],
            integrity_check['quantum_hash_valid'],
            integrity_check['parallel_computation_ok']
        ])
        
        return integrity_check
    
    def _check_font_conversion_issues(self, text: str) -> List[str]:
        """Проверка проблем конвертации шрифтов"""
        issues = []
        
        # Проверка на проблемы с кириллицей
        try:
            text.encode('cp1251')
        except UnicodeEncodeError:
            issues.append('cyrillic_encoding_issue')
        
        # Проверка на проблемы с румынскими символами
        romanian_chars = 'ăâîșțĂÂÎȘȚ'
        if any(char in text for char in romanian_chars):
            try:
                text.encode('latin2')
            except UnicodeEncodeError:
                issues.append('romanian_diacritics_issue')
        
        # Проверка на потерю форматирования
        if '\t' in text or '  ' in text:
            issues.append('formatting_loss_detected')
        
        return issues
    
    def _calculate_authenticity_score(self, ocr_result, distortion_analysis, 
                                   quantum_check, font_issues) -> float:
        """Расчет итоговой оценки аутентичности"""
        base_score = 1.0
        
        # OCR уверенность
        ocr_weight = 0.3
        base_score -= (1.0 - ocr_result.confidence) * ocr_weight
        
        # Искажения
        if distortion_analysis['distortion_detected']:
            distortion_weight = 0.4
            base_score -= distortion_analysis['distortion_score'] * distortion_weight
        
        # Квантовая целостность
        if not quantum_check['integrity_preserved']:
            quantum_weight = 0.2
            base_score -= quantum_weight
        
        # Проблемы шрифтов
        if font_issues:
            font_weight = 0.1
            base_score -= len(font_issues) * font_weight
        
        return max(0.0, min(1.0, base_score))
    
    def _generate_document_id(self, file_path: str) -> str:
        """Генерация ID документа"""
        timestamp = datetime.now().isoformat()
        file_hash = hashlib.md5(file_path.encode()).hexdigest()[:8]
        return f"doc_{file_hash}_{timestamp}"
    
    def generate_authenticity_report(self, checks: List[AuthenticityCheck]) -> str:
        """Генерация отчета проверки аутентичности"""
        report = {
            'verification_summary': {
                'total_documents': len(checks),
                'authentic_documents': sum(1 for c in checks if c.authenticity_score >= self.thresholds['minimum_authenticity']),
                'high_authenticity': sum(1 for c in checks if c.authenticity_score >= self.thresholds['high_authenticity']),
                'distorted_documents': sum(1 for c in checks if c.distortion_detected),
                'quantum_verified': sum(1 for c in checks if c.quantum_verified)
            },
            'average_scores': {
                'authenticity': sum(c.authenticity_score for c in checks) / max(len(checks), 1),
                'distortion_level': sum(1 for c in checks if c.distortion_detected) / max(len(checks), 1)
            },
            'font_issues_summary': {},
            'verification_timestamp': datetime.now().isoformat(),
            'detailed_checks': []
        }
        
        # Анализ проблем с шрифтами
        for check in checks:
            for issue in check.font_conversion_issues:
                report['font_issues_summary'][issue] = report['font_issues_summary'].get(issue, 0) + 1
        
        # Детальные результаты
        for check in checks:
            report['detailed_checks'].append({
                'document_id': check.document_id,
                'authenticity_score': check.authenticity_score,
                'distortion_detected': check.distortion_detected,
                'quantum_verified': check.quantum_verified,
                'font_issues_count': len(check.font_conversion_issues),
                'verification_timestamp': check.timestamp.isoformat()
            })
        
        return json.dumps(report, ensure_ascii=False, indent=2)
    
    def batch_verify_documents(self, directory: str, file_pattern: str = "*.pdf") -> List[AuthenticityCheck]:
        """Пакетная проверка документов"""
        print(f"📁 Пакетная проверка аутентичности: {directory}")
        
        import glob
        files = glob.glob(os.path.join(directory, file_pattern))
        results = []
        
        for file_path in files:
            try:
                result = self.verify_document_authenticity(file_path)
                results.append(result)
                print(f"✅ Проверен: {os.path.basename(file_path)} - {result.authenticity_score:.2f}")
            except Exception as e:
                print(f"❌ Ошибка проверки {file_path}: {str(e)}")
        
        return results

def main():
    """Основная функция верификатора"""
    print("🛡️ Запуск Authenticity Verifier...")
    print("⚛️ A©tor Quantum System - Многоуровневая проверка аутентичности")
    
    # Инициализация верификатора
    verifier = AuthenticityVerifier()
    
    # Демонстрация проверки
    sample_text = "Acest text este protejat de sistemul cuantic A©tor"
    
    # Создание тестового результата
    sample_check = AuthenticityCheck(
        document_id="test_doc_001",
        original_text=sample_text,
        translated_text="[English translation]: This text is protected by the quantum system A©tor",
        back_translated="[Russian translation]: Этот текст защищен квантовой системой A©tor",
        authenticity_score=0.95,
        distortion_detected=False,
        quantum_verified=True,
        font_conversion_issues=[],
        timestamp=datetime.now()
    )
    
    print(f"📊 Образец проверки: {sample_check}")
    
    # Генерация отчета
    report = verifier.generate_authenticity_report([sample_check])
    print(f"📋 Отчет проверки: {report}")
    
    print("🔚 Верификатор аутентичности готов к работе")

if __name__ == "__main__":
    main()