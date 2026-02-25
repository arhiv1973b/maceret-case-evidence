# MACERET CASE EVIDENCE - Container Registry

## Evidence Container

Docker image with complete apostille evidence for Maceret Alexei case.

### Pull Latest Image

```bash
docker pull ghcr.io/arhiv1973b/maceret-case-evidence:latest
```

### Verify Integrity

```bash
docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/arhiv1973b/maceret-case-evidence:latest
```

Compare the SHA-256 digest with records in `/integrity-hashes/`.

### Image Tags

| Tag         | Description      | Date       |
| ----------- | ---------------- | ---------- |
| `latest`    | Current evidence | 2026-02-21 |
| `sha-xxxxx` | Specific commit  | -          |

### Evidence Files (90 apostilles)

All apostilles processed with metadata:

- 7H2Q3790FZEI5 - TORTURE (1-568/98)
- 5S2WF92X7X4R8 - FRAMED DRUGS (1-272/03)
- CK5O133ZKLJE8 - FALSE CONVICTION (1-42/09)
- CO2S9BA3JX6H1 - VICTIM MURDER (Markova Galina)
- - 86 more

### Legal Status

This container contains verified evidence of:

- Torture case (1997-1998)
- False criminal charges
- Victim murder cover-up
- Attempted assassination

---

Generated: 2026-02-21
