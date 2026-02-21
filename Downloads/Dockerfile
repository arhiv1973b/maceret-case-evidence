FROM alpine:latest

WORKDIR /evidence

COPY Apostilles ./Apostilles/
COPY APOSTILLE_INVESTIGATION_SUMMARY.md ./
COPY README.md ./
COPY "Реестр_полный_EVIDENCE.pdf" ./

RUN apk add --no-cache sha256sum && \
    mkdir -p /integrity-hashes && \
    find . -type f \( -name "*.pdf" -o -name "*.md" \) -exec sha256sum {} \; > /integrity-hashes/registry.json && \
    find . -type f \( -name "*.pdf" -o -name "*.md" \) -printf "%p|%s|%T@\n" > /integrity-hashes/sbom.csv && \
    echo "SBOM Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)" > /integrity-hashes/manifest.json

LABEL description="Legal evidence for Maceret case"
LABEL disability_group="I"
LABEL legal_status="Art. 3 ECHR vulnerability"
LABEL sbom="spdx-json"

CMD ["sh"]
