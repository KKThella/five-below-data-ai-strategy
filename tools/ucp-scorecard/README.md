# UCP Readiness Scorecard

An interactive Streamlit tool that assesses a retailer's readiness for **Google's Universal Commerce Protocol (UCP)** — the open standard enabling AI agents (Google AI Mode, Gemini, Perplexity, Microsoft Copilot) to discover, evaluate, and purchase products through conversational interfaces.

**Live demo context:** Pre-configured for Five Below's current state vs. Year 3 target, with competitive benchmarking against Walmart, Target, Dollar Tree, and Dollar General.

---

## What is UCP?

Google's Universal Commerce Protocol (launched January 2026, co-developed with Walmart, Target, Best Buy, and Home Depot) enables AI shopping agents to:

1. **Discover** products via natural language queries
2. **Retrieve** real-time pricing, availability, and product details
3. **Add to cart** and complete checkout programmatically
4. **Manage post-purchase** (order status, returns, exchanges)

A shopper asking Gemini *"find me fun gifts under $10 for a 7-year-old"* will surface products from UCP-compliant merchants — and skip retailers whose catalogs aren't connected.

---

## Scoring framework

The scorecard rates readiness across three dimensions (100 points total):

| Dimension | Points | What it measures |
|-----------|--------|-----------------|
| **Catalog Quality** | /40 | Completeness, taxonomy, images, attributes, GTIN coverage |
| **Real-Time Feed Readiness** | /25 | Pricing freshness (<5min SLA), inventory freshness (<15min SLA) |
| **UCP Endpoint Coverage** | /35 | 7 API endpoints from product search through post-purchase returns |

**Readiness tiers:**
- 🟢 **Excellent** (85–100) — UCP Ready; proceed to certification
- 🔵 **Good** (65–84) — Mostly ready; close remaining endpoint gaps
- 🟡 **Fair** (40–64) — Significant gaps; prioritize data foundation
- 🔴 **Poor** (0–39) — Not UCP ready; start with MDM and EDP

---

## What's inside (5 tabs)

| Tab | Description |
|-----|-------------|
| **Catalog Assessment** | Radar chart across 10 catalog dimensions + feed freshness scoring |
| **Endpoint Gap Analysis** | 7 UCP endpoints with status (Built/Partial/Missing), build effort, and donut coverage chart |
| **Revenue Opportunity** | Waterfall model: baseline → UCP conversion lift → new customer revenue; 3-scenario table |
| **Competitive Landscape** | Scatter plot of UCP score vs. catalog completeness vs. key competitors |
| **Remediation Roadmap** | 4-phase plan with score progression chart, action items, and investment/ROI summary |

---

## Setup

```bash
cd tools/ucp-scorecard
pip install -r requirements.txt
streamlit run app.py
```

App opens at `http://localhost:8501`

Use the sidebar to adjust all inputs — all charts and scores update in real time.

---

## Key features

- **Live scoring** — adjust catalog %, feed freshness, and endpoint status in sidebar; scorecard recalculates instantly
- **Revenue opportunity model** — configurable annual revenue, online %, and AI search share inputs
- **Competitive benchmarking** — Five Below vs. Walmart, Target, Dollar Tree, Dollar General
- **Cost of inaction** — year-by-year revenue at risk if UCP launch is delayed
- **Download assessment** — export full scorecard as a structured Markdown report

---

## UCP endpoints covered

| Endpoint | Purpose | Complexity |
|----------|---------|-----------|
| `/products/search` | Semantic NL search for AI agents | High |
| `/products/{sku}/availability` | Real-time store + online inventory | Medium |
| `/products/{sku}/price` | Live pricing + promo eligibility | Medium |
| `/cart/add` | Agentic add-to-cart | High |
| `/checkout/initiate` | UCP payment handoff | Very High |
| `/orders/{id}/status` | Post-purchase tracking | Medium |
| `/returns/initiate` | Agentic return flow | High |

---

## Tech stack

- **Streamlit** — UI and sidebar controls
- **Plotly** — gauge chart, radar chart, waterfall, scatter, donut, line chart
- **Pandas** — data tables and scenario modeling
- **Python 3.9+**

---

*Built by [Kiran Thella](https://www.linkedin.com/in/kiranthella/) — AI Product Manager | Data & AI Strategy*
