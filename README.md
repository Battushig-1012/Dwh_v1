# ББСБ — Нэгдсэн Дата Засаглал & Тайлагналын Платформ

Enterprise Data & Regulatory Reporting Platform  
**SREP · BCBS 239 · DAMA-DMBOK** нийцэлтэй custom DWH stack.

## Архитектур

```
Data Sources → Python ETL (Airflow DAG) → PostgreSQL DWH
   staging → dw_core → data_marts (+ governance)
        → FastAPI → Next.js (SREP / Lineage / DQ / Dictionary / Reports)
```

| Давхарга | Технологи | Зориулалт |
|---|---|---|
| Sources | Oracle / MSSQL / MySQL / REST | Core, ERP, Loan App (read-replica) |
| ETL | Python 3.11, SQLAlchemy, Pandas, Airflow DAG | Incremental extract, DQ, transform |
| DWH | PostgreSQL 16 | `staging`, `dw_core`, `data_marts`, `governance` |
| API | FastAPI + JWT RBAC | Marts, lineage, dictionary, Excel/PDF |
| UI | Next.js + Recharts + React Flow | Дашборд, lineage, тайлангийн төв |

Дэлгэрэнгүй засаглал: [docs/DAMA_DMBOK_GOVERNANCE.md](docs/DAMA_DMBOK_GOVERNANCE.md)

## Шуурхай эхлүүлэх (Docker)

```bash
docker compose up -d postgres
# schema + seed автоматаар ачаална (/dwh/init)

docker compose up -d --build backend frontend
```

- UI: http://localhost:3000  
- API docs: http://localhost:8000/docs  
- Demo нэвтрэлт: `risk` / `ChangeMe123!`  
  (мөн `ceo`, `report`, `auditor`, `admin`)

### ETL ажиллуулах

```bash
docker compose --profile etl run --rm etl
```

эсвэл локал:

```bash
cd etl
pip install -r requirements.txt
set DATABASE_URL=postgresql+psycopg2://dwh_admin:dwh_secret_change_me@localhost:5432/bbsb_dwh
python -m src.run_nightly
```

Airflow-д суулгах DAG: `etl/dags/nightly_etl_dag.py` (cron `0 2 * * *`).

## Локал хөгжүүлэлт (Dockerгүйгээр)

1. PostgreSQL 16 дээр DB үүсгээд `dwh/init/*.sql` дарааллаар ажиллуулна.
2. Backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

3. Frontend:

```bash
cd frontend
npm install
set NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

## Үндсэн дэлгэцүүд

1. **SREP Dashboard** — Капитал / LCR / DPD / NPL
2. **Data Lineage** — React Flow граф
3. **Data Quality** — batch + DQ дүрмийн лог
4. **Data Dictionary** — Owner/Steward/PII/ангилал
5. **Regulatory Hub** — Mongolbank M1 Excel, SREP PDF (audit trail-тэй)

## Үйлдвэрлэлд шилжих checklist

- [ ] Core / ERP read-replica холболтын URL (`CORE_DB_URL`, `ERP_DB_URL`)
- [ ] `JWT_SECRET`, DB нууц үг солих
- [ ] Airflow (эсвэл scheduler) дээр nightly DAG идэвхжүүлэх
- [ ] Data Dictionary-г бизнесийн багана бүрт бүрэн бөглөх
- [ ] Mongolbank / СЗХ албан ёсны Excel загварыг OpenPyXL template болгох
- [ ] Network: DWH зөвхөн дотоод VLAN, app tier-ээс хандах

## Багийн үүрэг (санал)

| Үүрэг | Тоо |
|---|---|
| Data Architect / Lead | 1 |
| ETL Engineer | 1 |
| Full-Stack Developer | 1–2 |
| Data / Business Analyst | 1 |
