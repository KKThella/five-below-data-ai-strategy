# Year 2 — Customer Intelligence: CDP + BI & Analytics

> **Theme:** Know the customer. Turn unified data into personalized experiences and self-service insights.

---

## Prerequisite check from Year 1

Before Year 2 investments activate, the following Year 1 gates must be met:

- [ ] Product MDM: >95% completeness, <4 hour pricing/availability freshness
- [ ] Store MDM: all 1,500+ stores with complete attributes and geo data
- [ ] EDP Silver layer: POS, e-commerce, loyalty transactions joined and clean
- [ ] Unity Catalog: RBAC live, PII tagged, lineage documented
- [ ] At least 3 certified Gold datasets in Power BI

If these aren't met, delay CDP investment. A CDP built on dirty customer data creates a garbage-in, garbage-out personalization engine.

---

## 1. Customer Data Platform (CDP)

### The Five Below customer data problem

Five Below's customer data is currently fragmented across:
- **Loyalty program** (Five Beyond app / loyalty card) — purchase history, points, redemptions
- **E-commerce** (Shopify or equivalent) — online browse, cart, purchase, returns
- **In-store POS** — transaction data, often anonymous (no loyalty card swipe)
- **Marketing platforms** — email opens, push notifications, ad click-throughs
- **Social** — engagement signals (indirect)

Without a CDP, Five Below cannot answer:
- *Who is our highest-value customer across all channels?*
- *Which customers are at risk of churning?*
- *What is the true LTV of a loyalty member vs. a guest shopper?*
- *Which in-store shoppers are also online buyers?*

### CDP Platform: Build vs. Buy decision

**Decision: Buy** — Salesforce Data Cloud or mParticle

| Criteria | Salesforce Data Cloud | mParticle | Segment |
|---|---|---|---|
| Identity resolution depth | High | High | Medium |
| Retail connectors | Strong (POS, e-comm, loyalty) | Strong | Medium |
| AI / ML activation | Einstein AI built-in | Partner ecosystem | Partner ecosystem |
| Power BI + Databricks integration | Yes (via connector) | Yes (webhooks) | Yes |
| Marketing activation (email, push, paid) | Native | Requires MAPs | Requires MAPs |
| Estimated cost (Year 2) | $1.2M–$1.8M | $800K–$1.2M | $600K–$1M |
| **Recommendation** | ✓ If Salesforce ecosystem | ✓ Best-in-class MDP | Consider as starter |

**Q1 Year 2 action:** Issue CDP RFP. Evaluation criteria: identity resolution accuracy on Five Below's data sample (run a PoC with anonymized loyalty + POS data), Databricks connector, marketing activation capabilities, retail reference customers.

### Unified customer profile — key attributes

```json
{
  "customer_id": "fb_unified_00123456",
  "identity": {
    "emails": ["user@email.com"],
    "phones": ["+15551234567"],
    "loyalty_id": "FB-LYL-789",
    "device_ids": ["ios_abc123"]
  },
  "segments": ["high_value", "seasonal_buyer", "beauty_affinity", "lapsed_30d"],
  "lifetime_value": {
    "total_spend": 847.50,
    "avg_basket": 22.30,
    "visit_frequency": "monthly",
    "channel_mix": {"in_store": 0.72, "online": 0.28}
  },
  "affinity": {
    "top_categories": ["tech_accessories", "beauty", "candy"],
    "price_sensitivity": "low",
    "promo_responsiveness": "high"
  },
  "risk": {
    "churn_score": 0.18,
    "days_since_last_purchase": 23
  }
}
```

### Customer segments — Year 2 activation targets

| Segment | Definition | Size (est.) | Activation |
|---|---|---|---|
| High-Value Loyalists | LTV >$500, visit frequency >8x/year | 2M | VIP early access, exclusive offers |
| Seasonal Shoppers | Spike in Nov–Dec + Easter, low other months | 5M | Re-engagement campaigns before seasonal peaks |
| Lapsed (31–90 days) | No purchase in 31–90 days | 3M | Win-back with personalized category offer |
| Online-Only | Never purchased in-store | 1.5M | Drive-to-store with geo-targeted offer |
| Price Sensitive | Responds only to ≥30% discount | 4M | Clearance and markdown notifications |

