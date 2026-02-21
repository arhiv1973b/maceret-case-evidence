# Использование легковесного образа для хранения данных
FROM alpine:latest

# Метаданные согласно CASE-MACHERET-1997-2026
LABEL org.opencontainers.image.title="Maceret Case Evidence" \
      org.opencontainers.image.description="Digital Evidence Archive - Actor Maceret Alexei" \
      org.opencontainers.image.vendor="A©tor" \
      org.opencontainers.image.version="2026.02.21" \
      case.id="CASE-MACHERET-1997-2026" \
      legal.jurisdiction="MD/ECHR" \
      legal.status="Non-rehabilitated / Disability Group I"

# Создание структуры директорий внутри контейнера
WORKDIR /evidence

# Копирование архива согласно структуре README
COPY legal-instruments/ ./legal-instruments/
COPY medical-records/ ./medical-records/
COPY procedural-docs/ ./procedural-docs/
COPY integrity-hashes/ ./integrity-hashes/
COPY README.md .

# Генерация финального хэша при сборке для верификации рантайма
RUN sha256sum README.md > build_verification.sha256

# Команда по умолчанию: вывод правового статуса при запуске
CMD ["cat", "README.md"]
