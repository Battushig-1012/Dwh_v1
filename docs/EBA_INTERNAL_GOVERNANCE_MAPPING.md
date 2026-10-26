# EBA/GL/2021/05 — Guidelines on internal governance under CRD → платформын сайжруулалт

**Эх сурвалж:** *Final report on Guidelines on internal governance under Directive 2013/36/EU* (EBA/GL/2021/05, 2 July 2021)

**Огноо:** 2026-10-26

---

## Документийн гол санаа

CRD Art. 74 / 88-ийн дагуу байгууллагын **дотоод засаглал**:

| Title | Агуулга |
|---|---|
| **I** | Proportionality — хэмжээ, зохион байгуулалт, үйл ажиллагааны ээдрээ, эрсдэлийн профайл |
| **II** | Management body (management + supervisory function), chair, committees (risk / audit / nomination / remuneration) |
| **III** | Governance framework — know-your-structure, complex structures, group, outsourcing |
| **IV** | Risk culture, code of conduct, conflicts of interest (incl. loans to MB & related parties), whistleblowing |
| **V** | Internal control — three lines of defence, RMF / Compliance / Internal Audit, new products, risk framework |
| **VI** | Business continuity management (governance ownership) |
| **VII** | Transparency (internal & external) |

**Давхардалгүй:** RDARR (өгөгдөл/тайлангийн чанар), ICT (EBA/GL/2019/04 аюулгүй байдал/BCM дэлгэрэнгүй), DPM (тайлангийн meta-model) — энэ модуль **CRD засаглалын зохицуулалт**-ыг хамарна.

---

## Платформд юу нэмсэн бэ

| GL элемент | Хэрэгжилт |
|---|---|
| Title I Proportionality | NBFI-scale flag; combined Risk/Audit committee |
| Title II MB + committees | Management/supervisory members, collective suitability, Risk Committee mandate + meeting pack |
| Title III KYS / outsourcing | Legal entities, business lines, key functions; outsourcing → ICT third-party |
| Title IV Culture / CoI / WB | Code of conduct, CoI register (staff + related-party loan), whistleblowing channels |
| Title V 3LOD + control fns | 1/2/3LOD map; RMF, Compliance, IA mandates; NPAC recent case |
| Title VI BCM | Governance ownership + deep-link `/ict`, `/bcbs` |
| Title VII Transparency | Internal/external practices + reporting hub link |

### Файлүүд

| Файл | Үүрэг |
|---|---|
| `backend/app/internal_gov_demo.py` | Titles I–VII demo дата |
| `backend/app/api/governance.py` | `/api/governance/*` |
| `frontend/src/app/governance/page.tsx` | Governance UI (таб: Scorecard…BCM) |
| `frontend/src/components/AppShell.tsx` | Навигацид `Governance` |
| `docs/EBA_INTERNAL_GOVERNANCE_MAPPING.md` | Энэ баримт |

### API

- `GET /api/governance/overview`
- `GET /api/governance/management-body`
- `GET /api/governance/organisation`
- `GET /api/governance/conduct`
- `GET /api/governance/controls`
- `GET /api/governance/bcm-transparency`

### UI

- http://localhost:3000/governance

---

## Яагаад ингэж сайжруулсан бэ

1. **Art. 88 oversight** — supervisory function + risk committee-ийн mandate/meeting cadence одоо платформ дээр харагдана (зөвхөн risk data биш).
2. **Know-your-structure** — хуулийн этгээд / салбар / business line-ийн бүртгэл opaque structure байхгүйг баталгаажуулна.
3. **CoI & related-party loans** — GL §12.1–12.2-ийн дагуу баримтжуулалт + mitigation статус.
4. **3LOD** — 1LOD (ops/reporting) ↔ 2LOD (CRO/Compliance) ↔ 3LOD (IA) тодорхой; RDARR/ICT-тай холбосон.
5. **Proportionality** — ББСБ-д combined committee зөвшөөрөгдсөн хэв маяг.

---

## Цаашид

- `DEMO_MODE=false` үед committee minutes / CoI / suitability-ийн persistent tables
- Remuneration & nomination committee (significant institutions) — одоо N/A (proportionality)
- External governance disclosure PDF export
