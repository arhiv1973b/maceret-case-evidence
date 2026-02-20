#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор финальных юридических выдержек
A©tor Quantum System - Подготовка судебных документов для международных инстанций
"""

import os
import sys
import json
import hashlib
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

# Импорт систем
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '07_Этические_маркеры'))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '05_Квантовые_вычисления'))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '03_Переводы'))

from quantum_auth_system import QuantumAuthSystem
from jus_cogens_calculator import JusCogensQuantumCalculator

@dataclass
class LegalExtract:
    """Юридическая выдержка"""
    title: str
    content: str
    legal_basis: List[str]
    violations_detected: List[str]
    quantum_signature: str
    intended_recipient: str
    urgency_level: str

class FinalLegalExtractsGenerator:
    """Генератор финальных юридических выдержек"""
    
    def __init__(self):
        self.quantum_auth = QuantumAuthSystem()
        self.jus_cogens_calc = JusCogensQuantumCalculator()
        self.extract_templates = self._initialize_templates()
        self.recipients = self._initialize_recipients()
        
    def _initialize_templates(self) -> Dict:
        """Инициализация шаблонов юридических документов"""
        return {
            "european_court": {
                "title": "Жалоба в Европейский суд по правам человека",
                "structure": [
                    "I. Сведения о заявителе",
                    "II. Фактические обстоятельства дела", 
                    "III. Нарушенные права и нормы",
                    "IV. Доказательства нарушений",
                    "V. Требования к Суду"
                ],
                "legal_basis": ["Конвенция о защите прав человека и основных свобод", "Протоколы к Конвенции"]
            },
            "un_committee": {
                "title": "Сообщение в Комитет ООН против пыток",
                "structure": [
                    "1. Идентификация жертвы",
                    "2. Описание пыток или жестокого обращения",
                    "3. Обстоятельства совершения нарушений",
                    "4. Государственные органы-нарушители",
                    "5. Внутренние средства правовой защиты"
                ],
                "legal_basis": ["Конвенция против пыток и других жестоких", "бесчеловечных или унижающих достоинство видов обращения"]
            },
            "international_criminal": {
                "title": "Обращение в Международный уголовный суд",
                "structure": [
                    "A. Юрисдикция Суда",
                    "B. Квалификация деяний как преступлений", 
                    "C. Доказательства вины лиц",
                    "D. Меры по обеспечению юрисдикции"
                ],
                "legal_basis": ["Римский статут Международного уголовного суда"]
            },
            "national_rehabilitation": {
                "title": "Ходатайство о реабилитации",
                "structure": [
                    "1. Основания для реабилитации",
                    "2. Доказательства незаконности осуждения",
                    "3. Последствия незаконного осуждения",
                    "4. Требования о компенсации вреда"
                ],
                "legal_basis": ["УПК РМ", "Закон о реабилитации жертв политических репрессий"]
            }
        }
    
    def _initialize_recipients(self) -> Dict:
        """Инициализация получателей документов"""
        return {
            "european_court": {
                "name": "Европейский суд по правам человека",
                "address": "Council of Europe, 67075 Strasbourg Cedex, France",
                "deadline": "6 месяцев с момента окончательного решения национальных судов",
                "language": "английский/французский"
            },
            "un_committee": {
                "name": "Комитет ООН против пыток",
                "address": "Office of the High Commissioner for Human Rights, Geneva, Switzerland",
                "deadline": "1 год с момента исчерпания внутренних средств защиты",
                "language": "английский/французский/испанский/русский"
            },
            "prosecutor_general": {
                "name": "Генеральному прокурору Республики Молдова",
                "address": "г. Кишинев, ул. 31 августа 1989 г., 82",
                "deadline": "немедленно",
                "language": "румынский/русский"
            },
            "parliament": {
                "name": "Парламенту Республики Молдова",
                "address": "г. Кишинев, пл. Великого Национального Собрания, 1",
                "deadline": "в течение 30 дней",
                "language": "румынский"
            }
        }
    
    def generate_extract_for_recipient(self, recipient_type: str, case_data: Dict) -> LegalExtract:
        """Генерация выдержки для конкретного получателя"""
        
        template = self.extract_templates.get(recipient_type)
        recipient = self.recipients.get(recipient_type)
        
        if not template or not recipient:
            raise ValueError(f"Неизвестный тип получателя: {recipient_type}")
        
        # Анализ нарушений на основе данных дела
        violations = self.jus_cogens_calc.analyze_document_for_violations(
            case_data.get("case_text", ""),
            case_data.get("metadata", {})
        )
        
        # Генерация контента на основе шаблона
        content = self._generate_content(template, case_data, violations, recipient)
        
        # Определение уровня срочности
        urgency_level = self._determine_urgency(violations, recipient_type)
        
        # Создание квантовой подписи
        quantum_signature = self._create_quantum_signature(content, violations)
        
        extract = LegalExtract(
            title=template["title"],
            content=content,
            legal_basis=template["legal_basis"],
            violations_detected=[v.violation_type for v in violations],
            quantum_signature=quantum_signature,
            intended_recipient=recipient["name"],
            urgency_level=urgency_level
        )
        
        return extract
    
    def _generate_content(self, template: Dict, case_data: Dict, violations: List, recipient: Dict) -> str:
        """Генерация контента документа"""
        
        content_parts = []
        
        # Заголовок
        content_parts.append(f"В {recipient['name']}")
        content_parts.append(f"Адрес: {recipient['address']}")
        content_parts.append(f"Дата: {datetime.now().strftime('%d.%m.%Y')}")
        content_parts.append("")
        
        # Основная часть на основе структуры шаблона
        for section in template["structure"]:
            content_parts.append(f"{section}")
            content_parts.append("-" * len(section))
            
            if "Сведения о заявителе" in section or "Идентификация жертвы" in section:
                content_parts.append(self._generate_applicant_info(case_data))
            elif "Фактические обстоятельства" in section or "Описание пыток" in section:
                content_parts.append(self._generate_factual_circumstances(case_data))
            elif "Нарушенные права" in section or "Квалификация деяний" in section:
                content_parts.append(self._generate_violations_section(violations))
            elif "Доказательства" in section:
                content_parts.append(self._generate_evidence_section(case_data, violations))
            elif "Требования" in section:
                content_parts.append(self._generate_requirements_section(recipient, violations))
            
            content_parts.append("")
        
        # Заключение
        content_parts.append("Приложения:")
        content_parts.append("1. Копии судебных решений")
        content_parts.append("2. Медицинские документы")
        content_parts.append("3. Показания свидетелей")
        content_parts.append("")
        content_parts.append(f"Квантовая подпись A©tor: {self._create_quantum_signature('', violations)}")
        content_parts.append("")
        content_parts.append("Подпись: _______________")
        
        return "\n".join(content_parts)
    
    def _generate_applicant_info(self, case_data: Dict) -> str:
        """Генерация информации о заявителе"""
        
        return f"""
