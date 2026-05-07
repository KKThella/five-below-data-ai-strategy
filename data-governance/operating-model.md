# Data Governance Operating Model

> Governance is not compliance overhead. It's the operating system that makes every downstream data investment trustworthy.

---

## Governance philosophy

Five Below's data governance model follows a **federated + center-led hybrid**:
- **Federated:** Business domains (Merchandising, Supply Chain, Marketing, Finance) own their data — they define what "correct" means for their domain and are accountable for quality.
- **Center-led:** A central Data Office (CDO function) sets standards, tooling, and cross-domain policy — and resolves conflicts when domains disagree.

This avoids two failure modes:
- **Fully centralized:** Data team becomes a bottleneck; business loses ownership; quality deteriorates because "IT owns it"
- **Fully federated:** Metrics diverge; no cross-domain trust; data swamp forms in the lake

---

## Organizational structure

```
Chief Data Officer (CDO)
│
├── Data Platform & Engineering (EDP, MDM, pipelines)
│
├── Data Governance & Quality (standards, stewardship, lineage)
│
├── Analytics & BI (Power BI, semantic layer, self-service)
│
└── AI / ML Product (use cases, model governance, UCP)
    │
    ├── Data PM (Merchandising + Supply Chain)
    ├── Data PM (Customer + Marketing)
    ├── BI PM (Enterprise BI + Self-Service)
    └── Business Analysts (embedded per domain)
```

---

## Data ownership & stewardship RACI

| Role | Accountable for | Responsible for | Consulted on | Informed of |
|---|---|---|---|---|
| **Domain Data Owner** (VP-level) | Data policy for their domain | Approving attribute definitions, SLAs | Cross-domain decisions | Quality scorecard weekly |
| **Data Steward** (Sr. Analyst) | Daily quality enforcement | Flagging quality issues, resolving conflicts | New source onboarding | Pipeline failures within 1hr |
| **Data Custodian** (Data Engineer) | Pipeline reliability | Building + monitoring pipelines | Schema changes | SLA breaches |
| **Data Consumer** (Analyst, PM) | Using certified data | Filing data quality tickets | New dataset requests | Dataset deprecation 30d notice |
| **CDO / Data Office** | Enterprise standards | Policy setting, conflict resolution | All major decisions | Monthly quality scorecard |

### Domain Data Owners by domain

| Domain | Data Owner | Steward | Key Datasets |
|---|---|---|---|
| Merchandising | VP Merchandising | Sr. Analyst, Merch Analytics | Product MDM, Assortment, Pricing |
| Supply Chain | VP Supply Chain | Sr. Analyst, SC Analytics | Vendor MDM, PO, Inventory |
| Stores | VP Store Operations | Sr. Analyst, Store Analytics | Store MDM, POS transactions |
| Customer & Marketing | VP Marketing | Sr. Analyst, CRM | CDP profiles, Loyalty, Campaigns |
| Finance | VP Finance | Sr. Financial Analyst | P&L, Margin, Cost |

---

## Data quality SLAs

### Tier 1 — Mission-critical (real-time operations)

| Dataset | Completeness SLA | Accuracy SLA | Freshness SLA | Consequence of breach |
|---|---|---|---|---|
| Product pricing (active SKUs) | >99.5% | >99.9% | <5 min | Incorrect pricing in UCP / POS / e-comm |
| Store inventory levels | >99% | >98% | <15 min | Stockout errors, incorrect allocation |
| Product availability flags | >99.5% | >99.9% | <5 min | Selling discontinued items |

### Tier 2 — Business-critical (daily operations)

| Dataset | Completeness SLA | Accuracy SLA | Freshness SLA |
|---|---|---|---|
| Product MDM (full attributes) | >97% | >99% | <4 hours |
| Customer unified profiles (CDP) | >90% | >97% | <1 hour |
| Vendor MDM | >95% | >98% | <24 hours |
| Store MDM | >99% | >99% | <24 hours |

### Tier 3 — Analytical (reporting and AI)

| Dataset | Completeness SLA | Accuracy SLA | Freshness SLA |
|---|---|---|---|
| Historical sales (Gold layer) | >98% | >99% | Daily by 6am ET |
| Customer segments (CDP) | >95% | >97% | Daily |
| AI model training datasets | >97% | >99% | Weekly refresh |

---

## Data quality monitoring

### Automated checks (run in Unity Catalog pipeline)

Every certified dataset runs the following checks on every refresh:

```
✓ Null check           → Flag columns with null rate > threshold
✓ Range check          → Flag numeric values outside expected bounds
✓ Referential check    → Flag orphan records (e.g., SKU with no product MDM record)
✓ Freshness check      → Alert if dataset hasn't refreshed within SLA window
✓ Volume check         → Alert if record count drops >10% from 7-day average (data loss signal)
✓ Duplicate check      → Flag duplicate primary keys
✓ Format check         → Flag malformed emails, phone numbers, zip codes
```

### Escalation protocol

```
Level 1: Automated alert → Data Custodian (pipeline fix within 1 hour)
Level 2: SLA breach >2 hours → Data Steward notified, incident ticket opened
Level 3: SLA breach >4 hours (Tier 1 data) → Domain Data Owner notified, P0 incident
Level 4: Business impact confirmed → CDO notified, cross-functional war room
```

---

## Decision rights framework

### What requires Domain Data Owner approval
- Adding or removing a field from the certified product / customer / store MDM schema
- Changing the survivorship rule for any golden record attribute
- Onboarding a new source system to the EDP
- Deprecating a certified dataset (30-day notice required)

### What requires CDO / Data Office approval
- Cross-domain attribute ownership disputes
- Changes to the enterprise data classification policy (PII, confidential, public)
- Approving a new AI use case for production deployment
- Unity Catalog RBAC role changes above analyst level
- Any data sharing with external vendors or partners

### What Data Stewards can decide independently
- Flagging and quarantining bad records (with notification to custodian)
- Approving new analyst access to existing certified datasets
- Scheduling ad-hoc data quality audits

---

## Data literacy program

Self-service analytics only works if business users trust and understand the data. Year 2 launches:

| Program | Format | Audience | Cadence |
|---|---|---|---|
| Data Office Hours | 60-min virtual session | All business analysts | 2x per week |
| Data Certification (Power BI) | Self-paced + assessment | All business users | Ongoing |
| New Dataset Walkthrough | 30-min recorded demo | Data consumers | Each new certified dataset |
| Monthly Data Quality Scorecard | Email report | All Data Owners | Monthly |
| Annual Data Governance Review | All-hands with CDO | All stakeholders | Annual |

---

## Governance tool stack

| Tool | Purpose |
|---|---|
| **Databricks Unity Catalog** | Centralized governance, lineage, access control, data discovery |
| **Great Expectations** | Automated data quality checks in pipelines |
| **Jira** | Data quality ticket tracking and SLA management |
| **Confluence** | Data dictionary, stewardship policies, decision log |
| **Power BI + Databricks** | Quality scorecard dashboards for Data Owners |