### Expected CDP business impact (Year 2)

| Metric | Baseline | Target | Method |
|---|---|---|---|
| Customer identity match rate | ~40% | >75% | Identity resolution across all channels |
| Email open rate | ~18% | >28% | Personalized subject lines + send-time optimization |
| Repeat purchase rate | ~35% | ~50% | Lapsed re-engagement + loyalty nudges |
| Average basket size (loyalty) | $22 | $26 | Cross-category recommendations |
| ROAS on paid media | 2.1x | 3.5x | Suppression of recent purchasers + lookalikes |

---

## 2. BI Strategy & Self-Service Analytics

### The problem with Five Below's current BI state (hypothesized)

Most retailers at Five Below's stage have:
- 8–15 different BI tools across teams (Tableau, Excel, Looker, Power BI, custom dashboards)
- Metrics that don't match between teams ("our comp store sales number is different from finance's")
- 80% of analytics requests going to a central data team with 3–5 week queue
- Business users unable to answer basic questions without engineering help

**Year 2 goal: 70% of business users can answer their own questions within 3 days, without filing an analytics ticket.**

### Power BI + Databricks Semantic Layer architecture

```
   Databricks Gold Layer (certified datasets)
            │
   Databricks Semantic Layer
   (metrics defined once, used everywhere)
            │
        Power BI
   ┌─────────┴──────────┐
   │  Governed Reports  │  Certified dashboards maintained by BI PM team
   │  (Finance, Merch,  │  Refreshed daily/hourly, SLA-backed
   │   Supply Chain)    │
   └────────────────────┘
            │
   Power BI Self-Service
   ┌─────────┴──────────┐
   │  Business User     │  Drag-and-drop on certified semantic model
   │  Exploration       │  Cannot break certified metrics
   └────────────────────┘
```

**Why Databricks Semantic Layer matters:** Metrics like "comp store sales," "GMROI," and "sell-through rate" are defined once in the semantic layer. Every Power BI report, every analyst query, every AI use case pulls from the same definition. This eliminates the "which number is right?" debate forever.

### KPI framework — Year 2 certified metrics

#### Merchandising
- Sell-through rate by category / SKU / store
- GMROI (Gross Margin Return on Inventory Investment)
- Weeks of supply on hand
- Markdown rate (% of SKUs marked down >15%)
- New product performance (4-week velocity vs. category average)

#### Store Operations
- Comp store sales (same-store revenue, 52-week comparison)
- Transactions per hour by daypart
- Average basket size by store format
- Shrink rate (% of inventory lost to theft/damage)
- Labor hours per $1,000 revenue

#### Supply Chain
- In-stock rate by SKU / store
- Vendor on-time delivery rate
- Purchase order cycle time
- Return rate by vendor / category
- Distribution center throughput

#### Customer & Marketing
- Customer acquisition cost (CAC) by channel
- Customer lifetime value (LTV) by segment
- Net Promoter Score (NPS) by channel
- Loyalty program enrollment rate
- Email / push conversion rate

### Self-service enablement plan

| Quarter | Milestone |
|---|---|
| Q1 | Semantic layer live with top 30 certified metrics; Power BI Premium deployed |
| Q2 | "Data office hours" program launched — 2x/week sessions for business analysts |
| Q3 | Self-service adoption: 40% of business users active in Power BI; analytics ticket queue reduced 50% |
| Q4 | Self-service adoption: 70% of users active; analytics ticket queue reduced 80% |

---

## Year 2 investment summary

| Line item | Estimated cost |
|---|---|
| CDP platform (Salesforce Data Cloud or mParticle) | $1M–$1.8M/year |
| Power BI Premium | $200K/year |
| Databricks semantic layer (included in EDP contract) | $0 incremental |
| CDP implementation (SI) | $800K one-time |
| Internal headcount (2 data PMs, 1 BI PM, 1 analytics engineer) | $700K/year |
| **Total Year 2 incremental** | **~$2.7M–$3.3M** |

**Expected Year 2 ROI:**
- Personalization lift on loyalty base → estimated $15–20M incremental revenue
- Paid media ROAS improvement → estimated $3–5M in media efficiency savings
- Self-service analytics (reduced engineering backlog) → estimated $2M in analyst productivity