Заявитель: {case_data.get('applicant_name', 'Не указано')}
Дата рождения: {case_data.get('birth_date', 'Не указана')}
Место жительства: {case_data.get('address', 'Не указано')}
Гражданство: {case_data.get('citizenship', 'Республика Молдова')}
Контактная информация: {case_data.get('contact', 'Не указана')}
""".strip()
    
    def _generate_factual_circumstances(self, case_data: Dict) -> str:
        """Генерация фактических обстоятельств"""
        
        return f"""
Хронология событий:
{case_data.get('timeline', 'Хронология не предоставлена')}

Ключевые участники:
- Прокурор: {case_data.get('prosecutor', 'Не указан')}
- Судья: {case_data.get('judge', 'Не указан')}
- Другие должностные лица: {case_data.get('other_officials', 'Не указаны')}

Обстоятельства дела:
{case_data.get('circumstances', 'Обстоятельства не описаны')}
""".strip()
    
    def _generate_violations_section(self, violations: List) -> str:
        """Генерация раздела о нарушениях"""
        
        if not violations:
            return "Конкретных нарушений не выявлено."
        
        violations_text = []
        for violation in violations:
            violations_text.append(f"- {violation.norm_article}: {violation.violation_type} (серьезность: {violation.severity:.2f})")
        
        return f"Выявленные нарушения прав человека:\n" + "\n".join(violations_text)
    
    def _generate_evidence_section(self, case_data: Dict, violations: List) -> str:
        """Генерация раздела доказательств"""
        
        evidence = []
        
        # Доказательства из данных дела
        if case_data.get('court_decisions'):
            evidence.append("- Судебные решения: " + case_data['court_decisions'])
        
        if case_data.get('medical_documents'):
            evidence.append("- Медицинские документы: " + case_data['medical_documents'])
        
        if case_data.get('witness_statements'):
            evidence.append("- Показания свидетелей: " + case_data['witness_statements'])
        
        # Доказательства нарушений
        for violation in violations:
            if violation.evidence:
                for ev in violation.evidence[:2]:  # Ограничиваем количество
                    evidence.append(f"- Доказательство по {violation.violation_type}: {ev}")
        
        return "\n".join(evidence) if evidence else "Доказательства не предоставлены."
    
    def _generate_requirements_section(self, recipient: Dict, violations: List) -> str:
        """Генерация раздела требований"""
        
        requirements = []
        
        if "Европейский суд" in recipient["name"]:
            requirements.extend([
                "1. Признать нарушение статей Конвенции о защите прав человека",
                "2. Назначить справедливую компенсацию морального и материального вреда",
                "3. Обязать государство принять меры по предотвращению подобных нарушений"
            ])
        elif "Комитет ООН" in recipient["name"]:
            requirements.extend([
                "1. Провести расследование фактов пыток и жестокого обращения",
                "2. Привлечь к ответственности виновных должностных лиц",
                "3. Обеспечить жертве эффективное средство правовой защиты"
            ])
        else:
            requirements.extend([
                "1. Отменить незаконные судебные решения",
                "2. Реабилитировать жертву незаконного преследования",
                "3. Выплатить компенсацию за причиненный вред"
            ])
        
        return "\n".join(requirements)
    
    def _determine_urgency(self, violations: List, recipient_type: str) -> str:
        """Определение уровня срочности"""
        
        if any(v.severity > 0.8 for v in violations):
            return "КРИТИЧЕСКАЯ"
        elif any(v.severity > 0.6 for v in violations):
            return "ВЫСОКАЯ"
        elif len(violations) > 2:
            return "СРЕДНЯЯ"
        else:
            return "НИЗКАЯ"
    
    def _create_quantum_signature(self, content: str, violations: List) -> str:
        """Создание квантовой подписи"""
        
        signature_data = {
            "content_hash": hashlib.sha256(content.encode('utf-8')).hexdigest(),
            "violations_count": len(violations),
            "timestamp": datetime.now().isoformat(),
            "total_severity": sum(v.severity for v in violations)
        }
        
        return hashlib.sha256(json.dumps(signature_data, sort_keys=True).encode()).hexdigest()
    
    def generate_all_extracts(self, case_data: Dict) -> List[LegalExtract]:
        """Генерация всех типов выдержек"""
        
        extracts = []
        
        # Генерируем для всех типов получателей
        for recipient_type in self.extract_templates.keys():
            try:
                extract = self.generate_extract_for_recipient(recipient_type, case_data)
                extracts.append(extract)
                print(f"✅ Сгенерирована выдержка для: {extract.intended_recipient}")
            except Exception as e:
                print(f"❌ Ошибка генерации для {recipient_type}: {e}")
        
        return extracts
    
    def save_extracts(self, extracts: List[LegalExtract]) -> List[str]:
        """Сохранение выдержек в файлы"""
        
        saved_files = []
        
        for extract in extracts:
            # Создаем имя файла
            safe_title = extract.title.replace(" ", "_").replace(",", "").lower()[:50]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_title}_{timestamp}.txt"
            
            # Сохраняем в директорию финальных выдержек
            output_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                "08_Финальные_выдержки", 
                filename
            )
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"{extract.title}\n")
                f.write("=" * len(extract.title) + "\n\n")
                f.write(f"Получатель: {extract.intended_recipient}\n")
                f.write(f"Уровень срочности: {extract.urgency_level}\n")
                f.write(f"Квантовая подпись: {extract.quantum_signature}\n\n")
                f.write(extract.content)
            
            saved_files.append(output_path)
            print(f"💾 Сохранено: {output_path}")
        
        return saved_files

def main():
    """Основная функция"""
    
    print("📋 Запуск Final Legal Extracts Generator...")
    print("🛡️ A©tor Quantum Protection Enabled")
    print("⚖️ Международные правовые стандарты активны")
    
    # Создаем генератор
    generator = FinalLegalExtractsGenerator()
    
    # Тестовые данные дела (на основе реальных документов)
    case_data = {
        "applicant_name": "Василенко",
        "birth_date": "Не указана",
        "address": "Не указан",
        "citizenship": "Республика Молдова",
        "contact": "Не указана",
        "timeline": """
