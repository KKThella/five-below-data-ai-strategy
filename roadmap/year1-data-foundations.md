# Year 1 — Data Foundations: MDM + Enterprise Data Platform

> **Theme:** Trust the data. You cannot personalize, optimize, or expose data to AI agents if the data is wrong.

---

## The problem Five Below needs to solve first

Five Below likely has:
- **Multiple product identifiers** across POS, e-commerce, wholesale, and merchandising systems — same SKU, different codes, no single golden record
- **Store data fragmentation** — store attributes (size, format, demographics, local assortment) living in disconnected spreadsheets and legacy systems
- **Vendor data inconsistency** — lead times, MOQs, compliance status managed manually with no central vendor master
- **No unified customer identity** — loyalty, e-commerce, and in-store transactions not linked at the person level

The result: every downstream team (merchandising, marketing, supply chain, e-commerce) builds their own "source of truth" spreadsheet. Analytics diverges. AI models trained on dirty data make bad recommendations. UCP catalog exposure exposes wrong prices and stale availability.

**Year 1 fixes the foundation.**

---

## 1. Master Data Management (MDM)

### What we're building

A governed, unified master record for Five Below's three core business entities:

#### Product MDM
| Attribute Group | Key Attributes | Source Systems |
|---|---|---|
| Identity | SKU, UPC, GTIN, internal item ID | POS, e-comm, WMS |
| Hierarchy | Category, subcategory, department, brand | Merchandising system |
| Content | Product name, description, images, attributes | Vendor feeds, manual |
| Pricing | Base price, promo price, markdown rules | Pricing system |
| Availability | Active/inactive, seasonal flags, store eligibility | Inventory system |

**Data quality SLAs:** completeness >97%, accuracy >99%, freshness <4 hours for pricing/availability

#### Store MDM
| Attribute Group | Key Attributes |
|---|---|
| Identity | Store ID, name, address, geo coordinates |
| Format | Store size (sq ft), format type, opening date |
| Operations | Store hours, manager, district, region |
| Performance | Volume tier, traffic profile, local demographics |

#### Vendor MDM
| Attribute Group | Key Attributes |
|---|---|
| Identity | Vendor ID, legal name, DBA, tax ID |
| Logistics | Lead time, MOQ, country of origin, Incoterms |
| Compliance | Vendor scorecard, certification status, audit history |
| Financial | Payment terms, rebate structures, cost tiers |

### MDM Platform: Build vs. Buy decision

**Decision: Buy** — Reltio Cloud or Profisee (evaluate both)

| Criteria | Reltio | Profisee | Build |
|---|---|---|---|
| Time to value | 6–9 months | 4–6 months | 18–24 months |
| Retail depth | High | Medium | N/A |
| Unity Catalog integration | Yes | Yes | Custom |
| Total cost (3yr) | $2.4M | $1.8M | $4M+ |
| **Recommendation** | ✓ If scale priority | ✓ If speed priority | ✗ |

**Q1 action:** Issue RFP to both vendors. Score on: data model flexibility, Unity Catalog connector, retail reference customers, implementation timeline.

### MDM governance model

```
Data Domain Owner (VP Merchandising / VP Supply Chain)
    ↓ owns policy
Data Steward (Sr. Analyst per domain)
    ↓ enforces quality
Data Custodian (Engineering)
    ↓ maintains pipelines
```

- **Decision rights:** Domain owners approve any change to master attribute definitions. Stewards approve new source system onboarding. Engineering owns SLA monitoring.
- **Conflict resolution:** When two source systems disagree on a product attribute, the MDM survivorship rule (configured per attribute) determines the golden record. Conflicts escalate to domain steward within 24 hours.

---

## 2. Enterprise Data Platform (EDP)

### Architecture: Databricks Lakehouse on Azure

```
                    SOURCE SYSTEMS
    ┌─────────┬──────────┬──────────┬──────────┐
    │  POS    │ E-Comm   │  WMS     │  Vendor  │
    │ (store) │(Shopify) │(Manhattan│  Feeds   │
    └────┬────┴────┬─────┴────┬─────┴────┬─────┘
         │         │          │          │
         └─────────┴──────────┴──────────┘
                        │
                   Fivetran / CDC
                        │
              ┌─────────▼──────────┐
              │    Bronze Layer     │  Raw ingestion, full history
              │   (Delta Lake)      │  SLA: <15 min latency
              └─────────┬──────────┘
                        │
              ┌─────────▼──────────┐
              │    Silver Layer     │  Cleaned, conformed, MDM-joined
              │  (Unity Catalog)    │  Data quality checks run here
              └─────────┬──────────┘
                        │
              ┌─────────▼──────────┐
              │     Gold Layer      │  Business-ready aggregates
              │  (Semantic Layer)   │  KPIs, metrics, BI-ready
              └─────────┬──────────┘
                        │
           ┌────────────┴────────────┐
           │                         │
    ┌──────▼──────┐          ┌───────▼──────┐
    │  Power BI   │          │  AI / ML     │
    │  (reports)  │          │  (Databricks │
    │             │          │   ML Runtime)│
    └─────────────┘          └──────────────┘
```

### Unity Catalog as the governance layer

Unity Catalog provides:
- **Centralized access control** — row/column level security, role-based access
- **Data lineage** — end-to-end lineage from source to BI dashboard
- **Data discovery** — business users can search and find certified datasets
- **Audit logging** — who accessed what, when

**Year 1 Unity Catalog setup:**
1. Define catalog hierarchy: `fivebelow_prod.{domain}.{table}`
   - Domains: `merchandising`, `supply_chain`, `stores`, `customers`, `finance`
2. Tag all PII fields (customer name, email, address) with `pii=true`
3. Configure RBAC: analyst, steward, engineer, executive roles
4. Certify first 20 "golden datasets" with steward sign-off

### Year 1 EDP delivery milestones

| Quarter | Milestone | Success Metric |
|---|---|---|
| Q1 | Databricks + Unity Catalog provisioned; Fivetran connectors live for POS, WMS, e-comm | Data flowing, no manual extracts |
| Q2 | Bronze + Silver layers live for all 3 MDM domains | <15 min latency, >99% pipeline uptime |
| Q3 | Gold layer + Power BI semantic model for merchandising KPIs | First self-service dashboard live |
| Q4 | Full data governance operating model active; stewardship RACI signed off | DQ SLAs met for all certified datasets |

---

## Year 1 investment summary

| Line item | Estimated cost |
|---|---|
| MDM platform (Profisee/Reltio) | $600K–$800K/year |
| Databricks + Unity Catalog | $800K–$1.2M/year |
| Fivetran (connectors) | $150K/year |
| Implementation partner (SI) | $1.5M one-time |
| Internal headcount (2 data engineers, 1 data steward) | $450K/year |
| **Total Year 1** | **~$3.5M–$4.1M** |

**Expected Year 1 ROI drivers:**
- Eliminate 40+ manual reporting spreadsheets across merchandising and supply chain → estimated $1.5M in analyst time savings
- Reduce pricing/inventory errors from data mismatches → estimated $3–5M in margin protection
- Foundation enabling Year 2 CDP and personalization ($15–20M revenue opportunity)
