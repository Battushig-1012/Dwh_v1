# ECB SSM Guide → ББСБ Platform Mapping

Source: *Guide on effective risk data aggregation and risk reporting* (ECB Banking Supervision, May 2024)

| SSM Section | Expectation | Platform feature |
|---|---|---|
| **3.1** Management body | Accountability, CRO/CFO sponsor, DQ KPI monitoring, meaningful reports | `/rdarr` Management Pack, sponsors, training note |
| **3.2** Scope | Reports, models, KRIs, critical data elements | `/rdarr/scope` inventory |
| **3.3** Governance framework | Data owners, central DG, 2LOD validation, 3LOD audit | `/rdarr/governance` RACI |
| **3.4** Integrated architecture | Taxonomy, dictionary, attribute-level lineage | Dictionary + `/rdarr/attribute-lineage` + staging→core→marts |
| **3.5** DQ management | Accuracy/integrity/completeness/timeliness KPIs, issue register, EUC, reconciliation | `/rdarr/dq-kpis`, `/dq-issues`, `/workarounds` |
| **3.6** Timeliness | Frequency + production time (≤20 WD benchmark), stress/fire-drill | `/rdarr/timeliness`, fire-drill API |
| **3.7** Implementation programme | Milestones, sponsors, BCBS 239 self-assessment | `/rdarr/programme` |

UI routes: `/rdarr`, `/scope`, `/kri`, `/timeliness`, `/programme` (+ existing dashboard/lineage/quality/dictionary/reports).
