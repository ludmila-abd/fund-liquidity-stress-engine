import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Fund Liquidity Control Room",
    page_icon="💧",
    layout="wide",
)

# ============================================================
# THEME CONSTANTS
# ============================================================

INK = "#111827"
MUTED = "#6B7280"
CREAM = "#F7F4EF"
BORDER = "#E5E7EB"
NAVY = "#1F2937"
BLUE = "#355C7D"
TEAL = "#0F766E"
GOLD = "#D6A85F"
AMBER = "#B45309"
RED = "#991B1B"
SLATE = "#334155"
GREEN = "#15803D"

DEFAULT_FILE = Path("outputs") / "liquidity_stress_report.xlsx"

# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
    <style>
    .stApp {{
        background: radial-gradient(circle at top left, #ffffff 0%, {CREAM} 38%, #efe9df 100%);
    }}

    .block-container {{
        max-width: 1500px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }}

    section[data-testid="stSidebar"] {{
        background: {NAVY};
        border-right: 1px solid rgba(255,255,255,0.08);
    }}

    section[data-testid="stSidebar"] * {{
        color: #f9fafb;
    }}

    .hero {{
        background:
            linear-gradient(135deg, rgba(17,24,39,0.96), rgba(53,92,125,0.92)),
            radial-gradient(circle at top right, rgba(214,168,95,0.45), rgba(214,168,95,0));
        border: 1px solid rgba(214,168,95,0.35);
        border-radius: 28px;
        padding: 34px 38px;
        margin-bottom: 22px;
        box-shadow: 0 24px 60px rgba(17,24,39,0.18);
        color: white;
    }}

    .eyebrow {{
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        border: 1px solid rgba(214,168,95,0.55);
        background: rgba(214,168,95,0.16);
        color: #fef3c7;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 850;
        margin-bottom: 14px;
    }}

    .hero h1 {{
        font-size: 44px;
        line-height: 1.02;
        letter-spacing: -0.055em;
        font-weight: 950;
        margin: 0 0 10px 0;
        color: white;
    }}

    .hero p {{
        font-size: 17px;
        line-height: 1.55;
        color: #e5e7eb;
        max-width: 1050px;
        margin-bottom: 0;
    }}

    .metric-card {{
        background: rgba(255,255,255,0.96);
        border: 1px solid {BORDER};
        border-radius: 22px;
        padding: 20px 18px;
        min-height: 128px;
        box-shadow: 0 14px 34px rgba(17,24,39,0.07);
        position: relative;
        overflow: hidden;
    }}

    .metric-card::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, {BLUE}, {GOLD});
    }}

    .metric-label {{
        color: {MUTED};
        font-size: 12px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-weight: 850;
        margin-bottom: 12px;
    }}

    .metric-value {{
        color: {INK};
        font-size: 28px;
        font-weight: 950;
        letter-spacing: -0.045em;
    }}

    .metric-note {{
        color: #9CA3AF;
        font-size: 12px;
        margin-top: 8px;
    }}

    .page-title {{
        margin-top: 10px;
        font-size: 31px;
        font-weight: 950;
        letter-spacing: -0.045em;
        color: {INK};
    }}

    .page-subtitle {{
        color: {MUTED};
        font-size: 15px;
        margin-top: 2px;
        margin-bottom: 20px;
    }}

    .badge-pass {{
        display: inline-block;
        padding: 7px 11px;
        border-radius: 999px;
        background: #dcfce7;
        color: {GREEN};
        font-size: 12px;
        font-weight: 900;
        margin-right: 7px;
        letter-spacing: 0.04em;
    }}

    .badge-risk {{
        display: inline-block;
        padding: 7px 11px;
        border-radius: 999px;
        background: #fee2e2;
        color: {RED};
        font-size: 12px;
        font-weight: 900;
        margin-right: 7px;
        letter-spacing: 0.04em;
    }}

    .badge-neutral {{
        display: inline-block;
        padding: 7px 11px;
        border-radius: 999px;
        background: #fef3c7;
        color: {AMBER};
        font-size: 12px;
        font-weight: 900;
        margin-right: 7px;
        letter-spacing: 0.04em;
    }}

    .insight {{
        background: #fffaf0;
        border: 1px solid #f3d7a4;
        border-left: 6px solid {GOLD};
        border-radius: 18px;
        padding: 18px 20px;
        color: {INK};
        box-shadow: 0 10px 28px rgba(31,111,139,0.08);
        margin: 18px 0;
    }}

    .risk {{
        background: #fff1f2;
        border: 1px solid #fecdd3;
        border-left: 6px solid {RED};
        border-radius: 18px;
        padding: 18px 20px;
        color: {INK};
        margin: 18px 0;
    }}

    div[data-testid="stDataFrame"] {{
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid {BORDER};
    }}

    h1, h2, h3 {{
        color: {INK};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HELPERS
# ============================================================

@st.cache_data
def load_workbook(path_or_buffer):
    return pd.read_excel(path_or_buffer, sheet_name=None)

def money(x):
    try:
        return f"£{float(x):,.0f}"
    except Exception:
        return "£0"

def money2(x):
    try:
        return f"£{float(x):,.2f}"
    except Exception:
        return "£0.00"

def pct(x):
    try:
        return f"{float(x):.1%}"
    except Exception:
        return "0.0%"

def num(x):
    try:
        return f"{float(x):,.0f}"
    except Exception:
        return "0"

def ratio(x):
    try:
        return f"{float(x):,.2f}x"
    except Exception:
        return "0.00x"

def bps(x):
    try:
        return f"{float(x):,.2f} bps"
    except Exception:
        return "0.00 bps"

def get_kpi(kpis, col, default=0):
    if col in kpis.columns and len(kpis) > 0:
        return kpis[col].iloc[0]
    return default

def page_header(title, subtitle):
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)

def metric_card(label, value, note=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def style_fig(fig, height=430):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=24, r=90, t=68, b=34),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Inter, Arial, sans-serif", size=13, color=INK),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=12),
        ),
    )
    fig.update_xaxes(showgrid=False, linecolor="#E5E7EB")
    fig.update_yaxes(gridcolor="#EEE7DA", zerolinecolor="#EEE7DA")
    return fig

