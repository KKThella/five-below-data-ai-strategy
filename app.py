import streamlit as st

st.set_page_config(
    page_title="Five Below — Data & AI Strategy",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
/* Hide Streamlit's auto-generated file-based nav */
[data-testid="stSidebarNav"] { display: none !important; }

/* Sidebar branding */
[data-testid="stSidebar"] { background: #0f172a; }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] hr { border-color: #1e293b !important; }
[data-testid="stSidebar"] a { color: #93c5fd !important; }
.sidebar-brand { font-size:20px; font-weight:800; color:#ffffff !important;
                 letter-spacing:-0.5px; margin-bottom:2px; }
.sidebar-sub   { font-size:11px; color:#64748b !important; text-transform:uppercase;
                 letter-spacing:0.08em; margin-bottom:16px; }
.nav-label     { font-size:10px; font-weight:700; color:#475569 !important;
                 text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px; }

/* Main content */
.hero-title   { font-size:42px; font-weight:800; color:#1e293b; line-height:1.15; margin-bottom:8px; }
.hero-sub     { font-size:18px; color:#475569; margin-bottom:32px; }
.year-card    { background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:20px 24px; height:100%; }
.year-label   { font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#94a3b8; margin-bottom:6px; }
.year-title   { font-size:18px; font-weight:700; color:#1e293b; margin-bottom:8px; }
.year-body    { font-size:13px; color:#475569; line-height:1.6; }
.tool-card    { background:white; border:1.5px solid #e2e8f0; border-radius:14px; padding:24px 28px;
                transition:border-color 0.2s; cursor:pointer; }
.tool-card:hover { border-color:#3b82f6; }
.tool-icon    { font-size:32px; margin-bottom:10px; }
.tool-title   { font-size:17px; font-weight:700; color:#1e293b; margin-bottom:6px; }
.tool-desc    { font-size:13px; color:#64748b; line-height:1.5; margin-bottom:12px; }
.tool-tag     { display:inline-block; background:#dbeafe; color:#1e40af; font-size:11px;
                font-weight:600; padding:2px 9px; border-radius:8px; margin-right:4px; margin-bottom:4px; }
.roi-box      { background:linear-gradient(135deg,#1e3a5f 0%,#1e40af 100%);
                border-radius:14px; padding:28px 32px; color:white; }
.roi-num      { font-size:36px; font-weight:800; }
.roi-label    { font-size:13px; opacity:0.8; margin-top:2px; }
.divider-line { border:none; border-top:1px solid #e2e8f0; margin:32px 0; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">🛒 Five Below</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Data &amp; AI Strategy</div>', unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="nav-label">Tools</div>', unsafe_allow_html=True)
    st.page_link("app.py",                                  label="🏠  Home & Strategy Overview")
    st.page_link("pages/1_🤖_AI_Prioritization.py",        label="🤖  AI Use Case Prioritization")
    st.page_link("pages/2_🏛️_Data_Quality_Dashboard.py",   label="🏛️  Data Quality Dashboard")
    st.page_link("pages/3_🛍️_UCP_Scorecard.py",            label="🛍️  UCP Readiness Scorecard")
    st.divider()
    st.markdown('<div class="nav-label">About</div>', unsafe_allow_html=True)
    st.markdown("**Kiran Thella**  \nAI Product Manager  \n13+ yrs · Nike · Gilead · eBay")
    st.markdown("")
    st.markdown("[🔗 LinkedIn](https://www.linkedin.com/in/kiranthella/)   [💻 GitHub](https://github.com/KKThella)")

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Five Below — Data & AI Strategy</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">A 3-year product strategy for transforming Five Below\'s data infrastructure '
    'into an enterprise AI platform — and positioning the brand to win in the emerging era of agentic commerce.</div>',
    unsafe_allow_html=True
)

# ── ROI STRIP ─────────────────────────────────────────────────────────────────
r1, r2, r3, r4 = st.columns(4)
metrics = [
    ("$92–111M", "Projected Year 3 annual value"),
    ("4–5×",     "ROI on $22–28M platform investment"),
    ("$33–52M",  "UCP agentic commerce opportunity"),
    ("3 Years",  "Foundation → AI → Agentic Commerce"),
]
for col, (val, label) in zip([r1, r2, r3, r4], metrics):
    with col:
        st.markdown(f"""
        <div class="roi-box">
            <div class="roi-num">{val}</div>
            <div class="roi-label">{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('<hr class="divider-line">', unsafe_allow_html=True)

# ── 3-YEAR ROADMAP ────────────────────────────────────────────────────────────
st.markdown("### 3-Year Strategic Roadmap")
st.caption("Three phases, each building on the last — no phase can be skipped.")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div class="year-card">
        <div class="year-label">Year 1</div>
        <div class="year-title">🏗️ Trust the Data</div>
        <div class="year-body">
            Build the data foundation — one version of truth for product, store, vendor, and customer data.
            <br><br>
            <strong>Key deliverables:</strong><br>
            · Databricks Lakehouse (Bronze → Gold)<br>
            · Profisee MDM for Product + Store + Vendor<br>
            · Unity Catalog governance + RBAC<br>
            · Real-time POS feed (&lt;15 min latency)<br>
            <br>
            <strong>Investment:</strong> ~$3.5–4.1M<br>
            <strong>Target:</strong> 99.5% product data accuracy
        </div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="year-card">
        <div class="year-label">Year 2</div>
        <div class="year-title">🧠 Know the Customer</div>
        <div class="year-body">
            Unify the customer — one profile across POS, e-commerce, loyalty, and email.
            <br><br>
            <strong>Key deliverables:</strong><br>
            · Customer Data Platform (CDP)<br>
            · 5 AI-ready customer segments<br>
            · Power BI + Databricks semantic layer<br>
            · Self-service analytics for all domains<br>
            <br>
            <strong>Investment:</strong> ~$4.2–5.1M<br>
            <strong>Target:</strong> 90% customer match rate
        </div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="year-card">
        <div class="year-label">Year 3</div>
        <div class="year-title">🚀 Win in Agentic Commerce</div>
        <div class="year-body">
            Ship AI use cases + expose catalog to Google AI Mode and Gemini shopping agents via UCP.
            <br><br>
            <strong>Key deliverables:</strong><br>
            · LLM Store Associate Agent ($6M impact)<br>
            · Markdown Optimization ML ($18M impact)<br>
            · Demand Sensing + Churn Prediction<br>
            · UCP endpoint suite (FastAPI on EDP)<br>
            <br>
            <strong>Investment:</strong> ~$14–19M total (3yr)<br>
            <strong>Target:</strong> $92–111M annual value
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="divider-line">', unsafe_allow_html=True)

# ── TOOLS ─────────────────────────────────────────────────────────────────────
st.markdown("### Interactive Tools")
st.caption("Use the sidebar or click below to explore each tool.")

t1, t2, t3 = st.columns(3)

with t1:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">🤖</div>
        <div class="tool-title">AI Use Case Prioritization Framework</div>
        <div class="tool-desc">
            Score and rank 11 retail AI use cases across Impact, Data Readiness,
            Feasibility, and Speed to Value. Interactive 2×2 priority matrix,
            value hypothesis generator, and A/B test templates.
        </div>
        <span class="tool-tag">11 Use Cases</span>
        <span class="tool-tag">Tier 1/2/3</span>
        <span class="tool-tag">A/B Test Builder</span>
    </div>""", unsafe_allow_html=True)
    st.page_link("pages/1_🤖_AI_Prioritization.py", label="→ Open AI Prioritization")

with t2:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">🏛️</div>
        <div class="tool-title">Data Quality Governance Dashboard</div>
        <div class="tool-desc">
            Operational SLA monitor for 9 certified datasets across Tier 1/2/3.
            Full stewardship RACI, 7-check automated pipeline suite,
            4-level escalation tracker, and decision rights framework.
        </div>
        <span class="tool-tag">SLA Monitor</span>
        <span class="tool-tag">RACI Explorer</span>
        <span class="tool-tag">Escalation Protocol</span>
    </div>""", unsafe_allow_html=True)
    st.page_link("pages/2_🏛️_Data_Quality_Dashboard.py", label="→ Open DQ Dashboard")

with t3:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">🛍️</div>
        <div class="tool-title">UCP Readiness Scorecard</div>
        <div class="tool-desc">
            Assess readiness for Google's Universal Commerce Protocol.
            Live scoring across catalog quality, feed freshness, and 7 API endpoints.
            Revenue waterfall model, competitive benchmarking, and remediation roadmap.
        </div>
        <span class="tool-tag">Live Scoring</span>
        <span class="tool-tag">Revenue Model</span>
        <span class="tool-tag">Competitive Analysis</span>
    </div>""", unsafe_allow_html=True)
    st.page_link("pages/3_🛍️_UCP_Scorecard.py", label="→ Open UCP Scorecard")

st.markdown('<hr class="divider-line">', unsafe_allow_html=True)

# ── WHAT IS UCP ───────────────────────────────────────────────────────────────
st.markdown("### Why UCP Is the Defining Bet for Five Below")
col_a, col_b = st.columns([3, 2])
with col_a:
    st.markdown("""
Google's **Universal Commerce Protocol** (launched January 2026) enables AI shopping agents to
discover, evaluate, and purchase products through conversational interfaces — without the shopper
ever visiting a website.

A customer asking Gemini *"find me fun gifts under \\$10 for a 7-year-old"* will surface products
from UCP-compliant merchants. Five Below is **exactly** the retailer AI agents should recommend
for value-driven, trend-right shopping — but only if the catalog is clean, real-time, and UCP-compliant.

**Walmart and Target are already live.** Dollar Tree and Dollar General have not started.
This is Five Below's window to leapfrog direct competitors in an entirely new commerce channel
that requires zero paid media spend.
    """)
with col_b:
    st.markdown("""
    | Retailer | UCP Status |
    |----------|-----------|
    | Walmart  | ✅ Live (founding partner) |
    | Target   | ✅ Live (founding partner) |
    | Five Below | 🔴 Not started |
    | Dollar Tree | 🔴 Not started |
    | Dollar General | 🟡 Evaluating |
    """)
    st.info("**Five Below's window:** Dollar Tree and Dollar General haven't started. First-mover advantage in value retail is still available.")

st.markdown("")
st.caption("Use the sidebar to navigate to any tool. All tools are interactive — adjust inputs and see results update in real time.")
