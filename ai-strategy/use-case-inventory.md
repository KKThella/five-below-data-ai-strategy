# AI Use Case Inventory & Prioritization

> Scoring framework: each use case rated 1–5 on Impact, Data Readiness, Feasibility, and Speed to Value. Total score /20. Prioritize Tier 1 (15+) first.

---

## Scoring matrix

| Use Case | Impact | Data Readiness | Feasibility | Speed | **Total** | **Tier** |
|---|---|---|---|---|---|---|
| Markdown Optimization | 5 | 4 | 4 | 4 | **17** | 1 |
| Demand Sensing & Allocation | 5 | 4 | 4 | 3 | **16** | 1 |
| LLM Store Associate Agent | 4 | 5 | 5 | 5 | **19** | 1 |
| UCP Catalog Exposure | 5 | 3 | 4 | 3 | **15** | 1 |
| Churn Prediction & Win-Back | 4 | 3 | 4 | 4 | **15** | 1 |
| Personalized Recommendations | 4 | 3 | 4 | 3 | **14** | 2 |
| Dynamic Clearance Pricing | 4 | 3 | 3 | 3 | **13** | 2 |
| Fraud Detection (e-comm) | 3 | 4 | 4 | 3 | **14** | 2 |
| Shrink / Loss Prevention ML | 4 | 2 | 3 | 2 | **11** | 3 |
| Automated Vendor Scorecards | 3 | 3 | 4 | 4 | **14** | 2 |
| Planogram Optimization | 4 | 2 | 2 | 2 | **10** | 3 |
| Real-time Chat (customer-facing) | 3 | 3 | 4 | 3 | **13** | 2 |

---

## Tier 1 use cases — detailed value hypotheses

### 1. LLM Store Associate Agent *(Score: 19/20)*

**Problem statement:** Store associates spend 20–30% of time on knowledge lookups (product location, return policy, promotion eligibility, neighboring store inventory). This reduces floor time and customer satisfaction.

**AI solution:** RAG-based LLM grounded on Product MDM, real-time store inventory, and policy documents. Associates query via tablet/handset in natural language.

| Success metric | Baseline | Target | Measurement method |
|---|---|---|---|
| Customer escalation rate | ~18% | <10% | Support ticket tracking |
| Associate lookup time | ~6 min avg | <1 min | Time-motion study (pilot) |
| Store NPS | 34 | 42 | Monthly NPS survey |
| Associate adoption | 0% | >80% in 6 months | DAU/MAU on tool |

**Value hypothesis:** $6M annual labor productivity gain (20% reduction in associate lookup time × avg store labor cost)

**Risks:** Hallucination on policy questions (mitigated by RAG grounding + human escalation fallback). Model freshness (mitigated by daily MDM sync).

---

### 2. Markdown Optimization *(Score: 17/20)*

**Problem statement:** Five Below marks down ~$180M of inventory annually using static rules ("mark 30% at week 6"). Rules don't account for store-level velocity, local competition, or remaining season length.

**AI solution:** Gradient boosting model predicting optimal markdown % by SKU × store × week, trained on 3 years of historical sell-through, store traffic, and competitor pricing data.

| Success metric | Baseline | Target | Measurement method |
|---|---|---|---|
| Sell-through rate (seasonal) | 74% | 82% | POS data, end-of-season audit |
| Markdown spend as % of revenue | 12% | 10.8% | Finance reporting |
| Dead stock units (end of season) | 8.2M units | <6M units | WMS inventory count |
| Margin per unit (markdowns) | -$0.40 avg | -$0.22 avg | Finance P&L |

**Value hypothesis:** $18M annual margin improvement (10% reduction in markdown spend)

**A/B test design:** Split stores into 3 cohorts (AI-recommended, rule-based, control). Run for one full seasonal cycle (12–16 weeks). Primary metric: sell-through rate. Secondary: margin per unit.

---

### 3. Demand Sensing & Inventory Allocation *(Score: 16/20)*

**Problem statement:** Five Below replenishes on 4-week rolling averages. TikTok-driven viral products stock out in 48 hours. Slow-moving products sit for 20+ weeks. Current system cannot react to real-time demand signals.

**AI solution:** Ensemble model combining:
- POS velocity (real-time, from EDP Bronze layer, <15 min latency)
- Social trend signals (TikTok API, Google Trends)
- Search volume velocity (Google Ads data)
- Weather patterns (for seasonal categories)

Output: daily allocation recommendations by SKU × DC → store cluster.

| Success metric | Baseline | Target | Measurement method |
|---|---|---|---|
| In-stock rate (trending SKUs) | ~72% | >88% | POS stockout flag |
| Inventory turn ratio | 6.2x | 7.5x | Finance/WMS |
| Overstock units (90+ days) | 11M units | <8M units | WMS aging report |
| Stockout-driven lost sales | ~$35M est. | <$20M | POS stockout × avg price |

**Value hypothesis:** $20M combined impact (recovered stockout sales + inventory savings)

---

### 4. Churn Prediction & Win-Back *(Score: 15/20)*

**Problem statement:** Five Below loses ~35% of active loyalty members each year. Win-back campaigns are batch, untargeted, and sent too late (60+ days after last purchase, when churn is already confirmed).

**AI solution:** Logistic regression / gradient boosting churn model on CDP behavioral signals:
- Days since last purchase (primary signal)
- Purchase frequency trend (declining = churn risk)
- Category engagement (narrowing = risk)
- Email engagement (declining = risk)
- Seasonal pattern (don't flag seasonal-only buyers as churn risk)

**Trigger:** Automated win-back campaign fires at 21-day inactivity (model confidence >70% churn risk), not 60 days.

| Success metric | Baseline | Target | Measurement method |
|---|---|---|---|
| Churn rate (annual) | ~35% | <28% | Cohort analysis |
| Win-back campaign CVR | ~4% | >9% | CDP campaign analytics |
| Lapsed customer recovery (LTV) | $8 avg | $22 avg | Finance × CDP |
| Model precision @ 70% threshold | — | >78% | Model card |

**Value hypothesis:** $12M recovered LTV from 5% churn rate reduction on loyalty base

---

## Tier 2 use cases — brief descriptions

### Personalized Recommendations (E-commerce)
Hybrid collaborative filtering + content-based model. Inputs: CDP purchase history, browse history, category affinity. Output: "You might also like" carousel. **Target:** +8% AOV.

### Dynamic Clearance Pricing
Reinforcement learning agent optimizing clearance markdown % daily (within $0.25 guardrails). Trained on historical clearance velocity. **Target:** 8% improvement in clearance sell-through.

### Fraud Detection (E-commerce)
Gradient boosting model on transaction signals (device fingerprint, velocity, address mismatch). **Target:** <0.3% false positive rate, >85% fraud catch rate.

### Automated Vendor Scorecards
LLM-assisted synthesis of vendor performance across on-time delivery, product quality, compliance, and cost. Weekly scorecard generated automatically from EDI + WMS data. **Target:** 80% reduction in manual vendor review time.

### Real-Time Customer Chat (E-commerce)
RAG-based LLM for e-commerce customer support (order status, returns, product questions). Grounded on EDP + CDP + Product MDM. **Target:** 30% reduction in human support tickets.

---

## Use case retirement criteria

A use case is retired or deprioritized if, after one full A/B test cycle:
- Primary metric improvement is <50% of target
- Model precision/recall is below minimum threshold
- Business adoption is <30% of target users
- Data quality issues cannot be resolved within one sprint

Retired use cases go back to the backlog with lessons learned documented for future consideration.