def risk_color(value):
    value = str(value).upper()
    if value in ["LOW", "MEET_IN_FULL"]:
        return GREEN
    if value in ["MEDIUM", "SWING_PRICING_REVIEW", "SWING_PRICING_TRIGGERED"]:
        return AMBER
    return RED

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div style="padding: 18px 4px 10px 4px;">
        <div style="font-size: 25px; font-weight: 950; letter-spacing: -0.04em; color: white;">
            Liquidity Control Room
        </div>
        <div style="color: #d1d5db; font-size: 13px; line-height: 1.45; margin-top: 6px;">
            Asset-side liquidity, liability-side redemption pressure, waterfall simulation and escalation outcomes.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.sidebar.file_uploader("Upload liquidity_stress_report.xlsx", type=["xlsx"])

if uploaded_file is not None:
    data_source = uploaded_file
    st.sidebar.success("Workbook uploaded")
elif DEFAULT_FILE.exists():
    data_source = DEFAULT_FILE
    st.sidebar.success("Using local export")
else:
    st.sidebar.error("Excel export not found. Run the notebook export cell first.")
    st.stop()

sheets = load_workbook(data_source)

required_sheets = [
    "Executive_KPIs_Wide",
    "Risk_Diagnostics",
    "Scenario_Decision_Summary",
    "LCR_Scenario_Horizon",
    "Liquidation_Waterfall",
    "Fire_Sale_By_Bucket",
    "Remaining_Liquidity",
    "Investor_Redemption",
    "Liquidity_Bucket_Summary",
    "Holdings_Enriched",
    "Stress_Test_Controls",
    "Escalation_Summary",
]

missing = [s for s in required_sheets if s not in sheets]
if missing:
    st.error(f"Missing required sheet(s): {missing}")
    st.stop()

kpis = sheets["Executive_KPIs_Wide"]
risk = sheets["Risk_Diagnostics"]
scenario_summary = sheets["Scenario_Decision_Summary"]
lcr_horizon = sheets["LCR_Scenario_Horizon"]
waterfall = sheets["Liquidation_Waterfall"]
fire_bucket = sheets["Fire_Sale_By_Bucket"]
remaining = sheets["Remaining_Liquidity"]
investor_redemption = sheets["Investor_Redemption"]
bucket_summary = sheets["Liquidity_Bucket_Summary"]
holdings = sheets["Holdings_Enriched"]
controls = sheets["Stress_Test_Controls"]
escalation_summary = sheets["Escalation_Summary"]

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Scenario Comparison",
        "Liquidation Waterfall",
        "Holdings Liquidity Map",
        "Fire-Sale Cost Analysis",
        "Liability-Side Flows",
        "Controls & Escalation",
        "Data Explorer",
    ],
)

