import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import io
from datetime import datetime


# ── SHARED SIDEBAR (injected on every page) ───────────────────────────────────
st.markdown("""
<style>
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebar"] { background: #0f172a; }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] hr { border-color: #1e293b !important; }
[data-testid="stSidebar"] a { color: #93c5fd !important; }
.sidebar-brand { font-size:20px; font-weight:800; color:#ffffff !important; letter-spacing:-0.5px; margin-bottom:2px; }
.sidebar-sub   { font-size:11px; color:#64748b !important; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:16px; }
.nav-label     { font-size:10px; font-weight:700; color:#475569 !important; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sidebar-brand">🛒 Five Below</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Data &amp; AI Strategy</div>', unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="nav-label">Tools</div>', unsafe_allow_html=True)
    st.page_link("app.py",                                 label="🏠  Home & Strategy Overview")
    st.page_link("pages/1_🤖_AI_Prioritization.py",       label="🤖  AI Use Case Prioritization")
    st.page_link("pages/2_🏛️_Data_Quality_Dashboard.py",  label="🏛️  Data Quality Dashboard")
    st.page_link("pages/3_🛍️_UCP_Scorecard.py",           label="🛍️  UCP Readiness Scorecard")
    st.divider()
    st.markdown('<div class="nav-label">About</div>', unsafe_allow_html=True)
    st.markdown("**Kiran Thella**  \nAI Product Manager  \n13+ yrs · Nike · Gilead · eBay")
    st.markdown("")
    st.markdown("[🔗 LinkedIn](https://www.linkedin.com/in/kiranthella/)   [💻 GitHub](https://github.com/KKThella)")


# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
# ── STYLES ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.tier-1  { background:#d1fae5; color:#065f46; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:600; }
.tier-2  { background:#fef3c7; color:#92400e; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:600; }
.tier-3  { background:#fee2e2; color:#991b1b; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:600; }
.metric-box { background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px 16px; text-align:center; }
.metric-label { font-size:12px; color:#64748b; margin-bottom:4px; }
.metric-value { font-size:24px; font-weight:700; color:#1e293b; }
.section-header { font-size:13px; font-weight:600; color:#475569; text-transform:uppercase;
                  letter-spacing:0.06em; margin:1.2rem 0 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ── DEFAULT USE CASES ─────────────────────────────────────────────────────────
DEFAULT_USE_CASES = [
    {"name": "LLM Store Associate Agent", "domain": "Store Operations",
     "description": "RAG-based LLM helping associates answer product, inventory, and policy questions in real time.",
     "impact": 4, "data_readiness": 5, "feasibility": 5, "speed": 5,
     "value_hypothesis": "15% reduction in customer escalations; $6M labor productivity gain",
     "success_metric": "Query resolution rate, associate adoption >80%, store NPS +8pts",
     "data_required": "Product MDM, real-time inventory, policy docs"},

    {"name": "Markdown Optimization ML", "domain": "Merchandising",
     "description": "ML model predicting optimal markdown % by SKU × store × week to maximize sell-through while protecting margin.",
     "impact": 5, "data_readiness": 4, "feasibility": 4, "speed": 4,
     "value_hypothesis": "10% reduction in markdown spend = $18M annual margin improvement",
     "success_metric": "Sell-through rate +8pts; markdown spend as % revenue -1.2pts",
     "data_required": "3yr sales history, store traffic, seasonal flags (EDP Gold)"},

    {"name": "Demand Sensing & Inventory Allocation", "domain": "Supply Chain",
     "description": "Ensemble model combining POS velocity, social trends, and search signals for store-level allocation recommendations.",
     "impact": 5, "data_readiness": 4, "feasibility": 4, "speed": 3,
     "value_hypothesis": "3% in-stock rate improvement = $12M recovered sales + $8M inventory savings",
     "success_metric": "In-stock rate (trending SKUs) +16pts; inventory turns 6.2x → 7.5x",
     "data_required": "Real-time POS (<15 min), social API, store MDM, weather data"},

    {"name": "Customer Churn Prediction", "domain": "Marketing",
     "description": "ML churn model on CDP behavioral signals triggering win-back at 21-day inactivity vs. current 60-day batch.",
     "impact": 4, "data_readiness": 3, "feasibility": 4, "speed": 4,
     "value_hypothesis": "5% churn reduction = $12M recovered LTV from loyalty base",
     "success_metric": "Win-back CVR +5pts; annual churn rate 35% → <28%",
     "data_required": "CDP unified profiles, purchase history, email engagement"},

    {"name": "UCP Catalog Exposure", "domain": "E-Commerce",
     "description": "UCP-compliant API layer exposing Five Below product catalog to AI shopping agents (Google Gemini, AI Mode).",
     "impact": 5, "data_readiness": 3, "feasibility": 4, "speed": 3,
     "value_hypothesis": "$33–52M incremental revenue from AI-native shopping discovery",
     "success_metric": "UCP catalog coverage 100%; AI-referred revenue; new customer acquisition via agents",
     "data_required": "Product MDM (>97% complete), real-time pricing/inventory (<5 min)"},

    {"name": "Personalized Product Recommendations", "domain": "E-Commerce",
     "description": "Hybrid collaborative filtering + content-based model on CDP unified customer profiles.",
     "impact": 4, "data_readiness": 3, "feasibility": 4, "speed": 3,
     "value_hypothesis": "8–12% lift in AOV = $4–6M incremental e-commerce revenue",
     "success_metric": "AOV +10%; recommendation CTR; add-to-cart rate +0.7%",
     "data_required": "CDP profiles, browse history, purchase history, Product MDM"},

    {"name": "Dynamic Clearance Pricing", "domain": "Merchandising",
     "description": "Reinforcement learning agent optimizing clearance markdown % daily within guardrails to maximize sell-through.",
     "impact": 4, "data_readiness": 3, "feasibility": 3, "speed": 3,
     "value_hypothesis": "8% improvement in clearance sell-through = $7M margin recovery",
     "success_metric": "Clearance sell-through rate; margin per clearance unit vs. baseline",
     "data_required": "POS velocity, inventory levels, pricing rules, competitor pricing"},

    {"name": "Automated Vendor Scorecards", "domain": "Supply Chain",
     "description": "LLM-assisted synthesis of vendor performance across delivery, quality, compliance, and cost from EDI + WMS data.",
     "impact": 3, "data_readiness": 3, "feasibility": 4, "speed": 4,
     "value_hypothesis": "80% reduction in manual vendor review time; faster risk identification",
     "success_metric": "Vendor review cycle time; analyst hours saved; vendor issue escalation rate",
     "data_required": "Vendor MDM, EDI feeds, WMS delivery data, quality records"},

    {"name": "Customer Support Chat (E-commerce)", "domain": "Marketing",
     "description": "RAG-based LLM for online customer support — order status, returns, product questions grounded on EDP + CDP.",
     "impact": 3, "data_readiness": 3, "feasibility": 4, "speed": 3,
     "value_hypothesis": "30% reduction in human support tickets = $2M annual support cost savings",
     "success_metric": "First-contact resolution rate; CSAT; ticket deflection rate",
     "data_required": "Order management data, Returns data, Product MDM, Policy docs"},

    {"name": "Shrink / Loss Prevention ML", "domain": "Store Operations",
     "description": "Anomaly detection model identifying high-shrink risk SKUs and store patterns to prioritize loss prevention focus.",
     "impact": 4, "data_readiness": 2, "feasibility": 3, "speed": 2,
     "value_hypothesis": "10% reduction in shrink = $15M+ annual P&L improvement",
     "success_metric": "Shrink rate by store tier; loss prevention ROI; model precision/recall",
     "data_required": "POS exceptions, inventory adjustments, store ops data, camera feeds (future)"},

    {"name": "Planogram Optimization", "domain": "Merchandising",
     "description": "Computer vision + ML to optimize in-store product placement based on traffic patterns, category affinity, and sales velocity.",
     "impact": 4, "data_readiness": 2, "feasibility": 2, "speed": 2,
     "value_hypothesis": "5% lift in impulse purchase rate = $20M+ revenue opportunity",
     "success_metric": "Sales per linear foot; category adjacency lift; planogram compliance",
     "data_required": "Store layout data, traffic heatmaps, POS by location, store MDM"},
]

DOMAINS = ["All Domains", "Merchandising", "Supply Chain", "Store Operations", "Marketing", "E-Commerce", "Finance"]

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "use_cases" not in st.session_state:
    st.session_state.use_cases = DEFAULT_USE_CASES.copy()
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dashboard"

# ── HELPERS ───────────────────────────────────────────────────────────────────
def score_total(uc):
    return uc["impact"] + uc["data_readiness"] + uc["feasibility"] + uc["speed"]

def tier(total):
    if total >= 15: return "Tier 1", "tier-1", "🟢"
    if total >= 11: return "Tier 2", "tier-2", "🟡"
    return "Tier 3", "tier-3", "🔴"

def effort_score(uc):
    # Effort = inverse of feasibility + inverse of speed (higher = harder)
    return (6 - uc["feasibility"]) + (6 - uc["speed"])

def df_from_state():
    rows = []
    for uc in st.session_state.use_cases:
        total = score_total(uc)
        t_label, _, t_icon = tier(total)
        rows.append({
            "Use Case": uc["name"],
            "Domain": uc["domain"],
            "Impact": uc["impact"],
            "Data Readiness": uc["data_readiness"],
            "Feasibility": uc["feasibility"],
            "Speed": uc["speed"],
            "Total Score": total,
            "Tier": t_label,
            "Icon": t_icon,
            "Effort": effort_score(uc),
        })
    return pd.DataFrame(rows).sort_values("Total Score", ascending=False)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Five_Below_Logo.svg/320px-Five_Below_Logo.svg.png",
             width=160)
    st.markdown("### Retail AI Prioritization")
    st.caption("Enterprise AI use case scoring framework for value retail.")
    st.divider()

    domain_filter = st.selectbox("Filter by domain", DOMAINS)
    st.divider()

    st.markdown("**Scoring guide**")
    st.caption("Each dimension scored 1–5")
    st.markdown("""
| Score | Meaning |
|---|---|
| 5 | Exceptional |
| 4 | Strong |
| 3 | Moderate |
| 2 | Limited |
| 1 | Minimal |
""")
    st.divider()
    st.markdown("**Tier thresholds**")
    st.markdown("🟢 **Tier 1** — Score ≥ 15 (Build now)")
    st.markdown("🟡 **Tier 2** — Score 11–14 (Build next)")
    st.markdown("🔴 **Tier 3** — Score ≤ 10 (Deprioritize)")
    st.divider()
    st.caption(f"Built by [Kiran Thella](https://linkedin.com/in/kiran-thella) · {datetime.now().strftime('%b %Y')}")

# ── HEADER ────────────────────────────────────────────────────────────────────
st.title("Retail AI Use Case Prioritization Framework")
st.caption("Evaluate, score, and rank enterprise AI initiatives across retail domains — grounded in data readiness, business impact, and speed to value.")

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🗂️ Priority Matrix", "➕ Add Use Case", "📋 Value Hypothesis"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    df = df_from_state()
    if domain_filter != "All Domains":
        df = df[df["Domain"] == domain_filter]

    # ── Summary metrics
    t1 = len(df[df["Tier"] == "Tier 1"])
    t2 = len(df[df["Tier"] == "Tier 2"])
    t3 = len(df[df["Tier"] == "Tier 3"])
    avg_score = round(df["Total Score"].mean(), 1) if len(df) else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Total Use Cases</div><div class="metric-value">{len(df)}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-box"><div class="metric-label">🟢 Tier 1 (Build Now)</div><div class="metric-value" style="color:#065f46">{t1}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-box"><div class="metric-label">🟡 Tier 2 (Build Next)</div><div class="metric-value" style="color:#92400e">{t2}</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Avg Priority Score</div><div class="metric-value">{avg_score}/20</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Ranked table
    st.markdown('<div class="section-header">Prioritized Use Case Backlog</div>', unsafe_allow_html=True)

    for _, row in df.iterrows():
        uc = next(u for u in st.session_state.use_cases if u["name"] == row["Use Case"])
        t_label, t_class, t_icon = tier(row["Total Score"])

        with st.expander(f"{t_icon} **{row['Use Case']}** — {row['Domain']} &nbsp; | &nbsp; Score: {row['Total Score']}/20"):
            col_left, col_right = st.columns([2, 1])
            with col_left:
                st.markdown(f"**Description:** {uc['description']}")
                st.markdown(f"**Value hypothesis:** {uc['value_hypothesis']}")
                st.markdown(f"**Success metric:** {uc['success_metric']}")
                st.markdown(f"**Data required:** {uc['data_required']}")
            with col_right:
                st.markdown(f'<span class="{t_class}">{t_label}</span>', unsafe_allow_html=True)
                scores_df = pd.DataFrame({
                    "Dimension": ["Impact", "Data Readiness", "Feasibility", "Speed"],
                    "Score": [uc["impact"], uc["data_readiness"], uc["feasibility"], uc["speed"]]
                })
                fig = px.bar(scores_df, x="Score", y="Dimension", orientation="h",
                             color="Score", color_continuous_scale=["#fef3c7", "#10b981"],
                             range_x=[0, 5], height=160)
                fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                                  coloraxis_showscale=False,
                                  plot_bgcolor="white", paper_bgcolor="white",
                                  font=dict(size=11))
                fig.update_xaxes(range=[0, 5], dtick=1, showgrid=True, gridcolor="#f1f5f9")
                fig.update_yaxes(showgrid=False)
                st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── Export
    export_df = df.drop(columns=["Icon", "Effort"])
    csv = export_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Export to CSV", csv,
                       f"retail_ai_prioritization_{datetime.now().strftime('%Y%m%d')}.csv",
                       "text/csv")

# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — PRIORITY MATRIX (2×2)
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    df_all = df_from_state()
    if domain_filter != "All Domains":
        df_all = df_all[df_all["Domain"] == domain_filter]

    st.markdown('<div class="section-header">Impact vs. Effort Matrix</div>', unsafe_allow_html=True)
    st.caption("Bubble size = total priority score. Quadrant: top-left = quick wins, top-right = big bets, bottom-left = fill-ins, bottom-right = thankless.")

    domain_colors = {
        "Merchandising": "#6366f1",
        "Supply Chain": "#f59e0b",
        "Store Operations": "#10b981",
        "Marketing": "#ec4899",
        "E-Commerce": "#3b82f6",
        "Finance": "#8b5cf6",
    }

    fig2 = go.Figure()

    for domain in df_all["Domain"].unique():
        d_df = df_all[df_all["Domain"] == domain]
        for _, row in d_df.iterrows():
            uc = next(u for u in st.session_state.use_cases if u["name"] == row["Use Case"])
            fig2.add_trace(go.Scatter(
                x=[row["Effort"]],
                y=[row["Impact"]],
                mode="markers+text",
                marker=dict(
                    size=row["Total Score"] * 3.5,
                    color=domain_colors.get(domain, "#94a3b8"),
                    opacity=0.8,
                    line=dict(color="white", width=2)
                ),
                text=[row["Use Case"]],
                textposition="top center",
                textfont=dict(size=10),
                name=domain,
                hovertemplate=(
                    f"<b>{row['Use Case']}</b><br>"
                    f"Domain: {domain}<br>"
                    f"Impact: {row['Impact']}/5<br>"
                    f"Effort: {row['Effort']}/8 (lower = easier)<br>"
                    f"Total Score: {row['Total Score']}/20<br>"
                    f"Tier: {row['Tier']}<extra></extra>"
                ),
                legendgroup=domain,
                showlegend=True,
            ))

    # Quadrant lines
    fig2.add_hline(y=3, line_dash="dot", line_color="#cbd5e1", line_width=1)
    fig2.add_vline(x=5, line_dash="dot", line_color="#cbd5e1", line_width=1)

    # Quadrant labels
    fig2.add_annotation(x=2.5, y=4.8, text="⚡ Quick Wins", showarrow=False,
                         font=dict(size=11, color="#10b981"), bgcolor="#f0fdf4")
    fig2.add_annotation(x=7.5, y=4.8, text="🚀 Big Bets", showarrow=False,
                         font=dict(size=11, color="#6366f1"), bgcolor="#eef2ff")
    fig2.add_annotation(x=2.5, y=1.2, text="📋 Fill-ins", showarrow=False,
                         font=dict(size=11, color="#94a3b8"), bgcolor="#f8fafc")
    fig2.add_annotation(x=7.5, y=1.2, text="⚠️ Reconsider", showarrow=False,
                         font=dict(size=11, color="#ef4444"), bgcolor="#fef2f2")

    fig2.update_layout(
        height=550,
        xaxis=dict(title="Effort (lower = easier)", range=[0, 10], dtick=1,
                   showgrid=True, gridcolor="#f1f5f9"),
        yaxis=dict(title="Business Impact (1–5)", range=[0.5, 5.5], dtick=1,
                   showgrid=True, gridcolor="#f1f5f9"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        font=dict(size=11),
        margin=dict(l=60, r=20, t=20, b=80),
    )
    st.plotly_chart(fig2, use_container_width=True)


    # ── Domain breakdown bar chart
    st.markdown('<div class="section-header">Average Priority Score by Domain</div>', unsafe_allow_html=True)
    domain_avg = df_all.groupby("Domain")["Total Score"].mean().reset_index().sort_values("Total Score", ascending=False)
    fig3 = px.bar(domain_avg, x="Domain", y="Total Score",
                  color="Total Score", color_continuous_scale=["#fef3c7", "#10b981"],
                  range_y=[0, 20], height=280, text="Total Score")
    fig3.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    fig3.update_layout(coloraxis_showscale=False, plot_bgcolor="white",
                       paper_bgcolor="white", margin=dict(t=10, b=10),
                       font=dict(size=11))
    fig3.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
    st.plotly_chart(fig3, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — ADD USE CASE
# ════════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Add a New AI Use Case</div>', unsafe_allow_html=True)
    st.caption("Score your use case across four dimensions. The framework will assign a priority tier automatically.")

    with st.form("add_use_case", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Use case name *", placeholder="e.g. Real-Time Replenishment ML")
            domain = st.selectbox("Business domain *", DOMAINS[1:])
            description = st.text_area("Description *", height=80,
                                       placeholder="What problem does this solve? What's the AI approach?")
        with col2:
            value_hypothesis = st.text_area("Value hypothesis *", height=80,
                                            placeholder="e.g. 10% reduction in stockouts = $8M recovered sales")
            success_metric = st.text_input("Primary success metric *",
                                           placeholder="e.g. In-stock rate +5pts; inventory turns +1.2x")
            data_required = st.text_input("Data required *",
                                          placeholder="e.g. Real-time POS, Vendor MDM, Store attributes")

        st.markdown("**Score each dimension (1 = minimal, 5 = exceptional)**")
        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            impact = st.slider("Business Impact", 1, 5, 3,
                               help="Revenue lift, cost savings, or risk reduction potential")
        with sc2:
            data_readiness = st.slider("Data Readiness", 1, 5, 3,
                                       help="Is required data clean, available, and governed?")
        with sc3:
            feasibility = st.slider("Technical Feasibility", 1, 5, 3,
                                    help="Model complexity, latency requirements, integration scope")
        with sc4:
            speed = st.slider("Speed to Value", 1, 5, 3,
                              help="How fast can you ship a production MVP?")

        total = impact + data_readiness + feasibility + speed
        t_label, _, t_icon = tier(total)
        st.info(f"{t_icon} This use case scores **{total}/20** → **{t_label}**")

        submitted = st.form_submit_button("Add to Backlog", type="primary")
        if submitted:
            if not name or not description or not value_hypothesis:
                st.error("Please fill in all required fields (*)")
            elif any(u["name"].lower() == name.lower() for u in st.session_state.use_cases):
                st.error(f"A use case named '{name}' already exists.")
            else:
                st.session_state.use_cases.append({
                    "name": name, "domain": domain, "description": description,
                    "impact": impact, "data_readiness": data_readiness,
                    "feasibility": feasibility, "speed": speed,
                    "value_hypothesis": value_hypothesis,
                    "success_metric": success_metric,
                    "data_required": data_required,
                })
                st.success(f"✅ '{name}' added as {t_label}! Go to Dashboard to see it ranked.")

    st.divider()

    # ── Delete a use case
    st.markdown('<div class="section-header">Remove a Use Case</div>', unsafe_allow_html=True)
    names = [u["name"] for u in st.session_state.use_cases]
    to_delete = st.selectbox("Select use case to remove", names)
    if st.button("🗑 Remove", type="secondary"):
        st.session_state.use_cases = [u for u in st.session_state.use_cases if u["name"] != to_delete]
        st.success(f"Removed '{to_delete}'")
        st.rerun()

    if st.button("↺ Reset to defaults"):
        st.session_state.use_cases = DEFAULT_USE_CASES.copy()
        st.success("Reset to default use cases")
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — VALUE HYPOTHESIS GENERATOR
# ════════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">Value Hypothesis Builder</div>', unsafe_allow_html=True)
    st.caption("Generate a structured value hypothesis and success metric framework for any AI use case. Use this for stakeholder alignment, business case approval, or AI Review Council submissions.")

    names_for_hyp = [u["name"] for u in st.session_state.use_cases]
    selected = st.selectbox("Select a use case", names_for_hyp)
    uc_sel = next(u for u in st.session_state.use_cases if u["name"] == selected)
    total_sel = score_total(uc_sel)
    t_label_sel, t_class_sel, t_icon_sel = tier(total_sel)

    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Impact", f"{uc_sel['impact']}/5")
    col_b.metric("Data Readiness", f"{uc_sel['data_readiness']}/5")
    col_c.metric("Feasibility", f"{uc_sel['feasibility']}/5")
    col_d.metric("Speed to Value", f"{uc_sel['speed']}/5")

    st.markdown("---")
    st.markdown(f"### {t_icon_sel} {selected}")
    st.markdown(f'<span class="{t_class_sel}">{t_label_sel} · Score {total_sel}/20</span>', unsafe_allow_html=True)

    st.markdown("#### Problem Statement")
    st.info(uc_sel["description"])

    st.markdown("#### Value Hypothesis")
    st.success(f"**If** we deploy {selected}, **then** we expect: {uc_sel['value_hypothesis']}.")

    st.markdown("#### Success Metrics")
    metrics_text = uc_sel["success_metric"]
    for metric in metrics_text.split(";"):
        metric = metric.strip()
        if metric:
            st.markdown(f"- {metric}")

    st.markdown("#### Data Requirements")
    st.warning(f"**Required before PoC can begin:** {uc_sel['data_required']}")

    st.markdown("#### Recommended A/B Test Design")
    ab_template = f"""
**Control group:** Existing rule-based or manual approach
**Treatment group:** {selected} recommendations
**Minimum sample size:** 10,000 observations per cell
**Test duration:** 6–8 weeks (minimum 1 seasonal cycle if applicable)
**Primary metric:** {metrics_text.split(';')[0].strip() if metrics_text else 'TBD'}
**Statistical significance threshold:** p < 0.05
**Rollback trigger:** Primary metric regression > 3% vs. control
"""
    st.markdown(ab_template)

    st.markdown("#### AI Review Council Submission Template")
    submission = f"""
**Use Case:** {selected}
**Domain:** {uc_sel['domain']}
**Priority Tier:** {t_label_sel} (Score: {total_sel}/20)

**Problem:** {uc_sel['description']}

**Value Hypothesis:** {uc_sel['value_hypothesis']}

**Success Metrics:** {uc_sel['success_metric']}

**Data Requirements:** {uc_sel['data_required']}

**Bias / Risk Assessment:** [To be completed by submitting team]

**Explainability Approach:** [Specify: SHAP values / business rules override / LLM grounding]

**Human Override Mechanism:** [Describe how a human can review or override the AI recommendation]

**Submitted by:** ___________  |  **Date:** {datetime.now().strftime('%B %d, %Y')}
"""
    st.code(submission, language=None)
    st.download_button(
        "⬇ Download Submission Template",
        submission.encode("utf-8"),
        f"AI_Review_{selected.replace(' ', '_')}.txt",
        "text/plain"
    )
