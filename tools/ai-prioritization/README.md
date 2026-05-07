# Retail AI Use Case Prioritization Framework

A product management tool for scoring, ranking, and managing an AI use case backlog — built for retail organizations investing in ML and LLM capabilities.

**Live demo context:** Designed around a real Five Below Data & AI strategy with 11 pre-loaded use cases spanning merchandising, supply chain, store operations, and customer analytics.

---

## What it does

| Tab | Description |
|-----|-------------|
| **Dashboard** | Ranked backlog of all AI use cases with tier badges, expandable detail cards, and score breakdowns |
| **Priority Matrix** | 2×2 Impact vs. Effort scatter plot (bubble size = total score) + domain distribution chart |
| **Add Use Case** | Form with 5-dimension scoring sliders to submit new use cases mid-session |
| **Value Hypothesis** | Auto-generated value hypothesis doc + A/B test template + AI Review Council submission download |

## Scoring framework

Each use case is rated 1–5 on four dimensions:

| Dimension | What it measures |
|-----------|-----------------|
| **Business Impact** | Revenue lift, cost savings, or risk reduction potential |
| **Data Readiness** | Is required data clean, available, and governed? |
| **Technical Feasibility** | Model complexity, latency requirements, integration scope |
| **Speed to Value** | How fast can we reach a production MVP? |

**Tier logic:**
- 🟢 **Tier 1** (≥15/20) — Fund and staff immediately
- 🟡 **Tier 2** (11–14/20) — Roadmap for next planning cycle
- 🔴 **Tier 3** (≤10/20) — Parking lot; revisit when data/tech matures

## Pre-loaded use cases (Five Below retail AI backlog)

1. LLM Store Associate Agent — 19/20 🟢
2. Markdown Optimization ML — 17/20 🟢
3. Demand Sensing & Inventory Allocation — 16/20 🟢
4. UCP Catalog Exposure (Google AI Mode) — 15/20 🟢
5. Churn Prediction & Win-Back — 15/20 🟢
6. Personalized Recommendations — 14/20 🟡
7. Automated Vendor Scorecards — 14/20 🟡
8. Fraud Detection (E-commerce) — 14/20 🟡
9. Dynamic Clearance Pricing — 13/20 🟡
10. Real-Time Customer Chat — 13/20 🟡
11. Shrink / Loss Prevention ML — 11/20 🟡

## Setup

```bash
git clone https://github.com/KKThella/retail-ai-prioritization.git
cd retail-ai-prioritization
pip install -r requirements.txt
streamlit run app.py
```

App opens at `http://localhost:8501`

## Features

- **Domain filter** — sidebar filter by business domain (Merchandising, Supply Chain, Store Ops, etc.)
- **CSV export** — download full scored backlog as CSV for stakeholder distribution
- **Reset to defaults** — restore pre-loaded Five Below use cases at any time
- **Value hypothesis generator** — structured output with business problem, AI approach, success metrics, A/B test design, and AI Review Council submission form
- **Responsive charts** — Plotly scatter and bar charts with hover tooltips

## Tech stack

- **Streamlit** — UI framework
- **Plotly** — interactive charting (scatter, bar)
- **Pandas** — data manipulation and CSV export
- **Python 3.9+**

## PM context

This tool operationalizes the AI use case intake → scoring → prioritization process described in enterprise AI governance frameworks. It mirrors the AI Review Council workflow where use cases are evaluated on business impact, data readiness, technical feasibility, and time-to-value before PoC approval.

The scoring model is adapted from real retail AI prioritization work and maps directly to the kind of structured intake process a Chief Data Officer or VP of Product would run before committing engineering resources to ML model development.

---

*Built by [Kiran Thella](https://www.linkedin.com/in/kiranthella/) — AI Product Manager | Data & AI Strategy*