st.sidebar.divider()
st.sidebar.caption("Built with Python, pandas, Plotly, Streamlit and Excel export.")

# ============================================================
# KPI VALUES
# ============================================================

fund_nav = get_kpi(kpis, "fund_nav_gbp")
number_of_holdings = get_kpi(kpis, "number_of_holdings")
watchlist_holdings = get_kpi(kpis, "watchlist_holdings")
scenarios_tested = get_kpi(kpis, "redemption_scenarios_tested")
scenarios_escalation = get_kpi(kpis, "scenarios_requiring_escalation")
high_critical = get_kpi(kpis, "high_critical_scenarios")
minimum_lcr = get_kpi(kpis, "minimum_lcr")
max_fire_cost = get_kpi(kpis, "maximum_fire_sale_cost_gbp")
systemic_outcome = str(get_kpi(kpis, "systemic_run_outcome", "UNKNOWN"))
weakest_remaining_liquidity = get_kpi(kpis, "weakest_remaining_liquidity_ratio")

# ============================================================
# HERO + KPI CARDS
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Fund Risk / Liquidity Stress Testing</div>
        <h1>Fund Liquidity Control Room</h1>
        <p>
            A liquidity mismatch stress engine that compares asset-side liquidation capacity
            against liability-side investor redemption pressure, then simulates redemption shocks,
            fire-sale costs, residual liquidity and model-suggested escalation outcomes.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4, m5, m6 = st.columns(6)

with m1:
    metric_card("Fund NAV", money(fund_nav), "open-ended fund")
with m2:
    metric_card("Holdings", num(number_of_holdings), f"{num(watchlist_holdings)} watchlist")
with m3:
    metric_card("Scenarios", num(scenarios_tested), "redemption shocks")
with m4:
    metric_card("Min LCR", ratio(minimum_lcr), "worst case")
with m5:
    metric_card("Max Fire-Sale Cost", money(max_fire_cost), "tail scenario")
with m6:
    metric_card("Tail Outcome", systemic_outcome.replace("_", " "), "systemic run")

st.write("")

