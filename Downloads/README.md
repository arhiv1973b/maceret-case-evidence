# MACERET CASE EVIDENCE

Legal evidence container for Maceret Alexei case.

## Status

**I группа инвалидности** (Group I disability) - critical for Art. 3 ECHR vulnerability assessment.

## Container

```bash
docker pull ghcr.io/arhiv1973b/maceret-case-evidence:latest
```

## Verify Integrity

```bash
docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/arhiv1973b/maceret-case-evidence:latest
```

Compare SHA-256 digest with `/integrity-hashes/registry.json`.

## Evidence Files

90 apostilles with metadata including:

- 7H2Q3790FZEI5 - TORTURE (1-568/98)
- 5S2WF92X7X4R8 - FRAMED DRUGS (1-272/03)
- CK5O133ZKLJE8 - FALSE CONVICTION (1-42/09)
- CO2S9BA3JX6H1 - VICTIM MURDER (Markova Galina)

## Legal Status

- Torture case (1997-1998)
- False criminal charges
- Victim murder cover-up

## ⚖️ Спецификация подлога: Дела 1-137/08, 1-983/07 и надзорные 4B-615/616

### 1. Искусственная изоляция «Дела Олейник»

- **Фактический подлог:** Материалы **4B-615/2007** и **4B-616/2007** подтверждают, что Ирина Олейник была арестована по фиктивному административному предлогу (нарушение тишины). Это было сделано для того, чтобы в условиях изоляции (5 суток) получить показания под пытками, которые затем легли в основу «Дела Олейник», выделенного из основного производства **1-983/07**.
- **Противоречие:** Мануальная (рукописная) версия дела **1-137/08** содержит записи, которые прямо исключают Олейник из состава преступления. Перевод дела в печатный вид на румынском языке был использован для «вписывания» её как соучастника.

### 2. Маскировка ошибки через ст. 361 УК РМ

- **Механизм сокрытия:** Верховный Суд не мог отменить штраф (ранее выросший из 90 леев в 12 000 леев), так как это автоматически бы обнажило фальсификацию текста в деле **1-983/07**.
- **Технология «Мануального сокрытия»:** В деле **1a-42/09** использование рукописного текста на русском языке было единственным способом оставить в материалах дела признание факта пыток, не допустив его попадания в электронную базу судебных решений.

## Links

- **Registry:** https://arhiv1973b.github.io/maceret-case-evidence/
- **Repository:** https://github.com/arhiv1973b/maceret-case-evidence

Generated: 2026-02-21
