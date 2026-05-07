# Five Below — Data & AI Strategy

> A complete product strategy and toolset for transforming Five Below's data and AI capabilities across a 3-year horizon.

This repository captures the end-to-end vision, roadmap, governance frameworks, and working tools I developed to demonstrate how a value retailer like Five Below can move from fragmented data assets to an enterprise-wide AI platform — and ultimately compete in the emerging era of agentic commerce.

---

## Strategic thesis

**The problem:** Five Below has ~1,100 stores, $3.6B in revenue, and a cult-favorite value brand. But its data infrastructure is fragmented — siloed merchandising systems, no unified customer profile, and AI capabilities that are largely aspirational. Meanwhile, Google's Universal Commerce Protocol (UCP) is reshaping how AI agents discover and purchase products. If Five Below's catalog isn't clean, real-time, and UCP-compliant by 2027, they don't exist in that shopping moment.

**The opportunity:** Five Below's price-to-fun ratio makes it *exactly* the merchant AI shopping agents will recommend when customers ask for affordable, trend-right products. The question is whether the data foundation will be ready to capitalize.

**The thesis:** Three years, three phases.

| Year | Theme | Core Deliverable |
|------|-------|-----------------|
| **Year 1** | Trust the data | Enterprise Data Platform (EDP) + Master Data Management (MDM) |
| **Year 2** | Know the customer | Customer Data Platform (CDP) + Self-Service BI |
| **Year 3** | Win in agentic commerce | Enterprise AI use cases + UCP catalog exposure |

---

## Three-year roadmap

### Year 1 — Data Foundations
**Goal:** One version of truth for product, store, vendor, and customer data.

- Databricks Lakehouse (Bronze → Silver → Gold layers) on Azure
- Profisee MDM for Product, Store, and Vendor master data
- Unity Catalog for governance, lineage, and access control
- Real-time POS feed (<15 min latency) replacing nightly batch
- **Investment:** ~$3.5–4.1M | **Target:** 99.5% product data accuracy, <5 min pricing freshness

📄 [Year 1 Detailed Roadmap](roadmap/year1-data-foundations.md)

### Year 2 — Customer Intelligence
**Goal:** Know every customer — unified profile, actionable segments, self-service analytics.

- Customer Data Platform (CDP) — unified buyer profile across POS, e-comm, loyalty, and email
- 5 AI-ready customer segments (Champions, Loyalists, At-Risk, Seasonal, New)
- Power BI + Databricks semantic layer for self-service reporting
- KPI framework across Merchandising, Supply Chain, Store Ops, and Customer
- **Investment:** ~$4.2–5.1M | **Target:** 90% customer match rate, 50% reduction in ad-hoc analytics requests

📄 [Year 2 Detailed Roadmap](roadmap/year2-customer-intelligence.md)

### Year 3 — Agentic Commerce
**Goal:** AI use cases in production + catalog exposure to Google AI Mode and Gemini shopping agents.

**Tier 1 AI use cases (H1 launch):**
- 🏆 LLM Store Associate Agent — $6M labor productivity gain
- 📉 Markdown Optimization ML — $18M annual margin improvement
- 📦 Demand Sensing & Inventory Allocation — $20M combined impact
- 🔁 Churn Prediction & Win-Back — $12M recovered LTV

**UCP Revenue Opportunity:** $33–52M incremental revenue from Google AI Mode catalog exposure

**3-year ROI:** $92–111M in value against $22–28M in platform investment = **4–5x ROI**

📄 [Year 3 Detailed Roadmap](roadmap/year3-agentic-commerce.md)

---

## AI strategy

### Use case inventory & prioritization
12 use cases scored across Impact, Data Readiness, Feasibility, and Speed to Value (1–5 each, /20 total). Tier 1 threshold: ≥15.

📄 [Use Case Inventory](ai-strategy/use-case-inventory.md)

### AI governance framework
5-stage intake process: Idea Submission → AI Review Council → PoC → Production Readiness Review → Continuous Monitoring. Includes model card template, responsible AI guardrails by use case type, and ethics review triggers.

📄 [AI Governance Framework](ai-strategy/ai-governance-framework.md)

---

## Data governance

### Operating model
Federated + center-led hybrid governance. Domain Data Owners (VP-level) own quality for their domain; the central Data Office (CDO function) sets standards and resolves cross-domain conflicts. Includes full RACI, Tier 1/2/3 data quality SLAs, automated DQ checks, and 4-level escalation protocol.

📄 [Data Governance Operating Model](data-governance/operating-model.md)

---

## Tools

Operational tools built to demonstrate how these strategies get executed — not just theorized.

### AI Use Case Prioritization Framework
> `tools/ai-prioritization/`

Interactive Streamlit app for scoring, ranking, and managing a retail AI use case backlog. Pre-loaded with 11 Five Below use cases. Features: ranked dashboard with tier badges, 2×2 priority matrix (Impact vs. Effort), value hypothesis generator, A/B test template builder, and AI Review Council submission download.

```bash
cd tools/ai-prioritization
pip install -r requirements.txt
streamlit run app.py
```

📂 [AI Prioritization Tool](tools/ai-prioritization/)

### Data Quality Governance Dashboard *(coming soon)*
> `tools/data-quality-dashboard/`

Streamlit dashboard operationalizing the Tier 1/2/3 SLA framework — real-time DQ signal monitoring, stewardship RACI explorer, 4-level escalation tracker, and Unity Catalog dataset health scorecard.

### UCP Readiness Scorecard *(coming soon)*
> `tools/ucp-scorecard/`

Interactive scorecard assessing a retailer's readiness for Google Universal Commerce Protocol compliance — catalog completeness, pricing feed latency, inventory freshness, checkout API, and post-purchase integration.

---

## Tech stack

| Layer | Technology |
|-------|-----------|
| Data Platform | Databricks Lakehouse (Bronze/Silver/Gold), Azure Data Lake |
| Governance | Databricks Unity Catalog, Great Expectations |
| MDM | Profisee (Product, Store, Vendor) |
| CDP | Salesforce Data Cloud / mParticle |
| BI | Power BI + Databricks Semantic Layer |
| AI/ML | Databricks ML Runtime, Azure OpenAI (LLMs), scikit-learn |
| LLM | RAG-based agents grounded on Product MDM + Policy docs |
| UCP | FastAPI layer on EDP Gold, Google UCP Gateway |
| Tools | Python, Streamlit, Plotly, pandas |

---

## About

Built by **Kiran Thella** — AI Product Manager with 13+ years of experience driving data platform and AI product strategy at Nike, Gilead Sciences, and eBay.

- 🔗 [LinkedIn](https://www.linkedin.com/in/kiranthella/)
- 💼 [GitHub](https://github.com/KKThella)
