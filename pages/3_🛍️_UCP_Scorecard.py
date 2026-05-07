import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
# ── STYLES ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.score-excellent { background:#d1fae5; color:#065f46; padding:4px 14px; border-radius:14px; font-size:13px; font-weight:700; }
.score-good      { background:#dbeafe; color:#1e40af; padding:4px 14px; border-radius:14px; font-size:13px; font-weight:700; }
.score-fair      { background:#fef3c7; color:#92400e; padding:4px 14px; border-radius:14px; font-size:13px; font-weight:700; }
.score-poor      { background:#fee2e2; color:#991b1b; padding:4px 14px; border-radius:14px; font-size:13px; font-weight:700; }
.metric-card     { background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:16px 20px; text-align:center; }
.metric-label    { font-size:11px; color:#64748b; margin-bottom:4px; text-transform:uppercase; letter-spacing:0.05em; }
.metric-value    { font-size:28px; font-weight:700; color:#1e293b; }
.metric-sub      { font-size:11px; color:#94a3b8; margin-top:3px; }
.section-header  { font-size:13px; font-weight:600; color:#475569; text-transform:uppercase; letter-spacing:0.06em; margin:1.2rem 0 0.5rem; }
.gap-critical    { border-left:4px solid #ef4444; padding:10px 14px; background:#fef2f2; border-radius:0 8px 8px 0; margin-bottom:10px; }
.gap-moderate    { border-left:4px solid #f59e0b; padding:10px 14px; background:#fffbeb; border-radius:0 8px 8px 0; margin-bottom:10px; }
.gap-minor       { border-left:4px solid #10b981; padding:10px 14px; background:#f0fdf4; border-radius:0 8px 8px 0; margin-bottom:10px; }
.ucp-endpoint-built   { background:#d1fae5; color:#065f46; padding:3px 10px; border-radius:8px; font-size:11px; font-weight:600; }
.ucp-endpoint-partial { background:#fef3c7; color:#92400e; padding:3px 10px; border-radius:8px; font-size:11px; font-weight:600; }
.ucp-endpoint-missing { background:#fee2e2; color:#991b1b; padding:3px 10px; border-radius:8px; font-size:11px; font-weight:600; }
.competitor-ahead { color:#ef4444; font-weight:600; }
.competitor-behind { color:#10b981; font-weight:600; }
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ─────────────────────────────────────────────────────────────────

UCP_ENDPOINTS = [
    {
        "endpoint": "/products/search",
        "purpose": "Semantic search across catalog — natural language queries from AI agents",
        "ucp_requirement": "Must support NL queries, return structured product data with pricing and availability",
        "complexity": "High",
        "build_weeks": 6,
    },
    {
        "endpoint": "/products/{sku}/availability",
        "purpose": "Real-time inventory by store and online — enables 'in stock near me' queries",
        "ucp_requirement": "Must return store-level availability with <15min staleness",
        "complexity": "Medium",
        "build_weeks": 3,
    },
    {
        "endpoint": "/products/{sku}/price",
        "purpose": "Current price + promotion eligibility — ensures AI agent surfaces accurate pricing",
        "ucp_requirement": "Must return base price, promo price, and eligibility rules with <5min staleness",
        "complexity": "Medium",
        "build_weeks": 3,
    },
    {
        "endpoint": "/cart/add",
        "purpose": "Add-to-cart via AI agent — enables frictionless agentic checkout",
        "ucp_requirement": "UCP standard cart schema: sku_id, quantity, store_id or fulfillment_type",
        "complexity": "High",
        "build_weeks": 6,
    },
    {
        "endpoint": "/checkout/initiate",
        "purpose": "UCP payment handoff — AI agent hands off to merchant checkout flow",
        "ucp_requirement": "OAuth 2.0 handoff, pre-populated cart, UCP payment token standard",
        "complexity": "Very High",
        "build_weeks": 8,
    },
    {
        "endpoint": "/orders/{id}/status",
        "purpose": "Post-purchase order tracking — enables agents to answer 'where is my order'",
        "ucp_requirement": "Real-time order status, estimated delivery, return eligibility",
        "complexity": "Medium",
        "build_weeks": 3,
    },
    {
        "endpoint": "/returns/initiate",
        "purpose": "Agentic return flow — customer can initiate return through AI agent",
        "ucp_requirement": "Return eligibility check, label generation handoff, refund estimate",
        "complexity": "High",
        "build_weeks": 5,
    },
]

CATALOG_DIMENSIONS = [
    {
        "dimension": "Product Name & Description",
        "ucp_requirement": "Clear, structured product name + 100–500 char description optimized for NL queries",
        "weight": 15,
        "impact": "Critical — directly affects AI agent's ability to match products to shopper queries",
    },
    {
        "dimension": "Category Taxonomy (Google-compatible)",
        "ucp_requirement": "Google Product Taxonomy mapped to all SKUs (full tree, not just top-level)",
        "weight": 15,
        "impact": "Critical — determines which AI agent queries Five Below products appear in",
    },
    {
        "dimension": "Product Images",
        "ucp_requirement": ">= 1 clean white-background image per SKU, min 800×800px",
        "weight": 12,
        "impact": "High — AI shopping UIs display images; missing images reduce conversion",
    },
    {
        "dimension": "Current Price",
        "ucp_requirement": "Real-time base price + promotional price with effective date",
        "weight": 15,
        "impact": "Critical — incorrect pricing = agent surfaces wrong price = customer distrust",
    },
    {
        "dimension": "Availability (online + store)",
        "ucp_requirement": "In-stock flag + store-level inventory + online availability, <15min freshness",
        "weight": 15,
        "impact": "Critical — availability determines whether agent recommends the product",
    },
    {
        "dimension": "Product Attributes (color, size, age range, etc.)",
        "ucp_requirement": "Structured attribute set mapped to Google's attribute vocabulary",
        "weight": 10,
        "impact": "High — enables filtered queries ('red toys under $5 for 5-year-olds')",
    },
    {
        "dimension": "Brand & Manufacturer",
        "ucp_requirement": "Standardized brand name; private label mapped to Five Below brand",
        "weight": 8,
        "impact": "Medium — brand queries and brand filtering",
    },
    {
        "dimension": "GTIN / Barcode",
        "ucp_requirement": "UPC/EAN for branded products; private label exempt but recommended",
        "weight": 5,
        "impact": "Medium — cross-retailer product matching by AI agents",
    },
    {
        "dimension": "Return Policy",
        "ucp_requirement": "Machine-readable return window, conditions, and process",
        "weight": 3,
        "impact": "Low-Medium — reduces post-purchase friction in agentic flows",
    },
    {
        "dimension": "Shipping Options & Fulfillment",
        "ucp_requirement": "Ship-to-home, BOPIS, delivery estimate by zip code",
        "weight": 2,
        "impact": "Low-Medium — fulfillment options surface in agent recommendations",
    },
]

COMPETITORS = [
    {"retailer": "Walmart", "ucp_score": 94, "catalog_completeness": 98, "status": "Live on UCP", "notes": "UCP founding partner; full endpoint suite live Jan 2026"},
    {"retailer": "Target", "ucp_score": 91, "catalog_completeness": 96, "status": "Live on UCP", "notes": "UCP founding partner; BOPIS + ship integration complete"},
    {"retailer": "Dollar Tree", "ucp_score": 38, "catalog_completeness": 55, "status": "Not started", "notes": "No public UCP roadmap announced"},
    {"retailer": "Dollar General", "ucp_score": 42, "catalog_completeness": 60, "status": "Evaluating", "notes": "Exploring UCP; no live endpoints"},
    {"retailer": "Five Below (current)", "ucp_score": 0, "catalog_completeness": 0, "status": "Not started", "notes": "Baseline — your current state"},
    {"retailer": "Five Below (Year 3 target)", "ucp_score": 0, "catalog_completeness": 0, "status": "Target", "notes": "Year 3 target with full data foundation"},
]

REMEDIATION_PLAN = [
    {
        "phase": "Phase 1 — Data Foundation (Year 1)",
        "duration": "12 months",
        "priority": "🔴 Blocker",
        "actions": [
            "Product MDM: Achieve >97% catalog completeness across all 10 catalog dimensions",
            "Google taxonomy mapping: Map all active SKUs to full Google Product Taxonomy tree",
            "Image backfill: Ensure >98% of active SKUs have compliant images (800×800px, white bg)",
            "Real-time pricing feed: Build EDP Bronze→Gold pipeline with <5min pricing latency",
            "Real-time inventory feed: Build store-level inventory pipeline with <15min latency",
            "GTIN coverage: Source UPCs for branded products; assign internal GTINs for private label",
        ],
        "ucp_score_after": 45,
    },
    {
        "phase": "Phase 2 — API Layer (Year 2 H2 → Year 3 H1)",
        "duration": "6 months",
        "priority": "🟡 High",
        "actions": [
            "Build FastAPI UCP endpoint layer on top of EDP Gold layer",
            "Launch /products/search with semantic search (Databricks Vector Search on product MDM)",
            "Launch /products/{sku}/availability — real-time store inventory lookup",
            "Launch /products/{sku}/price — real-time pricing with promo eligibility",
            "Register Five Below in Google UCP sandbox and begin certification testing",
            "OAuth 2.0 integration for UCP session handoff",
        ],
        "ucp_score_after": 72,
    },
    {
        "phase": "Phase 3 — Transactional Endpoints (Year 3 H1)",
        "duration": "4 months",
        "priority": "🟡 High",
        "actions": [
            "Launch /cart/add — UCP standard cart schema integration",
            "Launch /checkout/initiate — payment handoff with UCP token standard",
            "Launch /orders/{id}/status — post-purchase order tracking",
            "Launch /returns/initiate — agentic return flow",
            "Complete Google UCP certification and go live in AI Mode / Gemini",
        ],
        "ucp_score_after": 91,
    },
    {
        "phase": "Phase 4 — Optimize & Scale (Year 3 H2)",
        "duration": "Ongoing",
        "priority": "🟢 Growth",
        "actions": [
            "A/B test UCP vs. organic search conversion rates; optimize catalog attributes for agent queries",
            "Expand to additional AI agent platforms (Perplexity, Microsoft Copilot, Amazon Rufus)",
            "Launch UCP-specific promotions and AI-agent exclusive deals",
            "Instrument UCP funnel analytics (query → click → cart → purchase → return)",
            "Explore UCP advertising opportunities as platform matures",
        ],
        "ucp_score_after": 97,
    },
]

# ── SESSION STATE — SCORECARD INPUTS ─────────────────────────────────────────

def default_state():
    return {
        "catalog_completeness": 65,
        "taxonomy_coverage": 40,
        "image_coverage": 70,
        "pricing_freshness_min": 24 * 60,
        "inventory_freshness_min": 24 * 60,
        "gtin_coverage": 50,
        "attribute_coverage": 45,
        "endpoint_search": "Missing",
        "endpoint_availability": "Missing",
        "endpoint_price": "Missing",
        "endpoint_cart": "Missing",
        "endpoint_checkout": "Missing",
        "endpoint_order_status": "Missing",
        "endpoint_returns": "Missing",
        "annual_revenue_m": 3600,
        "online_revenue_pct": 8,
        "ai_search_capture_pct": 30,
    }

for k, v in default_state().items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── SCORING LOGIC ─────────────────────────────────────────────────────────────

def catalog_score():
    """0–40 points: catalog data quality across all dimensions."""
    weights = {
        "catalog_completeness": 10,
        "taxonomy_coverage": 10,
        "image_coverage": 6,
        "attribute_coverage": 8,
        "gtin_coverage": 4,
        "return_policy": 2,  # assume 100% for now (text-based)
    }
    raw = (
        (st.session_state.catalog_completeness / 100) * weights["catalog_completeness"] +
        (st.session_state.taxonomy_coverage / 100) * weights["taxonomy_coverage"] +
        (st.session_state.image_coverage / 100) * weights["image_coverage"] +
        (st.session_state.attribute_coverage / 100) * weights["attribute_coverage"] +
        (st.session_state.gtin_coverage / 100) * weights["gtin_coverage"] +
        1.0 * weights["return_policy"]  # assume basic return policy text exists
    )
    return round(raw, 1)

def feed_score():
    """0–25 points: real-time feed readiness (pricing + inventory)."""
    def pricing_pts(mins):
        if mins <= 5:   return 12.5
        if mins <= 30:  return 9.0
        if mins <= 60:  return 6.0
        if mins <= 240: return 3.0
        return 0.0

    def inventory_pts(mins):
        if mins <= 15:  return 12.5
        if mins <= 60:  return 9.0
        if mins <= 240: return 6.0
        if mins <= 720: return 3.0
        return 0.0

    return round(pricing_pts(st.session_state.pricing_freshness_min) +
                 inventory_pts(st.session_state.inventory_freshness_min), 1)

def endpoint_score():
    """0–35 points: UCP endpoint coverage."""
    endpoint_weights = {
        "endpoint_search": 10,
        "endpoint_availability": 6,
        "endpoint_price": 6,
        "endpoint_cart": 6,
        "endpoint_checkout": 4,
        "endpoint_order_status": 2,
        "endpoint_returns": 1,
    }
    status_multiplier = {"Built": 1.0, "Partial": 0.5, "Missing": 0.0}
    total = 0.0
    for key, weight in endpoint_weights.items():
        total += weight * status_multiplier.get(st.session_state[key], 0.0)
    return round(total, 1)

def total_score():
    return round(catalog_score() + feed_score() + endpoint_score(), 1)

def score_label(score):
    if score >= 85: return "Excellent", "score-excellent", "🟢 UCP Ready"
    if score >= 65: return "Good", "score-good", "🔵 Mostly Ready"
    if score >= 40: return "Fair", "score-fair", "🟡 Significant Gaps"
    return "Poor", "score-poor", "🔴 Not UCP Ready"

def revenue_opportunity():
    rev = st.session_state.annual_revenue_m
    online_pct = st.session_state.online_revenue_pct / 100
    ai_pct = st.session_state.ai_search_capture_pct / 100
    addressable_online = rev * online_pct
    ai_addressable = (rev * (1 - online_pct)) * ai_pct * 0.15  # new customer capture
    ucp_conversion_lift = addressable_online * ai_pct * 0.40   # 40% conversion lift for online
    new_customer = ai_addressable
    total = ucp_conversion_lift + new_customer
    return {
        "annual_revenue": rev,
        "online_revenue": round(rev * online_pct, 1),
        "ucp_conversion_lift": round(ucp_conversion_lift, 1),
        "new_customer_revenue": round(new_customer, 1),
        "total_opportunity": round(total, 1),
    }

def freshness_label(minutes):
    if minutes < 60: return f"{minutes}min"
    if minutes < 1440: return f"{minutes // 60}hr"
    return f"{minutes // 1440}d"

# ── SIDEBAR — SCORECARD INPUTS ────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🛍️ UCP Scorecard")
    st.markdown("**Adjust inputs to reflect current state**")
    st.caption(f"Scored: {datetime.now().strftime('%b %d, %Y')}")
    st.divider()

    st.markdown("**📦 Catalog Quality**")
    st.session_state.catalog_completeness = st.slider(
        "Overall Catalog Completeness (%)", 0, 100,
        st.session_state.catalog_completeness, 1,
        help="% of active SKUs with all required fields populated"
    )
    st.session_state.taxonomy_coverage = st.slider(
        "Google Taxonomy Coverage (%)", 0, 100,
        st.session_state.taxonomy_coverage, 1,
        help="% of SKUs mapped to full Google Product Taxonomy tree"
    )
    st.session_state.image_coverage = st.slider(
        "Image Coverage (%)", 0, 100,
        st.session_state.image_coverage, 1,
        help="% of active SKUs with compliant product images"
    )
    st.session_state.attribute_coverage = st.slider(
        "Attribute Coverage (%)", 0, 100,
        st.session_state.attribute_coverage, 1,
        help="% of SKUs with structured attributes (color, size, age range, etc.)"
    )
    st.session_state.gtin_coverage = st.slider(
        "GTIN / Barcode Coverage (%)", 0, 100,
        st.session_state.gtin_coverage, 1,
        help="% of branded SKUs with UPC/EAN codes"
    )

    st.divider()
    st.markdown("**⚡ Real-Time Feed Readiness**")
    pricing_options = [5, 15, 30, 60, 120, 240, 480, 1440]
    pricing_labels = ["5min", "15min", "30min", "1hr", "2hr", "4hr", "8hr", "24hr (batch)"]
    pricing_idx = pricing_options.index(st.session_state.pricing_freshness_min) \
        if st.session_state.pricing_freshness_min in pricing_options else 7
    pricing_sel = st.selectbox("Pricing Feed Freshness", pricing_labels, index=pricing_idx)
    st.session_state.pricing_freshness_min = pricing_options[pricing_labels.index(pricing_sel)]

    inv_options = [5, 15, 30, 60, 120, 240, 480, 1440]
    inv_labels = ["5min", "15min", "30min", "1hr", "2hr", "4hr", "8hr", "24hr (batch)"]
    inv_idx = inv_options.index(st.session_state.inventory_freshness_min) \
        if st.session_state.inventory_freshness_min in inv_options else 7
    inv_sel = st.selectbox("Inventory Feed Freshness", inv_labels, index=inv_idx)
    st.session_state.inventory_freshness_min = inv_options[inv_labels.index(inv_sel)]

    st.divider()
    st.markdown("**🔌 UCP Endpoint Status**")
    status_opts = ["Missing", "Partial", "Built"]
    for ep_key, ep_label in [
        ("endpoint_search",       "/products/search"),
        ("endpoint_availability", "/products/{sku}/availability"),
        ("endpoint_price",        "/products/{sku}/price"),
        ("endpoint_cart",         "/cart/add"),
        ("endpoint_checkout",     "/checkout/initiate"),
        ("endpoint_order_status", "/orders/{id}/status"),
        ("endpoint_returns",      "/returns/initiate"),
    ]:
        st.session_state[ep_key] = st.selectbox(
            ep_label, status_opts,
            index=status_opts.index(st.session_state[ep_key]),
            key=f"sb_{ep_key}"
        )

    st.divider()
    st.markdown("**💰 Revenue Model**")
    st.session_state.annual_revenue_m = st.number_input(
        "Annual Revenue ($M)", 100, 50000,
        st.session_state.annual_revenue_m, 100
    )
    st.session_state.online_revenue_pct = st.slider(
        "Online Revenue (% of total)", 1, 50,
        st.session_state.online_revenue_pct, 1
    )
    st.session_state.ai_search_capture_pct = st.slider(
        "AI Search Share of Queries (% by 2027)", 5, 60,
        st.session_state.ai_search_capture_pct, 5
    )

    if st.button("🔄 Reset to Five Below Baseline", use_container_width=True):
        for k, v in default_state().items():
            st.session_state[k] = v
        st.rerun()

# ── HEADER ────────────────────────────────────────────────────────────────────

st.title("🛍️ UCP Readiness Scorecard")
st.markdown(
    "Assess a retailer's readiness for **Google's Universal Commerce Protocol (UCP)** — "
    "the open standard enabling AI agents (Google AI Mode, Gemini, Perplexity) to discover, "
    "evaluate, and purchase products directly through conversational interfaces."
)

score = total_score()
cat_score = catalog_score()
fd_score = feed_score()
ep_score = endpoint_score()
label, css, status_text = score_label(score)

st.divider()

# ── SCORE SUMMARY ─────────────────────────────────────────────────────────────

col1, col2, col3, col4, col5 = st.columns([1.5, 1, 1, 1, 1])

with col1:
    gauge_color = "#10b981" if score >= 85 else ("#3b82f6" if score >= 65 else ("#f59e0b" if score >= 40 else "#ef4444"))
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "UCP Readiness Score", "font": {"size": 14, "color": "#475569"}},
        number={"suffix": "/100", "font": {"size": 28, "color": "#1e293b"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#94a3b8"},
            "bar": {"color": gauge_color},
            "steps": [
                {"range": [0, 40],  "color": "#fee2e2"},
                {"range": [40, 65], "color": "#fef3c7"},
                {"range": [65, 85], "color": "#dbeafe"},
                {"range": [85, 100],"color": "#d1fae5"},
            ],
            "threshold": {"line": {"color": "#1e293b", "width": 2}, "thickness": 0.75, "value": score}
        }
    ))
    fig_gauge.update_layout(height=200, margin=dict(t=40, b=0, l=20, r=20), paper_bgcolor="white")
    st.plotly_chart(fig_gauge, use_container_width=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Status</div>
        <div style="margin-top:6px"><span class="{css}">{status_text}</span></div>
        <div class="metric-sub" style="margin-top:8px">{label} readiness</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📦 Catalog Score</div>
        <div class="metric-value">{cat_score}<span style="font-size:14px;color:#94a3b8">/40</span></div>
        <div class="metric-sub">data quality</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">⚡ Feed Score</div>
        <div class="metric-value">{fd_score}<span style="font-size:14px;color:#94a3b8">/25</span></div>
        <div class="metric-sub">real-time readiness</div>
    </div>""", unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🔌 Endpoint Score</div>
        <div class="metric-value">{ep_score}<span style="font-size:14px;color:#94a3b8">/35</span></div>
        <div class="metric-sub">API coverage</div>
    </div>""", unsafe_allow_html=True)

st.markdown("")

# ── TABS ──────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📦 Catalog Assessment",
    "🔌 Endpoint Gap Analysis",
    "💰 Revenue Opportunity",
    "🏁 Competitive Landscape",
    "🗺️ Remediation Roadmap",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CATALOG ASSESSMENT
# ══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown('<div class="section-header">Catalog Readiness by Dimension</div>', unsafe_allow_html=True)
    st.caption(
        "UCP requires structured, accurate, and real-time product data across 10 catalog dimensions. "
        "Missing or stale data means AI agents cannot surface your products — even if you have the right inventory."
    )

    current_vals = {
        "Product Name & Description": st.session_state.catalog_completeness,
        "Category Taxonomy (Google-compatible)": st.session_state.taxonomy_coverage,
        "Product Images": st.session_state.image_coverage,
        "Current Price": 100 if st.session_state.pricing_freshness_min <= 30 else (
                         60 if st.session_state.pricing_freshness_min <= 240 else 20),
        "Availability (online + store)": 100 if st.session_state.inventory_freshness_min <= 60 else (
                                         60 if st.session_state.inventory_freshness_min <= 480 else 20),
        "Product Attributes (color, size, age range, etc.)": st.session_state.attribute_coverage,
        "Brand & Manufacturer": min(st.session_state.catalog_completeness + 10, 100),
        "GTIN / Barcode": st.session_state.gtin_coverage,
        "Return Policy": 85,
        "Shipping Options & Fulfillment": 70,
    }

    radar_dims = list(current_vals.keys())
    radar_vals = list(current_vals.values())
    target_vals = [dim["ucp_requirement"] and 97 for dim in CATALOG_DIMENSIONS]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=radar_vals + [radar_vals[0]],
        theta=radar_dims + [radar_dims[0]],
        fill="toself",
        name="Current State",
        fillcolor="rgba(59,130,246,0.15)",
        line=dict(color="#3b82f6", width=2),
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=[97] * len(radar_dims) + [97],
        theta=radar_dims + [radar_dims[0]],
        fill="toself",
        name="UCP Target (97%)",
        fillcolor="rgba(16,185,129,0.07)",
        line=dict(color="#10b981", width=1.5, dash="dot"),
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=420,
        paper_bgcolor="white",
        font_color="#1e293b",
        title="Catalog Dimension Coverage vs. UCP Target",
        margin=dict(t=50, b=20),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    st.divider()
    st.markdown('<div class="section-header">Dimension-by-Dimension Detail</div>', unsafe_allow_html=True)

    for dim in CATALOG_DIMENSIONS:
        name = dim["dimension"]
        current = current_vals.get(name, 50)
        gap = 97 - current
        if gap <= 0:
            gap_css, gap_label = "gap-minor", "✅ UCP Ready"
        elif gap <= 20:
            gap_css, gap_label = "gap-moderate", f"⚠️ Gap: {gap:.0f}pp to close"
        else:
            gap_css, gap_label = "gap-critical", f"🔴 Gap: {gap:.0f}pp to close"

        with st.expander(f"**{name}** — Weight: {dim['weight']}pts — {gap_label}"):
            c1, c2 = st.columns([1, 2])
            with c1:
                st.markdown(f"**Current coverage:** {current:.0f}%")
                st.progress(current / 100)
                st.markdown(f"**UCP requirement:** 97%")
                st.markdown(f"**Weight in score:** {dim['weight']} pts")
            with c2:
                st.markdown(f"**UCP requirement:** {dim['ucp_requirement']}")
                st.markdown(f"**Business impact:** {dim['impact']}")

    st.divider()
    st.markdown('<div class="section-header">Feed Freshness Assessment</div>', unsafe_allow_html=True)

    pricing_min = st.session_state.pricing_freshness_min
    inventory_min = st.session_state.inventory_freshness_min

    f1, f2 = st.columns(2)
    with f1:
        p_score = feed_score() / 2
        p_status = "✅ UCP Compliant (<5 min)" if pricing_min <= 5 else (
                   "⚠️ Near Compliant (<30 min)" if pricing_min <= 30 else "🔴 Not Compliant (batch)")
        st.markdown(f"**Pricing Feed Freshness**")
        st.markdown(f"Current: **{freshness_label(pricing_min)}** | UCP Requirement: **<5 min**")
        st.markdown(f"{p_status}")
        st.progress(min(5 / max(pricing_min, 1), 1.0))

    with f2:
        i_status = "✅ UCP Compliant (<15 min)" if inventory_min <= 15 else (
                   "⚠️ Near Compliant (<1 hr)" if inventory_min <= 60 else "🔴 Not Compliant (batch)")
        st.markdown(f"**Inventory Feed Freshness**")
        st.markdown(f"Current: **{freshness_label(inventory_min)}** | UCP Requirement: **<15 min**")
        st.markdown(f"{i_status}")
        st.progress(min(15 / max(inventory_min, 1), 1.0))

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ENDPOINT GAP ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown('<div class="section-header">UCP Endpoint Coverage</div>', unsafe_allow_html=True)
    st.caption(
        "UCP requires 7 API endpoints for full agentic commerce capability — from product discovery "
        "through checkout and post-purchase. Each endpoint enables a different part of the AI agent shopping flow."
    )

    ep_keys = [
        "endpoint_search", "endpoint_availability", "endpoint_price",
        "endpoint_cart", "endpoint_checkout", "endpoint_order_status", "endpoint_returns"
    ]
    ep_statuses = [st.session_state[k] for k in ep_keys]

    built_count   = ep_statuses.count("Built")
    partial_count = ep_statuses.count("Partial")
    missing_count = ep_statuses.count("Missing")

    m1, m2, m3 = st.columns(3)
    m1.metric("✅ Built", built_count, f"of {len(ep_keys)} endpoints")
    m2.metric("⚠️ Partial", partial_count, f"of {len(ep_keys)} endpoints")
    m3.metric("🔴 Missing", missing_count, f"of {len(ep_keys)} endpoints")

    st.markdown("")

    for ep, key in zip(UCP_ENDPOINTS, ep_keys):
        status = st.session_state[key]
        if status == "Built":
            badge_css, badge_label = "ucp-endpoint-built", "✅ Built"
            gap_css = "gap-minor"
        elif status == "Partial":
            badge_css, badge_label = "ucp-endpoint-partial", "⚠️ Partial"
            gap_css = "gap-moderate"
        else:
            badge_css, badge_label = "ucp-endpoint-missing", "🔴 Missing"
            gap_css = "gap-critical"

        with st.expander(
            f"**{ep['endpoint']}** &nbsp;&nbsp; "
            f"Complexity: {ep['complexity']} · Est. {ep['build_weeks']}wk build"
        ):
            st.markdown(f'<span class="{badge_css}">{badge_label}</span>', unsafe_allow_html=True)
            st.markdown("")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Purpose:** {ep['purpose']}")
                st.markdown(f"**Complexity:** {ep['complexity']}")
                st.markdown(f"**Estimated build time:** {ep['build_weeks']} weeks")
            with c2:
                st.markdown(f"**UCP requirement:** {ep['ucp_requirement']}")
                if status == "Missing":
                    st.info(f"⏱️ Add ~{ep['build_weeks']} weeks to roadmap. Dependency: EDP Gold layer + real-time feeds.")
                elif status == "Partial":
                    st.warning("⚠️ Partial implementation detected. Review UCP certification requirements before go-live.")
                else:
                    st.success("✅ Endpoint built. Ensure UCP certification test suite passes before production traffic.")

    st.divider()
    st.markdown('<div class="section-header">Build Timeline (based on current status)</div>', unsafe_allow_html=True)

    total_weeks = sum(ep["build_weeks"] for ep, key in zip(UCP_ENDPOINTS, ep_keys)
                      if st.session_state[key] == "Missing")
    partial_weeks = sum(ep["build_weeks"] // 2 for ep, key in zip(UCP_ENDPOINTS, ep_keys)
                        if st.session_state[key] == "Partial")

    if total_weeks + partial_weeks == 0:
        st.success("🎉 All endpoints built! Proceed to UCP certification testing.")
    else:
        st.markdown(f"""
        **Remaining endpoint work:**
        - Missing endpoints: **~{total_weeks} weeks** of build effort
        - Partial endpoints: **~{partial_weeks} weeks** of completion effort
        - **Total: ~{total_weeks + partial_weeks} weeks** (assumes sequential; parallel teams reduce this)
        """)
        st.info("💡 With a 3-engineer team, parallel endpoint development reduces calendar time by ~40%.")

    # Endpoint status donut
    donut_df = pd.DataFrame({
        "Status": ["Built", "Partial", "Missing"],
        "Count": [built_count, partial_count, missing_count],
    })
    fig_donut = px.pie(
        donut_df, values="Count", names="Status",
        color="Status",
        color_discrete_map={"Built": "#10b981", "Partial": "#f59e0b", "Missing": "#ef4444"},
        hole=0.55,
        title="UCP Endpoint Coverage",
    )
    fig_donut.update_layout(height=300, paper_bgcolor="white", font_color="#1e293b",
                            margin=dict(t=40, b=10))
    st.plotly_chart(fig_donut, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — REVENUE OPPORTUNITY
# ══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown('<div class="section-header">UCP Revenue Opportunity Model</div>', unsafe_allow_html=True)
    st.caption(
        "Quantify the incremental revenue at stake if Five Below becomes UCP-compliant vs. "
        "staying off the protocol while competitors capture AI-driven shopping queries."
    )

    opp = revenue_opportunity()

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Annual Revenue</div>
            <div class="metric-value">${opp['annual_revenue']:,.0f}M</div>
            <div class="metric-sub">total baseline</div>
        </div>""", unsafe_allow_html=True)
    with r2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Online Revenue</div>
            <div class="metric-value">${opp['online_revenue']:,.0f}M</div>
            <div class="metric-sub">{st.session_state.online_revenue_pct}% of total</div>
        </div>""", unsafe_allow_html=True)
    with r3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">UCP Conversion Lift</div>
            <div class="metric-value" style="color:#3b82f6">${opp['ucp_conversion_lift']:,.0f}M</div>
            <div class="metric-sub">40% lift on AI-driven online revenue</div>
        </div>""", unsafe_allow_html=True)
    with r4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total UCP Opportunity</div>
            <div class="metric-value" style="color:#10b981">${opp['total_opportunity']:,.0f}M</div>
            <div class="metric-sub">annual incremental revenue</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")

    # Waterfall chart
    waterfall_fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute", "relative", "relative", "total"],
        x=["Baseline Online Revenue", "UCP Conversion Lift\n(40% higher CVR)", "New Customer\nAcquisition via AI", "Total UCP\nOpportunity"],
        y=[opp["online_revenue"], opp["ucp_conversion_lift"], opp["new_customer_revenue"], 0],
        connector={"line": {"color": "#94a3b8"}},
        decreasing={"marker": {"color": "#ef4444"}},
        increasing={"marker": {"color": "#10b981"}},
        totals={"marker": {"color": "#3b82f6"}},
        text=[f"${opp['online_revenue']:.0f}M", f"+${opp['ucp_conversion_lift']:.0f}M",
              f"+${opp['new_customer_revenue']:.0f}M", f"${opp['total_opportunity']:.0f}M"],
        textposition="outside",
    ))
    waterfall_fig.update_layout(
        title="UCP Revenue Opportunity Waterfall ($M)",
        plot_bgcolor="white", paper_bgcolor="white",
        font_color="#1e293b", height=380,
        yaxis_title="Revenue ($M)",
    )
    st.plotly_chart(waterfall_fig, use_container_width=True)

    st.divider()
    st.markdown('<div class="section-header">Opportunity by Scenario</div>', unsafe_allow_html=True)

    scenarios = pd.DataFrame([
        {"Scenario": "Conservative",
         "AI Search Share": "20% of queries",
         "UCP Conversion Lift": "25%",
         "New Customer Capture": "Low",
         "Annual Revenue Impact": f"${opp['total_opportunity'] * 0.5:.0f}M"},
        {"Scenario": "Base Case",
         "AI Search Share": f"{st.session_state.ai_search_capture_pct}% of queries",
         "UCP Conversion Lift": "40%",
         "New Customer Capture": "Medium",
         "Annual Revenue Impact": f"${opp['total_opportunity']:.0f}M"},
        {"Scenario": "Optimistic",
         "AI Search Share": "45% of queries",
         "UCP Conversion Lift": "55%",
         "New Customer Capture": "High",
         "Annual Revenue Impact": f"${opp['total_opportunity'] * 1.8:.0f}M"},
    ])
    st.dataframe(scenarios, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown('<div class="section-header">Cost of Inaction</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
**If Five Below stays off UCP while competitors go live:**
- Walmart and Target capture AI-driven "value shopping" queries that Five Below would naturally win
- AI agents can't recommend Five Below products even when inventory + price are perfect matches
- Dollar Tree / Dollar General's eventual UCP entry could dilute Five Below's value positioning
- Loss of new customer acquisition channel that requires zero paid media spend
        """)
    with col_b:
        year_delay_cost = opp["total_opportunity"]
        st.markdown(f"""
**Revenue at risk per year of delay:**

| Delay | Revenue Foregone |
|-------|-----------------|
| 1 year | ${year_delay_cost:.0f}M |
| 2 years | ${year_delay_cost * 2:.0f}M |
| 3 years | ${year_delay_cost * 3:.0f}M+ |

*Plus compounding new customer LTV loss and competitive positioning erosion.*
        """)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — COMPETITIVE LANDSCAPE
# ══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown('<div class="section-header">UCP Competitive Landscape</div>', unsafe_allow_html=True)
    st.caption("How Five Below stacks up against key competitors on UCP readiness and catalog quality.")

    # Update Five Below scores dynamically
    comp_data = []
    for c in COMPETITORS:
        row = c.copy()
        if c["retailer"] == "Five Below (current)":
            row["ucp_score"] = score
            row["catalog_completeness"] = st.session_state.catalog_completeness
        elif c["retailer"] == "Five Below (Year 3 target)":
            row["ucp_score"] = 91
            row["catalog_completeness"] = 97
        comp_data.append(row)

    comp_df = pd.DataFrame(comp_data)

    fig_comp = px.scatter(
        comp_df,
        x="catalog_completeness",
        y="ucp_score",
        color="status",
        size=[30, 30, 20, 20, 25, 25],
        text="retailer",
        color_discrete_map={
            "Live on UCP": "#10b981",
            "Not started": "#ef4444",
            "Evaluating": "#f59e0b",
            "Target": "#3b82f6",
        },
        title="UCP Score vs. Catalog Completeness by Retailer",
        labels={"catalog_completeness": "Catalog Completeness (%)", "ucp_score": "UCP Readiness Score"},
        height=420,
    )
    fig_comp.update_traces(textposition="top center", marker=dict(opacity=0.85))
    fig_comp.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font_color="#1e293b",
        xaxis=dict(range=[0, 105]),
        yaxis=dict(range=[0, 105]),
    )
    fig_comp.add_hline(y=85, line_dash="dot", line_color="#94a3b8",
                       annotation_text="UCP Ready threshold (85)", annotation_position="right")
    fig_comp.add_vline(x=95, line_dash="dot", line_color="#94a3b8",
                       annotation_text="Catalog target (95%)", annotation_position="top")
    st.plotly_chart(fig_comp, use_container_width=True)

    st.divider()
    st.markdown('<div class="section-header">Competitor Detail</div>', unsafe_allow_html=True)

    display_df = comp_df[["retailer", "ucp_score", "catalog_completeness", "status", "notes"]].copy()
    display_df.columns = ["Retailer", "UCP Score", "Catalog %", "Status", "Notes"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown('<div class="section-header">What UCP-Live Competitors Can Do That Five Below Cannot</div>', unsafe_allow_html=True)

    gaps = [
        ("A shopper asks Gemini: 'Find me fun party supplies under $10'",
         "Walmart + Target products surface. Five Below is invisible.",
         "🔴 Critical"),
        ("AI agent completes a purchase without the shopper visiting a website",
         "Walmart processes agentic checkout. Five Below has no /cart/add endpoint.",
         "🔴 Critical"),
        ("Shopper asks: 'Is this toy available at a store near me?'",
         "Target returns real-time store availability. Five Below returns nothing (no /availability endpoint).",
         "🔴 Critical"),
        ("AI agent tracks an order post-purchase",
         "Walmart returns order status in-conversation. Five Below has no /orders endpoint.",
         "🟡 High"),
        ("Shopper asks AI to initiate a return",
         "Target handles return initiation in-agent. Five Below requires website visit.",
         "🟡 High"),
    ]

    for scenario, impact, severity in gaps:
        css = "gap-critical" if "🔴" in severity else "gap-moderate"
        st.markdown(f"""
        <div class="{css}">
            <strong>{severity} {scenario}</strong><br>
            <span style="font-size:13px">{impact}</span>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — REMEDIATION ROADMAP
# ══════════════════════════════════════════════════════════════════════════════

with tab5:
    st.markdown('<div class="section-header">UCP Readiness Remediation Roadmap</div>', unsafe_allow_html=True)
    st.caption("Four-phase plan to achieve full UCP certification — from data foundation to live agentic commerce.")

    # Score progression chart
    phases = ["Current State"] + [p["phase"].split("—")[0].strip() for p in REMEDIATION_PLAN]
    scores_progression = [score] + [p["ucp_score_after"] for p in REMEDIATION_PLAN]
    colors_progression = [
        "#ef4444" if s < 40 else ("#f59e0b" if s < 65 else ("#3b82f6" if s < 85 else "#10b981"))
        for s in scores_progression
    ]

    fig_prog = go.Figure()
    fig_prog.add_trace(go.Scatter(
        x=phases, y=scores_progression,
        mode="lines+markers+text",
        text=[f"{s}" for s in scores_progression],
        textposition="top center",
        line=dict(color="#3b82f6", width=3),
        marker=dict(size=14, color=colors_progression, line=dict(color="white", width=2)),
    ))
    fig_prog.add_hline(y=85, line_dash="dot", line_color="#10b981",
                       annotation_text="UCP Ready (85)", annotation_position="right")
    fig_prog.update_layout(
        title="UCP Score Progression by Phase",
        plot_bgcolor="white", paper_bgcolor="white",
        font_color="#1e293b", height=320,
        yaxis=dict(range=[0, 105], title="UCP Score"),
        xaxis_title="",
    )
    st.plotly_chart(fig_prog, use_container_width=True)

    st.divider()

    for phase in REMEDIATION_PLAN:
        phase_name = phase["phase"]
        with st.expander(f"**{phase_name}** — Score after: {phase['ucp_score_after']}/100 {phase['priority']}"):
            c1, c2 = st.columns([1, 3])
            with c1:
                st.metric("Duration", phase["duration"])
                st.metric("UCP Score After", f"{phase['ucp_score_after']}/100")
                st.markdown(f"**Priority:** {phase['priority']}")
            with c2:
                st.markdown("**Actions:**")
                for action in phase["actions"]:
                    st.markdown(f"- {action}")

    st.divider()
    st.markdown('<div class="section-header">Investment Summary</div>', unsafe_allow_html=True)

    investment = pd.DataFrame([
        {"Line Item": "Phase 1 — Data Foundation (MDM + EDP + feeds)", "Estimated Cost": "$3.5–4.1M", "Year": "Year 1"},
        {"Line Item": "Phase 2 — UCP API Layer (FastAPI + search)", "Estimated Cost": "$600K one-time", "Year": "Year 2–3"},
        {"Line Item": "Phase 3 — Transactional Endpoints (cart + checkout + post-purchase)", "Estimated Cost": "$400K one-time", "Year": "Year 3"},
        {"Line Item": "Phase 4 — Optimization + Platform Expansion", "Estimated Cost": "$200K/yr", "Year": "Year 3+"},
        {"Line Item": "**Total (3-year)**", "Estimated Cost": "**~$5.3–6.1M**", "Year": "Year 1–3"},
    ])
    st.dataframe(investment, use_container_width=True, hide_index=True)

    total_opp = revenue_opportunity()["total_opportunity"]
    st.markdown(f"""
    **ROI Summary:**
    - 3-year investment: ~$5.3–6.1M
    - Annual UCP revenue opportunity (at full readiness): **${total_opp:.0f}M/yr**
    - **Payback period: < 6 months** after UCP go-live
    - 3-year cumulative ROI: **~{int(total_opp * 3 / 5.7)}x**
    """)

    st.divider()
    st.markdown('<div class="section-header">Download This Assessment</div>', unsafe_allow_html=True)

    report_lines = [
        "# UCP Readiness Assessment Report",
        f"Generated: {datetime.now().strftime('%B %d, %Y')}",
        "",
        "## Overall Score",
        f"UCP Readiness Score: {score}/100 — {label} ({status_text})",
        f"- Catalog Score:  {cat_score}/40",
        f"- Feed Score:     {fd_score}/25",
        f"- Endpoint Score: {ep_score}/35",
        "",
        "## Catalog Inputs",
        f"- Overall Catalog Completeness: {st.session_state.catalog_completeness}%",
        f"- Google Taxonomy Coverage: {st.session_state.taxonomy_coverage}%",
        f"- Image Coverage: {st.session_state.image_coverage}%",
        f"- Attribute Coverage: {st.session_state.attribute_coverage}%",
        f"- GTIN Coverage: {st.session_state.gtin_coverage}%",
        f"- Pricing Feed Freshness: {freshness_label(st.session_state.pricing_freshness_min)}",
        f"- Inventory Feed Freshness: {freshness_label(st.session_state.inventory_freshness_min)}",
        "",
        "## Endpoint Status",
    ]
    for ep, key in zip(UCP_ENDPOINTS, ep_keys):
        report_lines.append(f"- {ep['endpoint']}: {st.session_state[key]}")

    report_lines += [
        "",
        "## Revenue Opportunity",
        f"- Annual Revenue: ${opp['annual_revenue']:,}M",
        f"- UCP Conversion Lift: ${opp['ucp_conversion_lift']:,}M",
        f"- New Customer Revenue: ${opp['new_customer_revenue']:,}M",
        f"- Total Annual Opportunity: ${opp['total_opportunity']:,}M",
        "",
        "## Next Steps",
        "1. Close catalog data gaps (MDM completeness, taxonomy mapping, image backfill)",
        "2. Build real-time EDP pricing and inventory feeds",
        "3. Develop FastAPI UCP endpoint layer on EDP Gold",
        "4. Register with Google UCP sandbox and begin certification testing",
        "5. Launch transactional endpoints (cart, checkout, post-purchase)",
    ]

    report_text = "\n".join(report_lines)
    st.download_button(
        "📥 Download Assessment as Markdown",
        data=report_text,
        file_name=f"ucp_readiness_assessment_{datetime.now().strftime('%Y%m%d')}.md",
        mime="text/markdown",
        use_container_width=True,
    )