2006 год - вынесено незаконное решение суда
13.02.2019 - подана жалоба на отмену решения
Прокурор Гуреев - нарушение процессуальных норм
Судья Холбан - императивный экзамен не проведен
""",
        "prosecutor": "Гуреев",
        "judge": "Холбан",
        "other_officials": "Сотрудники прокуратуры и суда",
        "circumstances": """
Нарушение статьи 22 УПК РМ - отсутствие оснований для уголовного преследования.
Применение недопустимых доказательств.
Отказ в предоставлении адвоката.
Нарушение презумпции невиновности.
""",
        "court_decisions": "Решение суда от 2006 года, жалоба от 13.02.2019",
        "medical_documents": "Не предоставлены",
        "witness_statements": "Не предоставлены",
        "case_text": """
В ходе судебного разбирательства были выявлены следующие нарушения:
1. Произвольное задержание без предъявления обвинений в течение 48 часов
2. Отказ в предоставлении адвоката на начальных этапах следствия  
3. Применение психологического давления для получения признательных показаний
4. Фальсификация доказательств со стороны прокурора Гуреева
5. Нарушение презумпции невиновности со стороны судьи Холбан
""",
        "metadata": {"case_number": "Не указан", "court": "Не указан"}
    }
    
    print(f"📄 Генерация выдержек для дела: {case_data['applicant_name']}")
    
    # Генерируем все выдержки
    extracts = generator.generate_all_extracts(case_data)
    
    print(f"\n📊 Сгенерировано выдержек: {len(extracts)}")
    
    for extract in extracts:
        print(f"  📄 {extract.title} - {extract.urgency_level}")
    
    # Сохраняем выдержки
    saved_files = generator.save_extracts(extracts)
    
    print(f"\n💾 Сохранено файлов: {len(saved_files)}")
    
    # Создаем сводный отчет
    summary_report = {
        "generation_summary": {
            "timestamp": datetime.now().isoformat(),
            "total_extracts": len(extracts),
            "case_applicant": case_data["applicant_name"],
            "quantum_protected": True
        },
        "extracts_details": [
            {
                "title": extract.title,
                "recipient": extract.intended_recipient,
                "urgency": extract.urgency_level,
                "violations_count": len(extract.violations_detected),
                "quantum_signature": extract.quantum_signature
            }
            for extract in extracts
        ],
        "legal_basis_used": list(set(
            basis for extract in extracts for basis in extract.legal_basis
        )),
        "violations_detected": list(set(
            violation for extract in extracts for violation in extract.violations_detected
        ))
    }
    
    # Сохраняем сводный отчет
    summary_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
        "08_Финальные_выдержки", 
        f"summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary_report, f, ensure_ascii=False, indent=2)
    
    print(f"📊 Сводный отчет сохранен: {summary_path}")
    print("\n🔚 Final Legal Extracts Generator готов к работе")

if __name__ == "__main__":
    main()