# Year 3 — Agentic Commerce: Enterprise AI + UCP

> **Theme:** Win in agentic commerce. AI use cases at scale + catalog exposure to AI shopping agents.

---

## The agentic commerce reality by 2027

By the time Five Below completes Year 1–2 data foundations, the retail landscape will have shifted significantly:

- **Google UCP** will be live across 20+ major retail partners (Walmart, Target, Best Buy, Home Depot already signed)
- **AI Mode in Google Search** and **Gemini** will handle an estimated 30–40% of product discovery queries
- Shoppers will ask *"find me fun tech gadgets under $5 for my kid's birthday"* and an AI agent will complete the purchase across UCP-compliant merchants — without the shopper ever visiting a product page

**Five Below's risk:** If their catalog isn't UCP-compliant with clean, real-time product data, pricing, and availability — they don't exist in that shopping moment.

**Five Below's opportunity:** As a value retailer with extraordinary price-to-fun ratio, Five Below is *exactly* the merchant AI shopping agents will recommend when shoppers ask for affordable, trend-right products. The UCP moment is a gift — if the data foundation is ready.

---

## 1. Enterprise AI Use Case Strategy

### AI use case prioritization framework

Each use case is evaluated on four dimensions (1–5 scale):
- **Business impact** — revenue lift, cost savings, or risk reduction potential
- **Data readiness** — is the required data clean, available, and governed? (requires Year 1–2)
- **Technical feasibility** — model complexity, latency requirements, integration scope
- **Time to value** — how fast can we get to a production MVP?

### Prioritized AI use case backlog (Year 3)

#### Tier 1 — High impact, Year 3 H1 launch

**1. AI-Powered Markdown Optimization**
- **Problem:** Five Below marks down ~$180M of inventory annually. Current markdown decisions are rule-based and manual, leading to over-marking (margin loss) or under-marking (dead stock).
- **AI approach:** ML model predicting sell-through probability by SKU × store × week. Model inputs: sell-through velocity, weeks remaining in season, local competitor pricing, store traffic forecasts.
- **Value hypothesis:** 10% reduction in markdown spend = $18M annual margin improvement. 5% reduction in dead stock = $9M in inventory recovery.
- **Success metrics:** Sell-through rate improvement (baseline vs. AI-recommended); margin per unit vs. control group; analyst adoption rate.
- **Data requirements:** 3 years of SKU-level sales history (from EDP), store-level traffic (from store ops), seasonal flags (from MDM). ✓ Available after Year 1.

**2. Demand Sensing & Inventory Allocation**
- **Problem:** Five Below replenishes on historical averages. When a product goes viral (TikTok effect), stores stock out in 48 hours. When a product misses, stores sit on 20 weeks of supply.
- **AI approach:** Real-time demand signal aggregation (POS velocity + social trend signals + search volume) feeding a store-level allocation recommendation engine.
- **Value hypothesis:** 3% in-stock rate improvement = ~$12M in recovered sales. 10% reduction in overstock = $8M inventory cost savings.
- **Success metrics:** In-stock rate by tier (viral, trending, steady, declining); inventory turn improvement; stockout frequency.
- **Data requirements:** Real-time POS feeds (EDP Bronze, <15 min), social API signals, store MDM attributes. ✓ Available after Year 1.

**3. LLM-Powered Store Associate Support Agent**
- **Problem:** Store associates spend 20–30% of their time answering customer questions they can't answer (product availability at other locations, return policies, promotions). This drives customer dissatisfaction and reduces floor time.
- **AI approach:** RAG-based LLM agent on store-facing device, grounded on Product MDM, store inventory, promotions, and policy documents. Associates query in plain English.
- **Value hypothesis:** 15% reduction in customer escalations = better NPS. 20% reduction in associate time on lookups = more floor time = estimated $6M in labor productivity.
- **Success metrics:** Query resolution rate (% answered without human escalation); associate adoption; NPS delta in pilot stores.
- **Data requirements:** Product MDM, store inventory (real-time), promotions database, policy documents. ✓ Available after Year 1.

#### Tier 2 — High impact, Year 3 H2 launch

**4. Personalized Product Recommendations (E-commerce + Loyalty)**
- **AI approach:** Collaborative filtering + content-based hybrid model on CDP unified customer profiles. "Because you bought Bluetooth earbuds, you might love these wireless charging pads."
- **Value hypothesis:** 8–12% lift in AOV = $4–6M incremental e-commerce revenue.

**5. Customer Churn Prediction & Win-Back**
- **AI approach:** ML churn model on CDP behavioral signals (days since purchase, frequency decline, category shift). Trigger win-back campaigns 2–3 weeks before predicted churn.
- **Value hypothesis:** 5% reduction in lapsed customers = $10–15M in recovered LTV.

**6. Dynamic Pricing for Clearance**
- **AI approach:** Reinforcement learning model optimizing clearance prices daily (within guardrails) to maximize sell-through while protecting margin floor.
- **Value hypothesis:** 8% improvement in clearance sell-through = $7M margin recovery.

---

## 2. Universal Commerce Protocol (UCP) Strategy

### What UCP means for Five Below

