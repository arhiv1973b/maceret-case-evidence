#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Квантовые вычисления для анализа Jus Cogens
A©tor Quantum System - Применение императивных норм международного права
"""

import os
import sys
import json
import math
import hashlib
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
# import numpy as np  # Не требуется для базовых квантовых вычислений

# Импорт квантовой системы
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '07_Этические_маркеры'))
from quantum_auth_system import QuantumAuthSystem

@dataclass
class JusCogensViolation:
    """Нарушение императивной нормы Jus Cogens"""
    norm_article: str
    violation_type: str
    severity: float  # 0.0 - 1.0
    evidence: List[str]
    quantum_signature: str
    erga_omnes_weight: float

@dataclass
class QuantumCalculation:
    """Результат квантового расчета"""
    calculation_id: str
    input_data: Dict
    result_vector: List[float]
    probability_amplitude: complex
    collapse_state: str
    quantum_hash: str

class JusCogensQuantumCalculator:
    """Квантовый калькулятор для анализа Jus Cogens"""
    
    def __init__(self):
        self.quantum_auth = QuantumAuthSystem()
        self.jus_cogens_norms = self._initialize_jus_cogens()
        self.erga_omnes_principles = self._initialize_erga_omnes()
        self.quantum_state = {}
        self.violations_detected = []
        
        # Принципы "Кролик беги" и "игрек минус"
        self.ethical_principles = {
            "rabbit_run": {
                "description": "Защита от обмана идеалистов",
                "weight": 0.8,
                "quantum_frequency": 7.83  # Резонанс Шумана
            },
            "y_minus": {
                "description": "Глобальная утопия против коллапса сознания", 
                "weight": 0.9,
                "quantum_frequency": 13.5  # Гармоника сознания
            }
        }
    
    def _initialize_jus_cogens(self) -> Dict:
        """Инициализация императивных норм Jus Cogens"""
        return {
            "prohibition_of_torture": {
                "article": "Конвенция против пыток 1984",
                "weight": 1.0,
                "erga_omnes": True,
                "keywords": ["пытки", "жестокое обращение", "бесчеловечное", "унижающее"]
            },
            "right_to_fair_trial": {
                "article": "Международный пакт о гражданских и политических правах, ст. 14",
                "weight": 0.95,
                "erga_omnes": True,
                "keywords": ["справедливый суд", "равенство перед законом", "презумпция невиновности"]
            },
            "prohibition_of_arbitrary_arrest": {
                "article": "МПГПП, ст. 9",
                "weight": 0.9,
                "erga_omnes": True,
                "keywords": ["произвольное задержание", "незаконное арест", "свобода"]
            },
            "right_to_effective_remedy": {
                "article": "МПГПП, ст. 2",
                "weight": 0.85,
                "erga_omnes": True,
                "keywords": ["эффективное средство правовой защиты", "восстановление прав"]
            }
        }
    
    def _initialize_erga_omnes(self) -> Dict:
        """Инициализация принципов erga omnes"""
        return {
            "obligation_to_protect": {
                "description": "Обязательство защищать фундаментальные права",
                "quantum_weight": 0.95,
                "frequency": 432  # Гц - частота гармонии
            },
            "universal_jurisdiction": {
                "description": "Универсальная юрисдикция над серьезными нарушениями",
                "quantum_weight": 0.9,
                "frequency": 528  # Гц - частота трансформации
            },
            "non_derogable_rights": {
                "description": "Неотъемлемые права не подлежат ограничению",
                "quantum_weight": 1.0,
                "frequency": 741  # Гц - частота пробуждения
            }
        }
    
    def calculate_quantum_superposition(self, violations: List[JusCogensViolation]) -> QuantumCalculation:
        """Расчет квантовой суперпозиции нарушений"""
        
        # Создаем вектор состояния из нарушений
        state_vector = []
        for violation in violations:
            amplitude = violation.severity * violation.erga_omnes_weight
            state_vector.append(amplitude)
        
        # Нормализация вектора
        norm = math.sqrt(sum(x**2 for x in state_vector))
        if norm > 0:
            state_vector = [x/norm for x in state_vector]
        
        # Расчет амплитуды вероятности
        probability_amplitude = complex(
            sum(state_vector) * self.ethical_principles["rabbit_run"]["weight"],
            sum(state_vector) * self.ethical_principles["y_minus"]["weight"]
        )
        
        # Определение состояния коллапса
        collapse_state = self._determine_collapse_state(probability_amplitude)
        
        # Генерация квантового хеша
        calculation_data = {
            "state_vector": state_vector,
            "probability_amplitude": str(probability_amplitude),
            "timestamp": datetime.now().isoformat()
        }
        quantum_hash = hashlib.sha256(json.dumps(calculation_data, sort_keys=True).encode()).hexdigest()
        
        return QuantumCalculation(
            calculation_id=f"QC_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            input_data={"violations_count": len(violations)},
            result_vector=state_vector,
            probability_amplitude=probability_amplitude,
            collapse_state=collapse_state,
            quantum_hash=quantum_hash
        )
    
    def _determine_collapse_state(self, amplitude: complex) -> str:
        """Определение состояния коллапса квантовой системы"""
        
        magnitude = abs(amplitude)
        phase = math.atan2(amplitude.imag, amplitude.real)
        
        if magnitude > 0.8:
            return "critical_violation"
        elif magnitude > 0.6:
            return "significant_breach"
        elif magnitude > 0.4:
            return "moderate_concern"
        else:
            return "minor_issue"
    
    def analyze_document_for_violations(self, document_text: str, metadata: Dict = None) -> List[JusCogensViolation]:
        """Анализ документа на предмет нарушений Jus Cogens"""
        
        violations = []
        text_lower = document_text.lower()
        
        for norm_name, norm_data in self.jus_cogens_norms.items():
            violation_detected = False
            evidence = []
            severity = 0.0
            
            # Поиск ключевых слов нарушений
            for keyword in norm_data["keywords"]:
                if keyword in text_lower:
                    violation_detected = True
                    # Извлекаем контекст вокруг ключевого слова
                    context_start = max(0, text_lower.find(keyword) - 50)
                    context_end = min(len(text_lower), text_lower.find(keyword) + 50)
                    context = document_text[context_start:context_end].strip()
                    evidence.append(context)
                    
                    # Рассчитываем серьезность на основе контекста
                    severity = max(severity, self._calculate_severity(context, norm_name))
            
            if violation_detected:
                # Применяем этические принципы
                ethical_adjustment = self._apply_ethical_principles(document_text)
                adjusted_severity = min(1.0, severity * ethical_adjustment)
                
                violation = JusCogensViolation(
                    norm_article=norm_data["article"],
                    violation_type=norm_name,
                    severity=adjusted_severity,
                    evidence=evidence,
                    quantum_signature=self._generate_quantum_signature(evidence),
                    erga_omnes_weight=norm_data["weight"] if norm_data["erga_omnes"] else 0.5
                )
                
                violations.append(violation)
                self.violations_detected.append(violation)
        
        return violations
    
    def _calculate_severity(self, context: str, norm_name: str) -> float:
        """Расчет серьезности нарушения на основе контекста"""
        
        base_severity = 0.5
        
        # Увеличиваем серьезность при наличии определенных маркеров
        severity_markers = {
            "systematic": 0.3,
            "deliberate": 0.4,
            "repeated": 0.2,
            "official": 0.3,
            "unlawful": 0.3
        }
        
        for marker, increase in severity_markers.items():
            if marker in context.lower():
                base_severity += increase
        
        return min(1.0, base_severity)
    
    def _apply_ethical_principles(self, text: str) -> float:
        """Применение этических принципов 'Кролик беги' и 'игрек минус'"""
        
        # "Кролик беги" - детекция обмана идеалистов
        deception_indicators = ["обещали", "гарантировали", "уверяли", "заверяли"]
        rabbit_run_factor = 1.0
        
        for indicator in deception_indicators:
            if indicator in text.lower():
                rabbit_run_factor *= 1.2  # Увеличиваем вес при обмане
        
        # "игрек минус" - защита от коллапса сознания
        consciousness_collapse_indicators = ["дезориентация", "путаница", "противоречие", "абсурд"]
        y_minus_factor = 1.0
        
        for indicator in consciousness_collapse_indicators:
            if indicator in text.lower():
                y_minus_factor *= 1.3  # Увеличиваем вес при коллапсе сознания
        
        return (rabbit_run_factor + y_minus_factor) / 2
    
    def _generate_quantum_signature(self, evidence: List[str]) -> str:
        """Генерация квантовой подписи для доказательств"""
        
        evidence_str = "|".join(evidence)
        timestamp = datetime.now().isoformat()
        signature_data = f"{evidence_str}_{timestamp}"
        
        return hashlib.sha256(signature_data.encode('utf-8')).hexdigest()
    
    def generate_jus_cogens_report(self, violations: List[JusCogensViolation], 
                                 quantum_calc: QuantumCalculation) -> Dict:
        """Генерация отчета по анализу Jus Cogens"""
        
        # Расчет общего уровня нарушений
        total_severity = sum(v.severity * v.erga_omnes_weight for v in violations)
        max_possible_severity = len(violations) * 1.0 * 1.0  # max severity * max weight
        violation_percentage = (total_severity / max_possible_severity * 100) if max_possible_severity > 0 else 0
        
        # Классификация нарушений
        critical_violations = [v for v in violations if v.severity > 0.8]
        significant_violations = [v for v in violations if 0.6 < v.severity <= 0.8]
        moderate_violations = [v for v in violations if 0.4 < v.severity <= 0.6]
        
        report = {
            "jus_cogens_analysis": {
                "analysis_timestamp": datetime.now().isoformat(),
                "total_violations": len(violations),
                "violation_percentage": violation_percentage,
                "collapse_state": quantum_calc.collapse_state,
                "quantum_hash": quantum_calc.quantum_hash
            },
            "violation_breakdown": {
                "critical": len(critical_violations),
                "significant": len(significant_violations), 
                "moderate": len(moderate_violations),
                "minor": len(violations) - len(critical_violations) - len(significant_violations) - len(moderate_violations)
            },
            "erga_omnes_assessment": {
                "applicable_norms": len([v for v in violations if v.erga_omnes_weight > 0.8]),
                "universal_jurisdiction_triggered": total_severity > 2.0,
                "international_obligations_breached": len(set(v.norm_article for v in violations))
            },
            "ethical_principles_applied": {
                "rabbit_run_protection": self.ethical_principles["rabbit_run"]["description"],
                "y_minus_stabilization": self.ethical_principles["y_minus"]["description"],
                "quantum_frequency_analysis": True
            },
            "detailed_violations": [
                {
                    "norm": v.norm_article,
                    "type": v.violation_type,
                    "severity": v.severity,
                    "erga_omnes_weight": v.erga_omnes_weight,
                    "quantum_signature": v.quantum_signature,
                    "evidence_count": len(v.evidence)
                }
                for v in violations
            ],
            "quantum_calculation": {
                "calculation_id": quantum_calc.calculation_id,
                "state_vector": quantum_calc.result_vector,
                "probability_amplitude": str(quantum_calc.probability_amplitude),
                "collapse_state": quantum_calc.collapse_state
            },
            "recommendations": self._generate_recommendations(violations, quantum_calc)
        }
        
        return report
    
    def _generate_recommendations(self, violations: List[JusCogensViolation], 
                                quantum_calc: QuantumCalculation) -> List[str]:
        """Генерация рекомендаций на основе анализа"""
        
        recommendations = []
        
        if quantum_calc.collapse_state == "critical_violation":
            recommendations.append("🚨 НЕМЕДЛЕННОЕ вмешательство международных инстанций требуется")
            recommendations.append("🔒 Применение универсальной юрисдикции erga omnes")
        
        if any(v.severity > 0.8 for v in violations):
            recommendations.append("⚖️ Рассмотрение дела в Европейском суде по правам человека")
            recommendations.append("📋 Подготовка жалобы в Комитет ООН против пыток")
        
        if len(violations) > 3:
            recommendations.append("🔄 Системный характер нарушений требует комплексной реформы")
            recommendations.append("🌐 Обращение в международные правозащитные организации")
        
        # Рекомендации на основе этических принципов
        recommendations.append("🐇 Применение протокола 'Кролик беги' для защиты от дальнейшего обмана")
        recommendations.append("🧘 Использование 'игрек минус' для предотвращения коллапса правосознания")
        
        return recommendations
    
    def save_analysis_report(self, report: Dict, filename: str = None):
        """Сохранение отчета анализа"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"jus_cogens_analysis_{timestamp}.json"
        
        output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "06_Анализ_Jus_Cogens", filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Отчет Jus Cogens сохранен: {output_path}")
        return output_path

