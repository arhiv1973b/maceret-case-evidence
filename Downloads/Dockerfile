FROM alpine:latest

WORKDIR /evidence

COPY Apostilles ./Apostilles/
COPY APOSTILLE_INVESTIGATION_SUMMARY.md ./
COPY README.md ./
COPY "Реестр_полный_EVIDENCE.pdf" ./

RUN apk add --no-cache sha256sum && \
    find . -type f -name "*.pdf" -exec sha256sum {} \; > /integrity-hashes/registry.json

LABEL description="Legal evidence for Maceret case"
LABEL disability_group="I"
LABEL legal_status="Art. 3 ECHR vulnerability"

CMD ["sh"]
