# AI Governance Framework

> Responsible AI is not a legal checkbox. It's a product quality standard.

---

## Principles

1. **Purpose-built:** Every AI use case must solve a specific, measurable business problem. No AI for AI's sake.
2. **Value-driven:** Every use case ships with a defined value hypothesis and success metric before a single line of model code is written.
3. **Human-in-the-loop:** Any AI decision affecting a customer (pricing, recommendation, churn flag) must have a human override mechanism.
4. **Explainable by default:** Business stakeholders must be able to understand *why* a model made a recommendation in plain English.
5. **Monitored continuously:** No model ships to production without a monitoring plan. Drift = re-train or retire.

---

## AI use case intake process

### Stage 1 — Idea submission (any team)

**Required fields in intake form:**
- Business problem statement (1 paragraph, specific and measurable)
- Proposed AI approach (classification, regression, LLM, etc.)
- Data requirements (which datasets, availability, quality needed)
- Value hypothesis (specific metric + expected lift + measurement method)
- Customer / associate impact assessment (does AI affect a person directly?)
- Potential bias risks (are protected attributes involved?)

**Timeline:** Submit anytime. AI Review Council reviews monthly.

### Stage 2 — AI Review Council assessment

**Council members:** CPO, CDO, Legal, Privacy, Data Science Lead, Engineering Lead

**Scoring criteria:**
| Criterion | Weight | Description |
|---|---|---|
| Strategic alignment | 25% | Does this support a Year 1–3 roadmap priority? |
| Data readiness | 25% | Is required data available, clean, and governed? |
| Business impact | 30% | Is the value hypothesis credible and measurable? |
| Risk assessment | 20% | Bias risk, regulatory risk, customer impact severity |

**Outcomes:** Approved for PoC / Needs revision / Rejected (with documented rationale)

### Stage 3 — Proof of Concept (6–8 weeks)

PoC success criteria defined upfront:
- Minimum model accuracy threshold (e.g., >75% precision @ 80% recall)
- Data pipeline feasibility confirmed
- Business stakeholder validation (does the output make sense to the domain expert?)

At PoC end: Go to production / Iterate / Retire.

### Stage 4 — Production readiness review

**Required artifacts before production deployment:**

**Model Card** (required for every model):
```
Model name: [name]
Version: [v1.0]
Use case: [what decision does this model inform?]
Training data: [source, date range, record count]
Performance metrics: [precision, recall, F1, AUC]
Bias assessment: [was model tested across protected attributes? Results?]
Explainability approach: [SHAP values, LIME, business rules override?]
Monitoring plan: [what triggers re-train? Who is notified of drift?]
Human override: [how can a human override the model's recommendation?]
Rollback plan: [what is the fallback if the model is taken offline?]
```

**A/B test design** (required for all customer-facing models):
- Control group: existing rule-based approach
- Treatment group: AI recommendation
- Sample size: minimum 10,000 observations per cell
- Primary metric + secondary metrics defined
- Statistical significance threshold: p < 0.05

### Stage 5 — Production monitoring

| Signal | Threshold | Action |
|---|---|---|
| Model accuracy drop | >5% from baseline | Alert Data Science → investigate within 48hr |
| Prediction distribution shift | >15% shift in output distribution | Auto-retrain triggered |
| Data quality breach on model input | Tier 1 SLA breach | Model suspended until data quality restored |
| Business metric regression | Primary metric drops >3% | Immediate review; potential rollback |
| Bias signal | Protected attribute performance gap widens | Immediate model review; potential suspension |

---

## Responsible AI guardrails by use case type

### Pricing models (Markdown, Dynamic Clearance)
- Model cannot recommend prices that discriminate by customer segment demographics
- Floor price guardrails hardcoded (model cannot go below cost + minimum margin)
- Human pricing team reviews model recommendations weekly; override logged
- A/B test must run minimum 4 weeks before full rollout

### Recommendation models (Personalization, Churn Win-Back)
- No use of protected attributes (race, religion, health status) as model features
- Customers can opt out of personalization (UI setting in loyalty app)
- Recommendation diversity guardrail: no more than 60% of recommendations from one category
- Explainability: "Because you bought X" language displayed with every recommendation

### LLM models (Store Agent, Customer Chat)
- Grounding required: all LLM responses must be grounded on approved documents (RAG)
- Hallucination prevention: any response about pricing, policy, or inventory must include a real-time data lookup
- Human escalation path always available (associate can transfer to manager; customer can reach human agent)
- Response logging: all LLM outputs logged for quality review (sampled 5% monthly)
- No PII in LLM context beyond session scope

### Allocation / Supply Chain models
- Store allocation recommendations are advisory, not automatic — supply chain team approves
- Model must explain top 3 factors driving each allocation recommendation
- No allocation model can result in a store receiving zero units of an active SKU without human override

---

## AI ethics review triggers

Any use case that hits the following triggers requires an expanded ethics review before PoC approval:

- Uses customer age, gender, location at ZIP+4 level, or purchase history for >12 months
- Affects employee scheduling, performance review, or compensation
- Generates synthetic customer data for training
- Uses facial recognition or biometric data (currently prohibited)
- Involves predictive policing or loss prevention targeting of individuals
- Any model with <5,000 training examples in a protected demographic group