def main():
    """Основная функция"""
    
    print("⚛️ Запуск Jus Cogens Quantum Calculator...")
    print("🛡️ A©tor Quantum Protection Enabled")
    print("🌍 Erga Omnes Jurisdiction Active")
    
    # Создаем калькулятор
    calculator = JusCogensQuantumCalculator()
    
    # Тестовый документ (на основе реальных данных из дела)
    test_document = """
    В ходе судебного разбирательства были выявлены следующие нарушения:
    1. Произвольное задержание без предъявления обвинений в течение 48 часов
    2. Отказ в предоставлении адвоката на начальных этапах следствия  
    3. Применение психологического давления для получения признательных показаний
    4. Фальсификация доказательств со стороны прокурора Гуреева
    5. Нарушение презумпции невиновности со стороны судьи Холбан
    """
    
    print(f"📄 Анализ документа: {len(test_document)} символов")
    
    # Анализ документа на нарушения
    violations = calculator.analyze_document_for_violations(test_document)
    
    print(f"🔍 Обнаружено нарушений: {len(violations)}")
    
    for i, violation in enumerate(violations, 1):
        print(f"  {i}. {violation.norm_article} - Серьезность: {violation.severity:.3f}")
    
    # Квантовые вычисления
    quantum_calc = calculator.calculate_quantum_superposition(violations)
    
    print(f"⚛️ Квантовое состояние: {quantum_calc.collapse_state}")
    print(f"📊 Амплитуда вероятности: {abs(quantum_calc.probability_amplitude):.3f}")
    
    # Генерация отчета
    report = calculator.generate_jus_cogens_report(violations, quantum_calc)
    
    print("\n📋 Краткий отчет:")
    print(f"  Всего нарушений: {report['jus_cogens_analysis']['total_violations']}")
    print(f"  Процент нарушений: {report['jus_cogens_analysis']['violation_percentage']:.1f}%")
    print(f"  Критических нарушений: {report['violation_breakdown']['critical']}")
    print(f"  Применимых норм erga omnes: {report['erga_omnes_assessment']['applicable_norms']}")
    
    # Сохранение отчета
    calculator.save_analysis_report(report)
    
    print("\n🔚 Jus Cogens Quantum Calculator готов к работе")

if __name__ == "__main__":
    main()