Google's Universal Commerce Protocol (launched January 2026, co-developed with Walmart, Target, Best Buy, Home Depot) enables AI shopping agents to:
1. **Discover** products via natural language queries
2. **Retrieve** real-time pricing, availability, and product details
3. **Add to cart** and complete checkout programmatically
4. **Manage post-purchase** (order status, returns, exchanges)

For Five Below: a shopper asking Gemini *"what's a fun gift under $10 for a 7-year-old?"* will result in an AI agent querying UCP-compliant merchants and surfacing Five Below products — **if and only if** Five Below's catalog data is clean, real-time, and UCP-compliant.

### UCP readiness requirements

| Requirement | Current State (est.) | Year 3 Target | Dependency |
|---|---|---|---|
| Product catalog completeness | ~65% | >97% | Year 1 MDM |
| Real-time pricing feed (<5 min) | Batch (24hr) | <5 min | Year 1 EDP |
| Real-time inventory by store | Batch (nightly) | <15 min | Year 1 EDP |
| Product images (all SKUs) | ~70% | >98% | Year 1 MDM |
| Category taxonomy (Google-compatible) | Partial | Full | Year 1 MDM |
| Checkout API (cart + payment) | E-comm only | UCP-compliant endpoint | Year 3 Build |

### UCP endpoint architecture

```
Five Below EDP (Gold Layer)
         │
    UCP API Layer (FastAPI)
    ┌────────────────────────────────┐
    │  /products/search              │  Semantic search on catalog
    │  /products/{sku}/availability  │  Real-time inventory by store
    │  /products/{sku}/price         │  Current price + promo eligibility
    │  /cart/add                     │  Add to cart (UCP standard)
    │  /checkout/initiate            │  UCP payment handoff
    │  /orders/{id}/status          │  Post-purchase tracking
    └────────────────────────────────┘
         │
    Google UCP Gateway
    (AI Mode in Search, Gemini, third-party agents)
```

**Build vs. Buy:** Build the UCP endpoint (thin API layer) on top of the Year 1 EDP. No vendor provides a Five Below-specific UCP wrapper. This is a 3–4 month engineering investment once Year 1 data foundations are live.

### UCP business case

| Scenario | Assumption | Revenue Impact |
|---|---|---|
| AI search captures 5% of Five Below's addressable online market | AI Mode handles 30% of product queries by 2027; Five Below currently captures ~2% of value shoppers online | $20–30M incremental revenue |
| UCP cart conversion rate is 40% higher than organic search | Reduced friction (no site visit required) | $8–12M lift |
| New customer acquisition via AI agents | AI agents surface Five Below to shoppers who wouldn't have searched organically | $5–10M new customer revenue |
| **Total UCP revenue opportunity (Year 3)** | | **$33–52M** |

---

## 3. AI Governance Framework (Year 3 Operating Model)

As AI use cases move to production, Five Below needs guardrails:

### AI intake and review process

```
Business team identifies AI use case
         │
AI Use Case Assessment Form submitted
(impact hypothesis, data requirements, bias risk, explainability needs)
         │
    ┌────▼─────┐
    │  AI Review │  Monthly cadence
    │  Council   │  CPO + CDO + Legal + Privacy + Engineering leads
    └────┬─────┘
         │
    ┌────▼──────────┐    ┌─────────────────┐
    │   Approved    │    │ Needs revision  │
    │   for PoC     │    │ (bias concern,  │
    └────┬──────────┘    │  data gap, etc) │
         │               └─────────────────┘
    PoC (6–8 weeks)
         │
    ┌────▼──────────────┐
    │ Production Review │  Model card required:
    │                   │  - Accuracy metrics
    │                   │  - Bias assessment
    │                   │  - Explainability approach
    │                   │  - Monitoring plan
    └────┬──────────────┘
         │
    Production deployment
    (with A/B test + rollback plan)
```

### Responsible AI guardrails

| Risk Area | Guardrail |
|---|---|
| Pricing bias | No model can recommend prices that discriminate by customer demographics |
| Inventory allocation fairness | Store allocation models must not disadvantage lower-income zip codes |
| Model drift | All production models monitored weekly; alert if accuracy drops >5% from baseline |
| Explainability | Any model affecting a customer-facing decision must have a human-readable explanation |
| Data minimization | AI models use minimum required customer attributes; no unnecessary PII |

---

## Year 3 investment summary

| Line item | Estimated cost |
|---|---|
| Databricks ML Runtime + AI capabilities | $400K incremental/year |
| Azure OpenAI (LLM use cases) | $300K/year (usage-based) |
| UCP endpoint development (engineering) | $600K one-time |
| AI/ML team (2 ML engineers, 1 AI PM) | $650K/year |
| **Total Year 3 incremental** | **~$1.95M/year + $600K one-time** |

**Expected Year 3 ROI:**

| AI Use Case | Estimated Annual Value |
|---|---|
| Markdown optimization | $18M margin improvement |
| Demand sensing | $20M (recovered sales + inventory savings) |
| LLM store agent | $6M labor productivity |
| Personalization + churn | $15M revenue lift |
| UCP catalog exposure | $33–52M incremental revenue |
| **Total** | **$92–111M** |

**3-year cumulative ROI:** ~$105–125M in value against ~$22–28M in platform investment = **4–5x ROI**
