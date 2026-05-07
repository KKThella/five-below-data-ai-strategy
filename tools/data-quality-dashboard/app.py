import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Retail Data Quality Governance Dashboard",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── STYLES ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.sla-pass   { background:#d1fae5; color:#065f46; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:600; }
.sla-warn   { background:#fef3c7; color:#92400e; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:600; }
.sla-breach { background:#fee2e2; color:#991b1b; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:600; }
.tier-1-badge { background:#dbeafe; color:#1e40af; padding:3px 10px; border-radius:12px; font-size:11px; font-weight:600; }
.tier-2-badge { background:#ede9fe; color:#5b21b6; padding:3px 10px; border-radius:12px; font-size:11px; font-weight:600; }
.tier-3-badge { background:#f1f5f9; color:#475569; padding:3px 10px; border-radius:12px; font-size:11px; font-weight:600; }
.section-header { font-size:13px; font-weight:600; color:#475569; text-transform:uppercase; letter-spacing:0.06em; margin:1.2rem 0 0.5rem; }
.escalation-l1 { border-left:4px solid #22c55e; padding:8px 12px; background:#f0fdf4; border-radius:0 8px 8px 0; margin-bottom:8px; }
.escalation-l2 { border-left:4px solid #f59e0b; padding:8px 12px; background:#fffbeb; border-radius:0 8px 8px 0; margin-bottom:8px; }
.escalation-l3 { border-left:4px solid #ef4444; padding:8px 12px; background:#fef2f2; border-radius:0 8px 8px 0; margin-bottom:8px; }
.escalation-l4 { border-left:4px solid #7c3aed; padding:8px 12px; background:#faf5ff; border-radius:0 8px 8px 0; margin-bottom:8px; }
.metric-card { background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:14px 18px; text-align:center; }
.metric-label { font-size:11px; color:#64748b; margin-bottom:4px; text-transform:uppercase; letter-spacing:0.05em; }
.metric-value { font-size:26px; font-weight:700; color:#1e293b; }
.metric-sub   { font-size:11px; color:#94a3b8; margin-top:2px; }
</style>
""", unsafe_allow_html=True)

# ── DATA DEFINITIONS ─────────────────────────────────────────────────────────

DATASETS = {
    "Tier 1 — Mission Critical": [
        {
            "dataset": "Product Pricing (active SKUs)",
            "domain": "Merchandising",
            "owner": "VP Merchandising",
            "steward": "Sr. Analyst, Merch Analytics",
            "completeness_sla": 99.5,
            "accuracy_sla": 99.9,
            "freshness_sla": "< 5 min",
            "consequence": "Incorrect pricing in UCP / POS / e-comm",
            "completeness_actual": 99.7,
            "accuracy_actual": 99.8,
            "freshness_actual_min": 3,
            "freshness_sla_min": 5,
        },
        {
            "dataset": "Store Inventory Levels",
            "domain": "Store Operations",
            "owner": "VP Store Operations",
            "steward": "Sr. Analyst, Store Analytics",
            "completeness_sla": 99.0,
            "accuracy_sla": 98.0,
            "freshness_sla": "< 15 min",
            "consequence": "Stockout errors, incorrect allocation",
            "completeness_actual": 98.6,
            "accuracy_actual": 97.4,
            "freshness_actual_min": 18,
            "freshness_sla_min": 15,
        },
        {
            "dataset": "Product Availability Flags",
            "domain": "Merchandising",
            "owner": "VP Merchandising",
            "steward": "Sr. Analyst, Merch Analytics",
            "completeness_sla": 99.5,
            "accuracy_sla": 99.9,
            "freshness_sla": "< 5 min",
            "consequence": "Selling discontinued items",
            "completeness_actual": 99.6,
            "accuracy_actual": 99.9,
            "freshness_actual_min": 4,
            "freshness_sla_min": 5,
        },
    ],
    "Tier 2 — Business Critical": [
        {
            "dataset": "Product MDM (full attributes)",
            "domain": "Merchandising",
            "owner": "VP Merchandising",
            "steward": "Sr. Analyst, Merch Analytics",
            "completeness_sla": 97.0,
            "accuracy_sla": 99.0,
            "freshness_sla": "< 4 hours",
            "consequence": "Stale catalog data in BI and AI models",
            "completeness_actual": 97.8,
            "accuracy_actual": 99.2,
            "freshness_actual_min": 210,
            "freshness_sla_min": 240,
        },
        {
            "dataset": "Customer Unified Profiles (CDP)",
            "domain": "Customer & Marketing",
            "owner": "VP Marketing",
            "steward": "Sr. Analyst, CRM",
            "completeness_sla": 90.0,
            "accuracy_sla": 97.0,
            "freshness_sla": "< 1 hour",
            "consequence": "Stale segments, incorrect personalization",
            "completeness_actual": 91.3,
            "accuracy_actual": 96.4,
            "freshness_actual_min": 72,
            "freshness_sla_min": 60,
        },
        {
            "dataset": "Vendor MDM",
            "domain": "Supply Chain",
            "owner": "VP Supply Chain",
            "steward": "Sr. Analyst, SC Analytics",
            "completeness_sla": 95.0,
            "accuracy_sla": 98.0,
            "freshness_sla": "< 24 hours",
            "consequence": "Incorrect vendor routing or PO mismatch",
            "completeness_actual": 96.1,
            "accuracy_actual": 98.5,
            "freshness_actual_min": 360,
            "freshness_sla_min": 1440,
        },
        {
            "dataset": "Store MDM",
            "domain": "Store Operations",
            "owner": "VP Store Operations",
            "steward": "Sr. Analyst, Store Analytics",
            "completeness_sla": 99.0,
            "accuracy_sla": 99.0,
            "freshness_sla": "< 24 hours",
            "consequence": "Store attributes incorrect in allocation models",
            "completeness_actual": 99.4,
            "accuracy_actual": 99.1,
            "freshness_actual_min": 480,
            "freshness_sla_min": 1440,
        },
    ],
    "Tier 3 — Analytical": [
        {
            "dataset": "Historical Sales (Gold Layer)",
            "domain": "Merchandising",
            "owner": "VP Merchandising",
            "steward": "Sr. Analyst, Merch Analytics",
            "completeness_sla": 98.0,
            "accuracy_sla": 99.0,
            "freshness_sla": "Daily by 6am ET",
            "consequence": "Stale training data for ML models",
            "completeness_actual": 98.3,
            "accuracy_actual": 99.1,
            "freshness_actual_min": 480,
            "freshness_sla_min": 1440,
        },
        {
            "dataset": "Customer Segments (CDP)",
            "domain": "Customer & Marketing",
            "owner": "VP Marketing",
            "steward": "Sr. Analyst, CRM",
            "completeness_sla": 95.0,
            "accuracy_sla": 97.0,
            "freshness_sla": "Daily",
            "consequence": "Wrong segment targeting in campaigns",
            "completeness_actual": 95.8,
            "accuracy_actual": 97.2,
            "freshness_actual_min": 720,
            "freshness_sla_min": 1440,
        },
        {
            "dataset": "AI Model Training Datasets",
            "domain": "AI / ML",
            "owner": "CDO / Data Office",
            "steward": "Data Science Lead",
            "completeness_sla": 97.0,
            "accuracy_sla": 99.0,
            "freshness_sla": "Weekly refresh",
            "consequence": "Model drift; degraded prediction quality",
            "completeness_actual": 97.5,
            "accuracy_actual": 99.0,
            "freshness_actual_min": 2880,
            "freshness_sla_min": 10080,
        },
    ],
}

RACI = [
    {"role": "Domain Data Owner (VP-level)", "accountable": "Data policy for their domain",
     "responsible": "Approving attribute definitions, SLAs",
     "consulted": "Cross-domain decisions", "informed": "Quality scorecard weekly"},
    {"role": "Data Steward (Sr. Analyst)", "accountable": "Daily quality enforcement",
     "responsible": "Flagging quality issues, resolving conflicts",
     "consulted": "New source onboarding", "informed": "Pipeline failures within 1hr"},
    {"role": "Data Custodian (Data Engineer)", "accountable": "Pipeline reliability",
     "responsible": "Building + monitoring pipelines",
     "consulted": "Schema changes", "informed": "SLA breaches"},
    {"role": "Data Consumer (Analyst / PM)", "accountable": "Using certified data",
     "responsible": "Filing data quality tickets",
     "consulted": "New dataset requests", "informed": "Dataset deprecation 30d notice"},
    {"role": "CDO / Data Office", "accountable": "Enterprise standards",
     "responsible": "Policy setting, conflict resolution",
     "consulted": "All major decisions", "informed": "Monthly quality scorecard"},
]

AUTOMATED_CHECKS = [
    {"check": "Null Check", "description": "Flag columns with null rate above threshold", "icon": "🔲"},
    {"check": "Range Check", "description": "Flag numeric values outside expected bounds", "icon": "📏"},
    {"check": "Referential Check", "description": "Flag orphan records (e.g., SKU with no product MDM record)", "icon": "🔗"},
    {"check": "Freshness Check", "description": "Alert if dataset hasn't refreshed within SLA window", "icon": "⏱️"},
    {"check": "Volume Check", "description": "Alert if record count drops >10% from 7-day average (data loss signal)", "icon": "📊"},
    {"check": "Duplicate Check", "description": "Flag duplicate primary keys", "icon": "🔄"},
    {"check": "Format Check", "description": "Flag malformed emails, phone numbers, zip codes", "icon": "✏️"},
]

DECISION_RIGHTS = {
    "Domain Data Owner approval required": [
        "Adding or removing a field from certified Product / Customer / Store MDM schema",
        "Changing the survivorship rule for any golden record attribute",
        "Onboarding a new source system to the EDP",
        "Deprecating a certified dataset (30-day notice required)",
    ],
    "CDO / Data Office approval required": [
        "Cross-domain attribute ownership disputes",
        "Changes to enterprise data classification policy (PII, confidential, public)",
        "Approving a new AI use case for production deployment",
        "Unity Catalog RBAC role changes above analyst level",
        "Any data sharing with external vendors or partners",
    ],
    "Data Stewards can decide independently": [
        "Flagging and quarantining bad records (with notification to custodian)",
        "Approving new analyst access to existing certified datasets",
        "Scheduling ad-hoc data quality audits",
    ],
}

# ── HELPERS ───────────────────────────────────────────────────────────────────

def sla_status(actual, sla, higher_is_better=True):
    """Return (status_label, css_class, delta) for a metric vs SLA."""
    if higher_is_better:
        delta = actual - sla
        if actual >= sla:
            return "✅ Pass", "sla-pass", f"+{delta:.1f}pp"
        elif actual >= sla - 1.0:
            return "⚠️ At Risk", "sla-warn", f"{delta:.1f}pp"
        else:
            return "🔴 Breach", "sla-breach", f"{delta:.1f}pp"
    else:
        # Lower is better (freshness minutes)
        delta = actual - sla
        if actual <= sla:
            return "✅ Pass", "sla-pass", f"-{abs(delta):.0f}min"
        elif actual <= sla * 1.25:
            return "⚠️ At Risk", "sla-warn", f"+{delta:.0f}min"
        else:
            return "🔴 Breach", "sla-breach", f"+{delta:.0f}min over"

def freshness_display(minutes):
    if minutes < 60:
        return f"{minutes}min"
    elif minutes < 1440:
        return f"{minutes//60}hr {minutes%60}min"
    else:
        return f"{minutes//1440}d {(minutes%1440)//60}hr"

def all_datasets():
    rows = []
    for tier, datasets in DATASETS.items():
        for d in datasets:
            d["tier"] = tier
            rows.append(d)
    return rows

def summary_metrics():
    datasets = all_datasets()
    total = len(datasets)
    breaches = 0
    at_risk = 0
    for d in datasets:
        _, c_cls, _ = sla_status(d["completeness_actual"], d["completeness_sla"])
        _, a_cls, _ = sla_status(d["accuracy_actual"], d["accuracy_sla"])
        _, f_cls, _ = sla_status(d["freshness_actual_min"], d["freshness_sla_min"], higher_is_better=False)
        if "breach" in c_cls.lower() or "breach" in a_cls.lower() or "breach" in f_cls.lower():
            breaches += 1
        elif "warn" in c_cls.lower() or "warn" in a_cls.lower() or "warn" in f_cls.lower():
            at_risk += 1
    healthy = total - breaches - at_risk
    return total, healthy, at_risk, breaches

# ── SIDEBAR ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🏛️ DQ Governance")
    st.markdown("**Five Below Data Office**")
    st.caption(f"Last refreshed: {datetime.now().strftime('%b %d, %Y %H:%M')}")
    st.divider()

    selected_domain = st.selectbox(
        "Filter by Domain",
        ["All Domains", "Merchandising", "Store Operations", "Supply Chain", "Customer & Marketing", "AI / ML"]
    )
    selected_tier = st.selectbox(
        "Filter by Tier",
        ["All Tiers", "Tier 1 — Mission Critical", "Tier 2 — Business Critical", "Tier 3 — Analytical"]
    )
    st.divider()
    st.markdown("**Quick links**")
    st.markdown("🔹 [SLA Monitor](#sla-monitor)")
    st.markdown("🔹 [RACI Explorer](#raci-explorer)")
    st.markdown("🔹 [Automated Checks](#automated-checks)")
    st.markdown("🔹 [Escalation Protocol](#escalation-protocol)")
    st.markdown("🔹 [Decision Rights](#decision-rights)")

# ── HEADER ────────────────────────────────────────────────────────────────────

st.title("🏛️ Retail Data Quality Governance Dashboard")
st.markdown(
    "Operationalizing enterprise data quality SLAs, stewardship accountability, "
    "and governance decision rights across Five Below's data platform."
)
st.divider()

# ── SUMMARY METRICS ───────────────────────────────────────────────────────────

total, healthy, at_risk, breaches = summary_metrics()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Datasets</div>
        <div class="metric-value">{total}</div>
        <div class="metric-sub">across all tiers</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">✅ Healthy</div>
        <div class="metric-value" style="color:#059669">{healthy}</div>
        <div class="metric-sub">all SLAs passing</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">⚠️ At Risk</div>
        <div class="metric-value" style="color:#d97706">{at_risk}</div>
        <div class="metric-sub">within 1pp of SLA</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🔴 SLA Breach</div>
        <div class="metric-value" style="color:#dc2626">{breaches}</div>
        <div class="metric-sub">requires immediate action</div>
    </div>""", unsafe_allow_html=True)

st.markdown("")

# ── TABS ──────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 SLA Monitor",
    "👥 RACI Explorer",
    "🤖 Automated Checks",
    "🚨 Escalation Protocol",
    "⚖️ Decision Rights"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — SLA MONITOR
# ══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown('<div class="section-header">Data Quality SLA Monitor</div>', unsafe_allow_html=True)
    st.caption("Real-time view of completeness, accuracy, and freshness SLAs across all certified datasets.")

    # Build rows respecting sidebar filters
    for tier_label, datasets in DATASETS.items():
        if selected_tier != "All Tiers" and selected_tier != tier_label:
            continue

        tier_num = tier_label.split("—")[0].strip()
        css_cls = "tier-1-badge" if "1" in tier_num else ("tier-2-badge" if "2" in tier_num else "tier-3-badge")

        filtered = [d for d in datasets
                    if selected_domain == "All Domains" or d["domain"] == selected_domain]
        if not filtered:
            continue

        st.markdown(f'<span class="{css_cls}">{tier_label}</span>', unsafe_allow_html=True)
        st.markdown("")

        for d in filtered:
            c_status, c_cls, c_delta = sla_status(d["completeness_actual"], d["completeness_sla"])
            a_status, a_cls, a_delta = sla_status(d["accuracy_actual"], d["accuracy_sla"])
            f_status, f_cls, f_delta = sla_status(d["freshness_actual_min"], d["freshness_sla_min"], higher_is_better=False)

            with st.expander(f"**{d['dataset']}** — {d['domain']}  |  {c_status} Completeness  |  {a_status} Accuracy  |  {f_status} Freshness"):
                r1, r2, r3 = st.columns(3)

                with r1:
                    st.markdown("**Completeness**")
                    st.progress(min(d["completeness_actual"] / 100, 1.0))
                    st.markdown(f"Actual: **{d['completeness_actual']}%**")
                    st.markdown(f"SLA: {d['completeness_sla']}%")
                    st.markdown(f'<span class="{c_cls}">{c_status} ({c_delta})</span>', unsafe_allow_html=True)

                with r2:
                    st.markdown("**Accuracy**")
                    st.progress(min(d["accuracy_actual"] / 100, 1.0))
                    st.markdown(f"Actual: **{d['accuracy_actual']}%**")
                    st.markdown(f"SLA: {d['accuracy_sla']}%")
                    st.markdown(f'<span class="{a_cls}">{a_status} ({a_delta})</span>', unsafe_allow_html=True)

                with r3:
                    st.markdown("**Freshness**")
                    actual_display = freshness_display(d["freshness_actual_min"])
                    st.markdown(f"Actual: **{actual_display}**")
                    st.markdown(f"SLA: {d['freshness_sla']}")
                    st.markdown(f'<span class="{f_cls}">{f_status} ({f_delta})</span>', unsafe_allow_html=True)

                st.markdown("---")
                ic1, ic2 = st.columns(2)
                with ic1:
                    st.markdown(f"**Domain Owner:** {d['owner']}")
                    st.markdown(f"**Data Steward:** {d['steward']}")
                with ic2:
                    st.markdown(f"**Breach consequence:** {d['consequence']}")

        st.markdown("")

    # Overall health chart
    st.divider()
    st.markdown('<div class="section-header">SLA Health Overview</div>', unsafe_allow_html=True)

    chart_rows = []
    for tier_label, datasets in DATASETS.items():
        for d in datasets:
            if selected_domain != "All Domains" and d["domain"] != selected_domain:
                continue
            _, c_cls, _ = sla_status(d["completeness_actual"], d["completeness_sla"])
            _, a_cls, _ = sla_status(d["accuracy_actual"], d["accuracy_sla"])
            _, f_cls, _ = sla_status(d["freshness_actual_min"], d["freshness_sla_min"], higher_is_better=False)
            worst = "Breach" if any("breach" in x for x in [c_cls, a_cls, f_cls]) else (
                "At Risk" if any("warn" in x for x in [c_cls, a_cls, f_cls]) else "Healthy"
            )
            chart_rows.append({
                "Dataset": d["dataset"],
                "Domain": d["domain"],
                "Tier": tier_label.split("—")[0].strip(),
                "Completeness": d["completeness_actual"],
                "Accuracy": d["accuracy_actual"],
                "Status": worst
            })

    if chart_rows:
        df = pd.DataFrame(chart_rows)
        color_map = {"Healthy": "#10b981", "At Risk": "#f59e0b", "Breach": "#ef4444"}
        fig = px.bar(
            df, x="Dataset", y="Completeness",
            color="Status", color_discrete_map=color_map,
            hover_data=["Domain", "Tier", "Accuracy"],
            title="Completeness % by Dataset (colored by worst SLA status)",
            labels={"Completeness": "Completeness %"},
            height=380
        )
        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_color="#1e293b", showlegend=True,
            xaxis_tickangle=-35
        )
        fig.add_hline(y=99, line_dash="dot", line_color="#94a3b8",
                      annotation_text="99% reference", annotation_position="top right")
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — RACI EXPLORER
# ══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown('<div class="section-header">Stewardship RACI</div>', unsafe_allow_html=True)
    st.caption("Who is Accountable, Responsible, Consulted, and Informed for data quality across each role.")

    raci_df = pd.DataFrame(RACI)
    raci_df.columns = ["Role", "Accountable For", "Responsible For", "Consulted On", "Informed Of"]
    st.dataframe(raci_df, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown('<div class="section-header">Domain Data Owners by Domain</div>', unsafe_allow_html=True)

    domain_owners = [
        {"Domain": "Merchandising", "Data Owner": "VP Merchandising", "Steward": "Sr. Analyst, Merch Analytics",
         "Key Datasets": "Product MDM, Assortment, Pricing"},
        {"Domain": "Supply Chain", "Data Owner": "VP Supply Chain", "Steward": "Sr. Analyst, SC Analytics",
         "Key Datasets": "Vendor MDM, PO, Inventory"},
        {"Domain": "Store Operations", "Data Owner": "VP Store Operations", "Steward": "Sr. Analyst, Store Analytics",
         "Key Datasets": "Store MDM, POS Transactions"},
        {"Domain": "Customer & Marketing", "Data Owner": "VP Marketing", "Steward": "Sr. Analyst, CRM",
         "Key Datasets": "CDP Profiles, Loyalty, Campaigns"},
        {"Domain": "Finance", "Data Owner": "VP Finance", "Steward": "Sr. Financial Analyst",
         "Key Datasets": "P&L, Margin, Cost"},
    ]
    st.dataframe(pd.DataFrame(domain_owners), use_container_width=True, hide_index=True)

    st.divider()
    st.markdown('<div class="section-header">Governance Model: Federated + Center-Led</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Why federated?**")
        st.markdown(
            "Business domains own their data — Merchandising defines what 'correct price' means, "
            "Supply Chain defines what 'complete PO record' means. Accountability lives closest to "
            "the business impact."
        )
        st.markdown("**Why center-led?**")
        st.markdown(
            "A central Data Office sets standards, tooling, and cross-domain policy. Without this, "
            "metrics diverge across domains and a data swamp forms in the lake."
        )

    with c2:
        st.markdown("**What this avoids:**")
        failure_modes = pd.DataFrame([
            {"Failure Mode": "Fully centralized", "Risk": "Data team becomes bottleneck; business loses ownership; IT 'owns' quality"},
            {"Failure Mode": "Fully federated", "Risk": "Metrics diverge across domains; no cross-domain trust; data swamp forms"},
        ])
        st.dataframe(failure_modes, use_container_width=True, hide_index=True)

        st.markdown("**Tool stack:**")
        tools = pd.DataFrame([
            {"Tool": "Databricks Unity Catalog", "Purpose": "Governance, lineage, access control, data discovery"},
            {"Tool": "Great Expectations", "Purpose": "Automated DQ checks in pipelines"},
            {"Tool": "Jira", "Purpose": "DQ ticket tracking and SLA management"},
            {"Tool": "Confluence", "Purpose": "Data dictionary, policies, decision log"},
            {"Tool": "Power BI + Databricks", "Purpose": "Quality scorecard dashboards"},
        ])
        st.dataframe(tools, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — AUTOMATED CHECKS
# ══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown('<div class="section-header">Unity Catalog Automated DQ Checks</div>', unsafe_allow_html=True)
    st.caption("Every certified dataset runs these checks on every pipeline refresh inside Databricks Unity Catalog.")

    for chk in AUTOMATED_CHECKS:
        col_icon, col_content = st.columns([0.05, 0.95])
        with col_icon:
            st.markdown(f"### {chk['icon']}")
        with col_content:
            st.markdown(f"**{chk['check']}**")
            st.markdown(chk["description"])
        st.divider()

    st.markdown('<div class="section-header">Check Coverage by Dataset</div>', unsafe_allow_html=True)
    st.caption("All Tier 1 and Tier 2 certified datasets run all 7 checks. Tier 3 runs 5 checks (excluding Format and Referential for non-operational datasets).")

    coverage_data = []
    check_names = [c["check"] for c in AUTOMATED_CHECKS]
    for tier_label, datasets in DATASETS.items():
        is_tier3 = "3" in tier_label
        for d in datasets:
            row = {"Dataset": d["dataset"], "Tier": tier_label.split("—")[0].strip()}
            for chk in check_names:
                if is_tier3 and chk in ["Referential Check", "Format Check"]:
                    row[chk] = "—"
                else:
                    row[chk] = "✅"
            coverage_data.append(row)

    coverage_df = pd.DataFrame(coverage_data)
    st.dataframe(coverage_df, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown('<div class="section-header">Sample DQ Check Output (Unity Catalog)</div>', unsafe_allow_html=True)
    st.code("""
# Great Expectations pipeline check — Product MDM (Silver → Gold)
suite = context.create_expectation_suite("product_mdm_gold_checks")

# Null checks
expect_column_values_to_not_be_null(column="sku_id")
expect_column_values_to_not_be_null(column="product_name")
expect_column_values_to_not_be_null(column="price_current")

# Range checks
expect_column_values_to_be_between(column="price_current", min_value=0.01, max_value=500.00)
expect_column_values_to_be_between(column="margin_pct", min_value=-0.50, max_value=0.95)

# Referential check — every active SKU must have a category
expect_column_pair_values_A_to_be_greater_than_B(
    column_A="sku_count_with_category",
    column_B="sku_count_active"
)

# Volume check — alert if record count drops >10%
expect_table_row_count_to_be_between(
    min_value=int(last_7day_avg * 0.90),
    max_value=int(last_7day_avg * 1.20)
)

# Freshness check
expect_column_max_to_be_between(
    column="updated_at",
    min_value=datetime.now() - timedelta(minutes=5)  # Tier 1 SLA
)
""", language="python")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — ESCALATION PROTOCOL
# ══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown('<div class="section-header">4-Level Escalation Protocol</div>', unsafe_allow_html=True)
    st.caption("Automated alerts escalate through four levels based on breach severity and duration.")

    levels = [
        ("Level 1", "escalation-l1", "⏱️ 0–1 hour",
         "Automated alert → Data Custodian (pipeline fix within 1 hour)",
         "Any dataset: pipeline failure detected by automated check",
         "Data Custodian investigates and resolves pipeline issue within 1 hour. No ticket required if resolved."),
        ("Level 2", "escalation-l2", "⏱️ 2+ hours",
         "SLA breach >2 hours → Data Steward notified, incident ticket opened in Jira",
         "Any dataset: SLA breach persists beyond 2 hours without resolution",
         "Data Steward opens P1 Jira ticket, notifies Data Custodian, and begins root cause investigation."),
        ("Level 3", "escalation-l3", "⏱️ 4+ hours (Tier 1 only)",
         "SLA breach >4 hours (Tier 1 data) → Domain Data Owner notified, P0 incident",
         "Tier 1 dataset: pricing, inventory, or availability data breached for 4+ hours",
         "Domain Data Owner (VP-level) is notified. P0 incident declared. Engineering lead joins. Business impact assessment begins."),
        ("Level 4", "escalation-l4", "⏱️ Business impact confirmed",
         "Business impact confirmed → CDO notified, cross-functional war room",
         "Any tier: confirmed downstream business impact (pricing errors in POS, wrong allocation executed, etc.)",
         "CDO convenes cross-functional war room. Rollback or mitigation plan activated within 2 hours. Post-mortem scheduled within 5 business days."),
    ]

    for level, css, timing, trigger_short, trigger_detail, response in levels:
        st.markdown(f"""
        <div class="{css}">
            <strong>{level}</strong> &nbsp;·&nbsp; {timing}<br>
            <span style="font-size:14px">{trigger_short}</span>
        </div>""", unsafe_allow_html=True)
        with st.expander(f"Details — {level}"):
            st.markdown(f"**Trigger condition:** {trigger_detail}")
            st.markdown(f"**Response:** {response}")

    st.divider()
    st.markdown('<div class="section-header">Active Incident Tracker</div>', unsafe_allow_html=True)

    incidents = [
        {"ID": "DQ-1042", "Dataset": "Store Inventory Levels", "Tier": "Tier 1", "Breach Type": "Freshness",
         "Opened": "Today 08:14", "Level": "Level 2", "Status": "🔴 Open", "Owner": "Sr. Analyst, Store Analytics"},
        {"ID": "DQ-1041", "Dataset": "Customer Unified Profiles (CDP)", "Tier": "Tier 2", "Breach Type": "Freshness",
         "Opened": "Today 06:30", "Level": "Level 1", "Status": "🟡 Investigating", "Owner": "Sr. Analyst, CRM"},
        {"ID": "DQ-1038", "Dataset": "Product MDM (full attributes)", "Tier": "Tier 2", "Breach Type": "Completeness",
         "Opened": "Yesterday 22:10", "Level": "Level 1", "Status": "✅ Resolved", "Owner": "Sr. Analyst, Merch Analytics"},
    ]

    st.dataframe(pd.DataFrame(incidents), use_container_width=True, hide_index=True)

    st.markdown(
        "**Note:** DQ-1042 (Store Inventory Levels freshness breach) is the current active P1. "
        "Freshness actual is 18min vs 15min SLA. Data Custodian has been notified and is investigating "
        "the EDP Bronze pipeline latency spike."
    )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — DECISION RIGHTS
# ══════════════════════════════════════════════════════════════════════════════

with tab5:
    st.markdown('<div class="section-header">Decision Rights Framework</div>', unsafe_allow_html=True)
    st.caption("Who has authority to make which data governance decisions — reducing ambiguity and escalation overhead.")

    colors = {
        "Domain Data Owner approval required": "#dbeafe",
        "CDO / Data Office approval required": "#fef3c7",
        "Data Stewards can decide independently": "#d1fae5",
    }

    for authority, decisions in DECISION_RIGHTS.items():
        bg = colors.get(authority, "#f1f5f9")
        st.markdown(f"""
        <div style="background:{bg}; border-radius:10px; padding:14px 18px; margin-bottom:16px;">
            <strong>{authority}</strong>
        </div>""", unsafe_allow_html=True)
        for decision in decisions:
            st.markdown(f"- {decision}")
        st.markdown("")

    st.divider()
    st.markdown('<div class="section-header">Data Literacy & Enablement Program</div>', unsafe_allow_html=True)
    st.caption("Self-service analytics only works if business users trust and understand the data.")

    literacy = pd.DataFrame([
        {"Program": "Data Office Hours", "Format": "60-min virtual session", "Audience": "All business analysts", "Cadence": "2× per week"},
        {"Program": "Data Certification (Power BI)", "Format": "Self-paced + assessment", "Audience": "All business users", "Cadence": "Ongoing"},
        {"Program": "New Dataset Walkthrough", "Format": "30-min recorded demo", "Audience": "Data consumers", "Cadence": "Each new certified dataset"},
        {"Program": "Monthly DQ Scorecard", "Format": "Email report", "Audience": "All Data Owners", "Cadence": "Monthly"},
        {"Program": "Annual Governance Review", "Format": "All-hands with CDO", "Audience": "All stakeholders", "Cadence": "Annual"},
    ])
    st.dataframe(literacy, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown('<div class="section-header">DQ Score by Domain</div>', unsafe_allow_html=True)

    domain_scores = []
    for tier_label, datasets in DATASETS.items():
        for d in datasets:
            avg_score = (d["completeness_actual"] + d["accuracy_actual"]) / 2
            domain_scores.append({"Domain": d["domain"], "Score": avg_score, "Dataset": d["dataset"]})

    domain_df = pd.DataFrame(domain_scores).groupby("Domain")["Score"].mean().reset_index()
    domain_df.columns = ["Domain", "Avg DQ Score (%)"]
    domain_df = domain_df.sort_values("Avg DQ Score (%)", ascending=True)

    fig2 = px.bar(
        domain_df, x="Avg DQ Score (%)", y="Domain",
        orientation="h",
        color="Avg DQ Score (%)",
        color_continuous_scale=["#ef4444", "#f59e0b", "#10b981"],
        range_color=[95, 100],
        title="Average Data Quality Score by Domain (Completeness + Accuracy avg)",
        height=300,
    )
    fig2.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font_color="#1e293b", showlegend=False,
        coloraxis_showscale=False,
    )
    fig2.add_vline(x=99, line_dash="dot", line_color="#94a3b8",
                   annotation_text="99% target", annotation_position="top right")
    st.plotly_chart(fig2, use_container_width=True)
