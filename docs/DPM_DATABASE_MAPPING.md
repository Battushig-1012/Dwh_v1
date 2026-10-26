# EBA DPM Database description (August 2013) → платформын сайжруулалт

**Эх сурвалж:** *Data Point Model database* — EBA DPM meta-model description (August 2013)

**Огноо:** 2026-10-26

---

## Документийн гол санаа

DPM нь тайлангийн **template (table)** болон **dimensional data point**-ийн хоорондын холбоог relational meta-model-оор хадгална:

`ReportingFramework → Taxonomy → Module → Table/TableVersion → Axis / AxisOrdinate → TableCell → DataPoint / DataPointVersion`

Dimensional: `Domain → Dimension → Member` (+ Hierarchy), Metric + Context (XBRL холбоос).

Давуу тал: consistency check, олон view, DWH/time-series-д DataPoint-ийн тогтвортой ID.

---

## Платформд юу нэмсэн бэ

| DPM ойлголт | Хэрэгжилт |
|---|---|
| ReportingFramework / Taxonomy / Module | `MN_REG` / `MN_REG_2026` / `M1_MONTHLY` |
| Table + TableVersion | `M1` / `M1.00` |
| Axis X/Y | Columns / Rows |
| AxisOrdinate + categorisation | Мөр бүрийн `[Dimension].[Member]` |
| TableCell (shaded / reportable) | Abstract header = shaded |
| DataPoint + DataPointVersion | Тогтвортой DP-id + CategorisationKey |
| Metric + ContextOfDataPoints | Metric vs бусад хэмжээс салгах (XBRL-ready) |
| Domain / Dimension / Member / Hierarchy | MET, BAS, MCAT, RSK |
| Validation / consistency | Metric mandatory, no dup dim, unique key, NPL formula |
| Fact | M1 дүн → DataPointID-тай холбосон |

### Файлүүд

| Файл | Үүрэг |
|---|---|
| `dwh/init/08_dpm_metamodel.sql` | PostgreSQL DPM schema (production path) |
| `backend/app/dpm_demo.py` | Demo meta-model + M1 mapping + checks |
| `backend/app/api/dpm.py` | `/api/dpm/*` |
| `frontend/src/app/dpm/page.tsx` | DPM UI |
| `frontend/src/app/reports/page.tsx` | M1 хүснэгтэд DP-id + categorisation key |
| `docs/DPM_DATABASE_MAPPING.md` | Энэ баримт |

### API

- `GET /api/dpm/overview`
- `GET /api/dpm/table/m1`
- `GET /api/dpm/dictionary`
- `GET /api/dpm/datapoints/{id}`
- `GET /api/dpm/consistency`
- `GET /api/dpm/facts/m1`

### UI

- http://localhost:3000/dpm
- http://localhost:3000/reports — DataPoint багана нэмэгдсэн

---

## Яагаад ингэж сайжруулсан бэ

Өмнө нь `M1.A.01` зэрэг кодууд зөвхөн **flat mart** мөр байсан. DPM-ийн дагуу:

1. Мөр/багана → **ordinate categorisation**
2. Нэг бизнес баримт → **нэг DataPoint** (олон cell хуваалцаж болно)
3. Taxonomy өөрчлөгдсөн ч DataPoint ID хадгалагдана (versioning)
4. Автомат consistency check хийх боломжтой

SSM/BCBS/ICT модулиудтай **давхцахгүй** — тэд засаглал/эрсдэл/ICT; DPM бол **тайлангийн meta + fact identity**.

---

## Цаашид

- `DEMO_MODE=false` үед `08_dpm_metamodel.sql` + seed loader
- Нэмэлт template (СЗХ, COREP-style) ижил meta-model дээр
- XBRL export: Metric = primary item, Context = бусад dimension-member
