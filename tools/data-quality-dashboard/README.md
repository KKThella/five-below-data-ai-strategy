# Retail Data Quality Governance Dashboard

An operational Streamlit dashboard that brings a retail enterprise data governance framework to life — covering data quality SLA monitoring, stewardship accountability, automated checks, escalation protocol, and decision rights.

**Built for:** Five Below's federated + center-led data governance model across a Databricks Unity Catalog platform.

---

## What it does

| Tab | Description |
|-----|-------------|
| **SLA Monitor** | Live view of Completeness, Accuracy, and Freshness SLAs for all 9 certified datasets — with pass/warn/breach status badges and expandable detail cards |
| **RACI Explorer** | Full stewardship RACI (Accountable / Responsible / Consulted / Informed) by role, plus Domain Data Owner assignments per business domain |
| **Automated Checks** | 7-check pipeline suite that runs on every dataset refresh in Unity Catalog — null, range, referential, freshness, volume, duplicate, format |
| **Escalation Protocol** | 4-level escalation ladder from automated alert (Level 1) to CDO war room (Level 4) — with active incident tracker |
| **Decision Rights** | Decision authority matrix defining what requires Domain Owner vs CDO vs Steward approval |

## Datasets monitored

**Tier 1 — Mission Critical (real-time)**
- Product Pricing (active SKUs) — SLA: 99.5% complete, <5 min freshness
- Store Inventory Levels — SLA: 99% complete, <15 min freshness
- Product Availability Flags — SLA: 99.5% complete, <5 min freshness

**Tier 2 — Business Critical (daily operations)**
- Product MDM (full attributes)
- Customer Unified Profiles (CDP)
- Vendor MDM
- Store MDM

**Tier 3 — Analytical (reporting and AI)**
- Historical Sales (Gold Layer)
- Customer Segments (CDP)
- AI Model Training Datasets

## Setup

```bash
cd tools/data-quality-dashboard
pip install -r requirements.txt
streamlit run app.py
```

App opens at `http://localhost:8501`

## Governance model

This dashboard operationalizes a **federated + center-led hybrid** governance model:

- **Federated:** Business domains (Merchandising, Supply Chain, Marketing, Finance) own their data — they define correctness and are accountable for quality
- **Center-led:** A central Data Office (CDO function) sets standards, tooling, and cross-domain policy

**Tool stack:** Databricks Unity Catalog · Great Expectations · Jira · Confluence · Power BI

## Tech stack

- **Streamlit** — UI framework
- **Plotly** — interactive bar charts with hover tooltips
- **Pandas** — RACI and dataset tables

---

*Built by [Kiran Thella](https://www.linkedin.com/in/kiranthella/) — AI Product Manager | Data & AI Strategy*
