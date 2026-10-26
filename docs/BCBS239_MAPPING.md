# BCBS 239 (Jan 2013) → Platform mapping

Source: *Principles for effective risk data aggregation and risk reporting* (BCBS, January 2013)

**Relationship to SSM Guide (May 2024):** SSM operationalises BCBS 239 for ECB banks. Existing `/rdarr`, `/scope`, `/kri`, `/quality`, `/timeliness`, `/programme` screens stay. This pack adds BCBS-native gaps only.

| Principle | Title | Existing (kept) | Added |
|---|---|---|---|
| P1 | Governance | RDARR Pack, 3LOD | Limitations, trade-offs, expert judgment, materiality, change checklist |
| P2 | Architecture / IT | DWH layers, dictionary, lineage | Single IDs, authoritative sources, BCP |
| P3 | Accuracy & Integrity | DQ engine, EUC, recon | Validation inventory, escalation, accuracy requirements |
| P4 | Completeness | Scope | Completeness matrix, concentrations by customer/product/branch |
| P5 | Timeliness | Timeliness SLA | (kept) |
| P6 | Adaptability | Fire-drill | Concentration ad-hoc views |
| P7 | Report accuracy | Export audit | Validation inventory (report checks) |
| P8 | Comprehensiveness | SREP pillars | Comprehensive risk report + scenarios |
| P9 | Clarity & usefulness | Exec pack | Recipient profiles + qualitative narrative |
| P10 | Frequency | Calendar | Stress frequency escalation matrix |
| P11 | Distribution | RBAC | Distribution list, classification, ack |
| P12–P14 | Supervisory | Evidence via drill/issues | Marked as evidence / N/A-light for solo ББСБ |

UI: `/bcbs`, `/risk-report`, `/distribution`, `/concentrations`
