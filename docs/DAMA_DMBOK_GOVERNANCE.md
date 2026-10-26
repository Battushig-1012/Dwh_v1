# DAMA-DMBOK нийцэл — ББСБ Дата Засаглал

Энэхүү платформ нь **DAMA-DMBOK (Data Management Body of Knowledge)**-ийн гол мэдлэгийн хэсгүүдийг техникийн түвшинд тусгасан.

## Knowledge Areas → Системийн хэрэгжилт

| DAMA Knowledge Area | Платформ дахь шийдэл |
|---|---|
| **Data Governance** | `governance` schema, Data Owner / Steward талбарууд, RBAC (EXEC/RISK/REPORT/AUDITOR/ADMIN) |
| **Data Architecture** | 3 үе шат: `staging` → `dw_core` → `data_marts` |
| **Data Modeling & Design** | Core fact/dim загвар, mart-ууд SREP/DPM кодчиллоор |
| **Data Storage & Operations** | On-premise PostgreSQL DWH, batch лог, health check |
| **Data Security** | JWT + role-based API, PII тэмдэглэл (`is_pii`), ангилал (Internal/Confidential/Restricted) |
| **Data Integration & Interoperability** | Python ETL, incremental load, Airflow DAG (`etl/dags`) |
| **Document & Content Management** | Excel/PDF export — гар аргаар засахгүй, audit trail |
| **Reference & Master Data** | `dw_core.dim_customer` (SCD бэлэн бүтэц) |
| **Data Warehousing & BI** | `data_marts` + Next.js SREP dashboard |
| **Metadata** | `governance.data_dictionary` + `/api/dictionary` |
| **Data Quality** | Null / Range / Uniqueness engine + `dq_rule_results` |
| **Data Lineage** | `lineage_nodes` / `lineage_edges` + React Flow визуал |

## BCBS 239 / SREP 4 зарчим

1. **Lineage** — Эх систем → Staging → Core → Mart → Тайлан
2. **Dictionary & Metadata** — багана бүрийн утга, нэгж, эзэмшигч
3. **Accuracy & Integrity** — Excel-ээр тоо засахгүй; бүх өөрчлөлт код + audit trail
4. **Timeliness** — Шөнө 02:00 ETL → өглөө 09:00 бэлэн дашборд

## Үүрэг (RACI товч)

| Үүрэг | Хариуцлага |
|---|---|
| Data Owner | Бизнес утга, ангилал, хандалтын бодлого |
| Data Steward | Dictionary шинэчлэл, DQ дүрмийн тохиргоо |
| ETL Engineer | Пайплайн, чанарын шалгуур |
| Reporting Officer | Регуляцийн экспорт, баталгаажуулалт |
| Auditor | Lineage / Audit trail шалгалт (зөвхөн унших) |
