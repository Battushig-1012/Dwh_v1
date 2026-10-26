# EBA/GL/2019/04 — ICT & Security Risk Management → платформын сайжруулалт

**Эх сурвалж:** *Final Report — EBA Guidelines on ICT and security risk management* (EBA/GL/2019/04, 29 November 2019)

**Огноо:** 2026-10-26  
**Хамаарал:** SSM RDARR / BCBS 239 хуудсуудыг **солиогүй**; ICT & security-ийн шаардлагыг **нэмэлт модуль** болгож нэмсэн.

---

## Юу хийсэн бэ? (товч)

| Хэсэг | Платформд нэмсэн |
|---|---|
| **3.1** Proportionality | Scorecard дээр NBFI/пропорциональ хэрэглээ тэмдэглэсэн |
| **3.2** Governance & ICT strategy | ICT стратеги, зорилго, action plan, удирдлагын үүрэг |
| **3.2.3** Third parties | Гуравдагч талын бүртгэл + assurance / exit plan |
| **3.3** ICT risk framework | Asset inventory (CIA), хамаарал, risk register, audit findings |
| **3.4** Information security | Policy summary, IAM matrix, least privilege, recertification |
| **3.4.2(d)** Privileged logging | Login / failed login / admin login → privileged activity log API |
| **3.4.5–3.4.7** Monitor / test / awareness | Monitoring чадварууд, security test бүртгэл, awareness % |
| **3.5** Operations | Backup/RTO/RPO, capacity, incident register + process |
| **3.6** Project & change | ICT төсөл + change log (security review flag) |
| **3.7** BCM | Platform BIA (RTO/RPO), BCP scenario/test, crisis comms |
| **3.8** PSU | **N/A** — төлбөрийн үйлчилгээний UI биш |

---

## Техникийн өөрчлөлт (файл)

| Файл | Үүрэг |
|---|---|
| `backend/app/ict_security_demo.py` | EBA хэсгүүдийн demo дата + privileged log |
| `backend/app/api/ict.py` | `/api/ict/*` endpoints |
| `backend/app/api/auth.py` | Амжилттай/амжилтгүй нэвтрэлтийг ICT log руу бичнэ |
| `backend/app/api/__init__.py` | ICT router холболт |
| `frontend/src/app/ict/page.tsx` | **ICT Security** UI (таб: Overview…BCM) |
| `frontend/src/components/AppShell.tsx` | Навигацид `ICT Security` |
| `docs/EBA_ICT_SECURITY_MAPPING.md` | Энэ баримт |

### Шинэ API

- `GET /api/ict/overview`
- `GET /api/ict/strategy`
- `GET /api/ict/assets`
- `GET /api/ict/information-security`
- `GET /api/ict/operations`
- `GET /api/ict/change`
- `GET /api/ict/bcm`
- `GET /api/ict/audit`
- `GET /api/ict/privileged-log` (ADMIN / AUDITOR / RISK)

### Шинэ UI

- http://localhost:3000/ict

---

## Яагаад ингэж сайжруулсан бэ?

1. **RDARR/BCBS** нь эрсдэлийн **дата агрегаци/тайлан**-д төвлөрдөг.  
2. **EBA ICT GL** нь тэр датаг хадгалж, боловсруулж, хамгаалах **ICT систем, хандалт, үйлдэл, тасралт**-ыг шаарддаг.  
3. Хоёулаа SREP/засаглалд хэрэгтэй тул нэг платформ дээр **өөр модуль** болгон хадгалсан (давхардлыг багасгах).

### Давхардлыг хэрхэн шийдсэн бэ?

| Сэдэв | Аль хэдийн байсан | ICT модульд |
|---|---|---|
| BCP / timeliness | BCBS `/bcbs`, SSM `/timeliness` | Platform **BIA + ICT BCP test** нарийвчилсан |
| Access / RBAC | Login roles | **Least privilege matrix, recertification, privileged log** |
| Change | BCBS change checklist | **ICT change/project register + security review** |
| Incidents | DQ issues | **Operational/security ICT incident process** |

---

## Цаашид (production)

- `DEMO_MODE=false` үед privileged log / incident / asset-ийг `governance` schema хүснэгт рүү шилжүүлэх  
- MFA (action plan AP-01), SIEM use-case, жилийн pentest-ийг бодит хэрэгсэлтэй холбох  
- 3.8 Payment PSU зөвхөн төлбөрийн үйлчилгээ нэмэгдвэл тусад нь

---

## Ашиглах

1. API/UI асаалттай үед нэвтрэх: `risk` / `ChangeMe123!`  
2. Цэс → **ICT Security**  
3. Privileged log харах: `admin` эсвэл `auditor` / `risk` эрхээр