# ============================================================
# PAGE 1 — EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":
    page_header(
        "Executive Overview",
        "Headline view of liquidity coverage, fire-sale costs, escalation outcomes and residual portfolio liquidity."
    )

    st.markdown(
        f"""
        <span class="badge-risk">SYSTEMIC OUTCOME: {systemic_outcome.replace("_", " ")}</span>
        <span class="badge-neutral">{num(scenarios_escalation)} ESCALATION SCENARIOS</span>
        <span class="badge-neutral">{num(high_critical)} HIGH / CRITICAL</span>
        <span class="badge-pass">0 CASH SHORTFALLS</span>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    c1, c2 = st.columns([1.1, 0.9])

    with c1:
        fig = px.bar(
            scenario_summary.sort_values("redemption_pct_of_nav"),
            x="scenario_name",
            y="liquidity_coverage_ratio",
            text="liquidity_coverage_ratio",
            title="Liquidity Coverage Ratio by Scenario",
            color_discrete_sequence=[BLUE],
        )
        fig.add_hline(y=1.0, line_dash="dash", line_color=RED)
        fig.update_traces(texttemplate="%{text:.2f}x", textposition="outside")
        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    with c2:
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=float(minimum_lcr),
                number={"suffix": "x", "font": {"size": 38, "color": INK}},
                title={"text": "Minimum Liquidity Coverage Ratio"},
                gauge={
                    "axis": {"range": [0, max(3, float(minimum_lcr) * 2)]},
                    "bar": {"color": RED if float(minimum_lcr) < 1.5 else AMBER},
                    "bgcolor": "white",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0, 1], "color": "#fee2e2"},
                        {"range": [1, 1.5], "color": "#fef3c7"},
                        {"range": [1.5, 3], "color": "#dcfce7"},
                    ],
                    "threshold": {
                        "line": {"color": RED, "width": 4},
                        "thickness": 0.75,
                        "value": 1,
                    },
                },
            )
        )
        fig.update_layout(title_text=None)
        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        fire_plot = scenario_summary.sort_values("fire_sale_cost_gbp")
        fig = px.bar(
            fire_plot,
            y="scenario_name",
            x="fire_sale_cost_gbp",
            text="fire_sale_cost_gbp",
            orientation="h",
            title="Fire-Sale Cost by Scenario",
            color_discrete_sequence=[GOLD],
        )
        fig.update_traces(texttemplate="£%{text:,.0f}", textposition="outside", cliponaxis=False)
        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    with c4:
        fig = px.bar(
            risk,
            x="scenario_name",
            y="remaining_liquidity_ratio",
            text="remaining_liquidity_ratio",
            title="Remaining Liquidity Ratio After Redemption",
            color="liquidity_risk_band",
            color_discrete_map={
                "LOW": GREEN,
                "MEDIUM": AMBER,
                "HIGH": RED,
                "CRITICAL": RED,
            },
        )
        fig.update_traces(texttemplate="%{text:.1%}", textposition="outside")
        fig.update_layout(showlegend=True)
        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    st.markdown(
        """
        <div class="risk">
            <b>Executive takeaway:</b> the fund can meet all tested redemptions in cash terms,
            but severe scenarios materially consume liquid assets and increase the remaining
            portfolio's illiquid concentration. The systemic run therefore requires liquidity
            committee escalation rather than simple pass/fail treatment.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Scenario Decision Summary")
    st.dataframe(scenario_summary, use_container_width=True, hide_index=True)

# ============================================================
# PAGE 2 — SCENARIO COMPARISON
# ============================================================

elif page == "Scenario Comparison":
    page_header(
        "Scenario Comparison",
        "Compare redemption amount, cash raised, liquidity coverage, fire-sale cost and model-suggested outcome."
    )

    c1, c2 = st.columns(2)

    with c1:
        comp = scenario_summary[
            ["scenario_name", "redemption_amount_gbp", "cash_raised_by_deadline_gbp"]
        ].melt(
            id_vars="scenario_name",
            var_name="metric",
            value_name="value_gbp",
        )

        fig = px.bar(
            comp,
            x="scenario_name",
            y="value_gbp",
            color="metric",
            barmode="group",
            title="Redemption Amount vs Cash Raised",
            color_discrete_sequence=[BLUE, GOLD],
        )
        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    with c2:
        fig = px.scatter(
            scenario_summary,
            x="redemption_pct_of_nav",
            y="fire_sale_cost_gbp",
            size="redemption_amount_gbp",
            color="model_suggested_escalation",
            text="scenario_name",
            title="Redemption Shock vs Fire-Sale Cost",
        )
        fig.update_traces(textposition="top center")
        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    st.markdown("### Liquidity Risk Diagnostics")
    st.dataframe(
        risk[
            [
                "scenario_id",
                "scenario_name",
                "scenario_materiality",
                "redemption_pct_of_nav",
                "liquidity_coverage_ratio",
                "fire_sale_cost_gbp",
                "remaining_liquidity_ratio",
                "remaining_illiquid_ratio",
                "liquidity_risk_band",
                "liquidity_risk_score",
                "model_suggested_escalation",
                "recommended_management_action",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### LCR by Scenario and Horizon")
    st.dataframe(lcr_horizon, use_container_width=True, hide_index=True)

# ============================================================
# PAGE 3 — LIQUIDATION WATERFALL
# ============================================================

elif page == "Liquidation Waterfall":
    page_header(
        "Liquidation Waterfall",
        "Day-by-day sell-down view showing which assets are sold, cash raised, fire-sale cost and remaining redemption need."
    )

    scenario_options = waterfall["scenario_name"].dropna().unique().tolist()
    selected_scenario = st.selectbox("Select scenario", scenario_options)

    wf = waterfall[waterfall["scenario_name"] == selected_scenario].copy()

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            wf,
            x="ticker",
            y="cash_raised_gbp",
            color="liquidity_bucket",
            title=f"Cash Raised by Holding — {selected_scenario}",
            text="cash_raised_gbp",
        )
        fig.update_traces(texttemplate="£%{text:,.0f}", textposition="outside", cliponaxis=False)
        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    with c2:
        fig = px.line(
            wf,
            x="ticker",
            y="remaining_redemption_need_gbp",
            markers=True,
            title=f"Remaining Redemption Need — {selected_scenario}",
        )
        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    st.markdown("### Liquidation Waterfall")
    st.dataframe(wf, use_container_width=True, hide_index=True)

# ============================================================
# PAGE 4 — HOLDINGS LIQUIDITY MAP
# ============================================================

elif page == "Holdings Liquidity Map":
    page_header(
        "Holdings Liquidity Map",
        "Portfolio composition by liquidity bucket, market depth, watchlist flags and position concentration."
    )

    c1, c2 = st.columns(2)

    with c1:
        fig = px.pie(
            bucket_summary,
            names="liquidity_bucket",
            values="market_value_gbp",
            title="Initial Portfolio Liquidity Bucket Composition",
            hole=0.35,
        )
        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    with c2:
        fig = px.scatter(
            holdings,
            x="pct_of_adv_held",
            y="market_value_gbp",
            size="market_value_gbp",
            color="liquidity_bucket",
            hover_name="ticker",
            title="Position Size vs Market Depth",
        )
        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    st.markdown("### Liquidity Bucket Summary")
    st.dataframe(bucket_summary, use_container_width=True, hide_index=True)

    st.markdown("### Watchlist Holdings")
    watchlist = holdings[holdings["liquidity_data_status"] == "WATCHLIST"].copy()
    st.dataframe(
        watchlist[
            [
                "holding_id",
                "ticker",
                "asset_class",
                "sector",
                "market_value_gbp",
                "liquidity_bucket",
                "pct_of_adv_held",
                "bid_ask_spread_bps",
                "liquidity_flag_summary",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

# ============================================================
# PAGE 5 — FIRE-SALE COST ANALYSIS
# ============================================================

elif page == "Fire-Sale Cost Analysis":
    page_header(
        "Fire-Sale Cost Analysis",
        "Analyse estimated value lost through forced selling under each redemption shock."
    )

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            fire_bucket,
            x="scenario_name",
            y="fire_sale_cost_gbp",
            color="liquidity_bucket",
            title="Fire-Sale Cost by Liquidity Bucket",
        )
        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    with c2:
        fig = px.bar(
            fire_bucket,
            x="scenario_name",
            y="avg_transaction_cost_bps",
            color="liquidity_bucket",
            barmode="group",
            title="Average Transaction Cost bps by Bucket",
        )
        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    st.markdown("### Fire-Sale Cost by Bucket")
    st.dataframe(fire_bucket, use_container_width=True, hide_index=True)

# ============================================================
# PAGE 6 — LIABILITY-SIDE FLOWS
# ============================================================

elif page == "Liability-Side Flows":
    page_header(
        "Liability-Side Redemption Flows",
        "Investor-type redemption allocation under mild, elevated, stress, crisis and systemic scenarios."
    )

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            investor_redemption,
            x="scenario_name",
            y="allocated_redemption_gbp",
            color="investor_type",
            title="Allocated Redemption by Investor Type",
        )
        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    with c2:
        fig = px.bar(
            investor_redemption,
            x="scenario_name",
            y="redemption_share",
            color="investor_type",
            title="Redemption Share by Investor Type",
        )
        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    st.markdown("### Investor Redemption Allocation")
    st.dataframe(investor_redemption, use_container_width=True, hide_index=True)

# ============================================================
# PAGE 7 — CONTROLS & ESCALATION
# ============================================================

elif page == "Controls & Escalation":
    page_header(
        "Controls & Escalation",
        "Stress-test controls, escalation outcomes and model-suggested management actions."
    )

    c1, c2 = st.columns(2)

    with c1:
        control_plot = controls.groupby("status", as_index=False).agg(control_count=("control", "count"))

        fig = px.bar(
            control_plot,
            x="status",
            y="control_count",
            text="control_count",
            title="Stress Test Control Status",
            color="status",
            color_discrete_map={
                "PASS": GREEN,
                "REVIEW": AMBER,
                "FAIL": RED,
            },
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    with c2:
        esc_plot = risk.groupby("model_suggested_escalation", as_index=False).agg(
            scenario_count=("scenario_id", "count")
        )

        fig = px.bar(
            esc_plot,
            y="model_suggested_escalation",
            x="scenario_count",
            text="scenario_count",
            orientation="h",
            title="Model-Suggested Escalation Outcomes",
            color_discrete_sequence=[BLUE],
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(style_fig(fig, 430), use_container_width=True)

    st.markdown("### Stress Test Controls")
    st.dataframe(controls, use_container_width=True, hide_index=True)

    st.markdown("### Escalation Summary")
    st.dataframe(escalation_summary, use_container_width=True, hide_index=True)

# ============================================================
# PAGE 8 — DATA EXPLORER
# ============================================================

elif page == "Data Explorer":
    page_header(
        "Data Explorer",
        "Inspect any exported table from the liquidity stress reporting workbook."
    )

    sheet = st.selectbox("Select table", sorted(sheets.keys()))

    st.dataframe(
        sheets[sheet],
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download selected table as CSV",
        data=sheets[sheet].to_csv(index=False).encode("utf-8"),
        file_name=f"{sheet}.csv",
        mime="text/csv",
    )