# Ops Reports — жижиг/завсрын тайлангийн каталог

**Асуудал:** Завсрын мэдээ, Core тооцоолол нэмэгдэх тусам sidebar дүүрнэ.  
**Шийдэл:** Нэг цэс **Ops Reports** + backend **registry/pack**.

---

## Хэрэглэгчид

1. Sidebar → **Ops Reports**
2. Каталогоос тайлан сонгоно
3. Дэлгэрэнгүй: `/ops-reports/{CODE}`

Regulatory M1/SREP export тусдаа үлдэнэ: **Reg Reports**.

---

## Backend бүтэц

```
backend/app/ops_reports/
  registry.py              # ReportSpec + register/list/catalog
  __init__.py              # pack-уудыг ачаална (_load_packs)
  <code>/
    calc.py                # тооцоолол / demo дата
    __init__.py            # register(ReportSpec(...))
```

### API (нэг router)

| Method | Path |
|---|---|
| GET | `/api/ops-reports` — каталог |
| GET | `/api/ops-reports/{CODE}` — meta |
| GET | `/api/ops-reports/{CODE}/overview` |
| GET | `/api/ops-reports/{CODE}/mart` |
| GET | `/api/ops-reports/{CODE}/staging` |
| GET | `/api/ops-reports/{CODE}/pipeline` |
| GET | `/api/ops-reports/{CODE}/sql` |

---

## Шинэ тайлан нэмэх (sidebar хөндөхгүй)

1. `backend/app/ops_reports/<code>/calc.py` — дата + тооцоо  
2. `backend/app/ops_reports/<code>/__init__.py` — `register(ReportSpec(...))`  
3. `ops_reports/__init__.py` → `_load_packs()` дотор `from . import <code>`  
4. UI автоматаар каталогт гарна (`/ops-reports`)

---

## Юу sidebar-д үлдэх вэ

Зөвхөн **тогтвортой бүтээгдэхүүний бүлгүүд**: SREP, frameworks, DWH хяналт, **Ops Reports** (каталог), Reg Reports.  
Жижиг тайлан бүрийг nav-д бичихгүй.
