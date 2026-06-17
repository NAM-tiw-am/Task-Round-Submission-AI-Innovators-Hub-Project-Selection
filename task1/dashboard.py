import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bank Marketing Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130 0%, #2a2f45 100%);
        border: 1px solid #3d4266;
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #7c9ef8; }
    .metric-label { font-size: 0.85rem; color: #8b92a8; margin-top: 4px; }
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #c9d1f5;
        border-left: 3px solid #7c9ef8;
        padding-left: 10px;
        margin-bottom: 12px;
    }
    div[data-testid="stSidebar"] { background-color: #161925; }
    h1, h2, h3 { color: #e0e4f8 !important; }
</style>
""", unsafe_allow_html=True)

COLORS = {
    "yes": "#4caf84",
    "no": "#e05c6a",
    "primary": "#7c9ef8",
    "secondary": "#b07cf8",
    "accent": "#f8c37c",
    "bg": "#1e2130",
    "grid": "#2a2f45",
}

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#c9d1f5", size=12),
    margin=dict(l=10, r=10, t=40, b=10),
)

# ── Data loader ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    sep = ";" if path.endswith(".csv") else ","
    try:
        df = pd.read_csv(path, sep=sep)
    except Exception:
        df = pd.read_csv(path, sep=",")

    # Normalise column names
    df.columns = [c.strip().lower().replace('"', '') for c in df.columns]
    if "y" in df.columns:
        df["subscribed"] = df["y"].str.strip().str.replace('"', '')
    elif "subscribed" not in df.columns:
        df["subscribed"] = "no"

    # Clean string columns
    str_cols = df.select_dtypes("object").columns
    for c in str_cols:
        df[c] = df[c].str.strip().str.replace('"', '')

    return df

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🏦 Bank Marketing")
    st.caption("Term Deposit Campaign Analysis")

    # File upload
    uploaded = st.file_uploader("Upload bank-full.csv", type=["csv"])

    if uploaded:
        path = "/tmp/bank_uploaded.csv"
        with open(path, "wb") as f:
            f.write(uploaded.read())
        df_full = load_data(path)
    else:
        # Try default paths
        default_paths = [
            "/mnt/user-data/uploads/bank-full.csv",
            "bank-full.csv",
        ]
        df_full = None
        for p in default_paths:
            if os.path.exists(p):
                df_full = load_data(p)
                break

        if df_full is None:
            st.info("📂 Please upload bank-full.csv to get started.")
            st.stop()

    st.markdown("---")
    st.markdown("### 🎛️ Filters")

    # Age slider
    age_min, age_max = int(df_full["age"].min()), int(df_full["age"].max())
    age_range = st.slider("Age Range", age_min, age_max, (age_min, age_max))

    # Job filter
    jobs = sorted(df_full["job"].unique().tolist())
    sel_jobs = st.multiselect("Job Type", jobs, default=jobs)

    # Marital filter
    marital_opts = sorted(df_full["marital"].unique().tolist())
    sel_marital = st.multiselect("Marital Status", marital_opts, default=marital_opts)

    # Education filter
    edu_opts = sorted(df_full["education"].unique().tolist())
    sel_edu = st.multiselect("Education", edu_opts, default=edu_opts)

    # Month filter
    month_order = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
    avail_months = [m for m in month_order if m in df_full["month"].unique()]
    sel_months = st.multiselect("Month", avail_months, default=avail_months)

    # Balance slider
    bal_min, bal_max = int(df_full["balance"].min()), int(df_full["balance"].max())
    bal_range = st.slider("Balance Range (€)", bal_min, bal_max, (bal_min, bal_max))

    st.markdown("---")
    st.caption(f"Dataset: {len(df_full):,} records")

# ── Apply filters ─────────────────────────────────────────────────────────────
df = df_full[
    (df_full["age"] >= age_range[0]) & (df_full["age"] <= age_range[1]) &
    (df_full["job"].isin(sel_jobs)) &
    (df_full["marital"].isin(sel_marital)) &
    (df_full["education"].isin(sel_edu)) &
    (df_full["month"].isin(sel_months)) &
    (df_full["balance"] >= bal_range[0]) & (df_full["balance"] <= bal_range[1])
].copy()

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🏦 Bank Marketing — Term Deposit EDA Dashboard")
st.caption(f"Showing **{len(df):,}** of **{len(df_full):,}** records after filters")

# ── KPI row ───────────────────────────────────────────────────────────────────
total = len(df)
subscribed = (df["subscribed"] == "yes").sum()
conv_rate = subscribed / total * 100 if total else 0
avg_balance = df["balance"].mean()
avg_duration = df["duration"].mean() / 60  # minutes
avg_age = df["age"].mean()

k1, k2, k3, k4, k5 = st.columns(5)
kpi_data = [
    (k1, f"{total:,}", "Total Clients"),
    (k2, f"{subscribed:,}", "Subscribed (Yes)"),
    (k3, f"{conv_rate:.1f}%", "Conversion Rate"),
    (k4, f"€{avg_balance:,.0f}", "Avg Balance"),
    (k5, f"{avg_duration:.1f} min", "Avg Call Duration"),
]
for col, val, lbl in kpi_data:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{val}</div>
            <div class="metric-label">{lbl}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  TAB NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "👥 Demographics",
    "💰 Financial",
    "📞 Campaign",
    "🔍 Deep Dive",
])

# helper
def styled_fig(fig):
    fig.update_layout(**PLOTLY_THEME)
    fig.update_xaxes(showgrid=True, gridcolor=COLORS["grid"], zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=COLORS["grid"], zeroline=False)
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Subscription Distribution</div>', unsafe_allow_html=True)
        counts = df["subscribed"].value_counts()
        fig = go.Figure(go.Pie(
            labels=counts.index,
            values=counts.values,
            hole=0.55,
            marker_colors=[COLORS["yes"], COLORS["no"]],
            textinfo="label+percent",
            textfont_size=13,
        ))
        fig.add_annotation(text=f"<b>{conv_rate:.1f}%</b><br>Conv Rate",
                           x=0.5, y=0.5, showarrow=False,
                           font=dict(size=16, color="#e0e4f8"))
        fig.update_layout(title="Subscribed to Term Deposit", showlegend=True,
                          legend=dict(orientation="h", y=-0.1), **PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Subscription by Month</div>', unsafe_allow_html=True)
        month_df = (df.groupby(["month", "subscribed"])
                      .size().reset_index(name="count"))
        month_df["month"] = pd.Categorical(month_df["month"], categories=month_order, ordered=True)
        month_df = month_df.sort_values("month")
        fig = px.bar(month_df, x="month", y="count", color="subscribed",
                     color_discrete_map={"yes": COLORS["yes"], "no": COLORS["no"]},
                     barmode="group", title="Monthly Campaign Outcomes")
        styled_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-header">Conversion Rate by Job</div>', unsafe_allow_html=True)
        job_conv = (df.groupby("job")["subscribed"]
                      .apply(lambda x: (x == "yes").mean() * 100)
                      .reset_index(name="conv_rate")
                      .sort_values("conv_rate", ascending=True))
        fig = px.bar(job_conv, x="conv_rate", y="job", orientation="h",
                     title="Conversion Rate by Job Type (%)",
                     color="conv_rate",
                     color_continuous_scale=["#2a3560", COLORS["primary"], COLORS["yes"]])
        fig.update_layout(coloraxis_showscale=False, **PLOTLY_THEME)
        fig.update_xaxes(showgrid=True, gridcolor=COLORS["grid"])
        fig.update_yaxes(showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">Conversion Rate by Education</div>', unsafe_allow_html=True)
        edu_conv = (df.groupby("education")["subscribed"]
                      .apply(lambda x: (x == "yes").mean() * 100)
                      .reset_index(name="conv_rate")
                      .sort_values("conv_rate", ascending=False))
        fig = px.funnel(edu_conv, x="conv_rate", y="education",
                        title="Funnel: Education → Subscription Rate (%)",
                        color_discrete_sequence=[COLORS["primary"]])
        fig.update_layout(**PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — DEMOGRAPHICS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Age Distribution by Outcome</div>', unsafe_allow_html=True)
        bin_size = st.slider("Age bin size", 1, 10, 5, key="age_bin")
        fig = px.histogram(df, x="age", color="subscribed",
                           color_discrete_map={"yes": COLORS["yes"], "no": COLORS["no"]},
                           nbins=int((age_max - age_min) / bin_size),
                           barmode="overlay", opacity=0.75,
                           title="Age Distribution — Subscribed vs Not")
        styled_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Job Breakdown</div>', unsafe_allow_html=True)
        job_df = df["job"].value_counts().reset_index()
        job_df.columns = ["job", "count"]
        fig = px.bar(job_df, x="job", y="count",
                     color="count",
                     color_continuous_scale=["#2a3560", COLORS["primary"]],
                     title="Clients by Job Type")
        fig.update_layout(coloraxis_showscale=False, **PLOTLY_THEME)
        fig.update_xaxes(tickangle=35, showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-header">Marital Status</div>', unsafe_allow_html=True)
        mar_sub = (df.groupby(["marital", "subscribed"])
                     .size().reset_index(name="count"))
        fig = px.bar(mar_sub, x="marital", y="count", color="subscribed",
                     color_discrete_map={"yes": COLORS["yes"], "no": COLORS["no"]},
                     barmode="stack", title="Marital Status vs Subscription")
        styled_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">Age vs Balance (by Outcome)</div>', unsafe_allow_html=True)
        sample = df.sample(min(2000, len(df)), random_state=42)
        fig = px.scatter(sample, x="age", y="balance", color="subscribed",
                         color_discrete_map={"yes": COLORS["yes"], "no": COLORS["no"]},
                         opacity=0.55, title="Age vs Account Balance",
                         hover_data=["job", "education"])
        styled_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — FINANCIAL
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Balance Distribution (Log Scale)</div>', unsafe_allow_html=True)
        df_pos = df[df["balance"] > 0]
        fig = px.histogram(df_pos, x="balance", color="subscribed",
                           color_discrete_map={"yes": COLORS["yes"], "no": COLORS["no"]},
                           log_x=True, nbins=60, barmode="overlay", opacity=0.75,
                           title="Account Balance Distribution (€, log scale)")
        styled_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Average Balance by Job</div>', unsafe_allow_html=True)
        bal_job = (df.groupby("job")["balance"]
                     .mean().reset_index()
                     .sort_values("balance", ascending=True))
        fig = px.bar(bal_job, x="balance", y="job", orientation="h",
                     color="balance",
                     color_continuous_scale=["#2a3560", COLORS["accent"]],
                     title="Avg Balance by Job (€)")
        fig.update_layout(coloraxis_showscale=False, **PLOTLY_THEME)
        fig.update_yaxes(showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-header">Loan & Housing vs Subscription</div>', unsafe_allow_html=True)
        loan_cols = st.selectbox("Select attribute", ["housing", "loan", "default"], key="loan_sel")
        loan_df = (df.groupby([loan_cols, "subscribed"])
                     .size().reset_index(name="count"))
        fig = px.bar(loan_df, x=loan_cols, y="count", color="subscribed",
                     color_discrete_map={"yes": COLORS["yes"], "no": COLORS["no"]},
                     barmode="group", title=f"{loan_cols.title()} vs Subscription")
        styled_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">Balance Boxplot by Outcome</div>', unsafe_allow_html=True)
        grp_by = st.selectbox("Group by", ["subscribed", "education", "marital", "job"], key="box_grp")
        fig = px.box(df, x=grp_by, y="balance", color="subscribed",
                     color_discrete_map={"yes": COLORS["yes"], "no": COLORS["no"]},
                     title=f"Balance Distribution by {grp_by.title()}",
                     points=False)
        fig.update_layout(**PLOTLY_THEME)
        fig.update_xaxes(tickangle=30, showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CAMPAIGN
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Call Duration vs Outcome</div>', unsafe_allow_html=True)
        df["duration_min"] = df["duration"] / 60
        max_dur = st.slider("Max call duration (min)", 1, int(df["duration_min"].max()), 20, key="dur_sl")
        fig = px.histogram(df[df["duration_min"] <= max_dur],
                           x="duration_min", color="subscribed",
                           color_discrete_map={"yes": COLORS["yes"], "no": COLORS["no"]},
                           nbins=50, barmode="overlay", opacity=0.75,
                           title="Call Duration Distribution (minutes)")
        styled_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Campaign Contacts vs Conversion</div>', unsafe_allow_html=True)
        max_camp = st.slider("Max contacts shown", 1, 30, 15, key="camp_sl")
        camp_df = (df[df["campaign"] <= max_camp]
                     .groupby(["campaign", "subscribed"])
                     .size().reset_index(name="count"))
        fig = px.bar(camp_df, x="campaign", y="count", color="subscribed",
                     color_discrete_map={"yes": COLORS["yes"], "no": COLORS["no"]},
                     barmode="stack", title="# Campaign Contacts vs Subscription")
        styled_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-header">Contact Method</div>', unsafe_allow_html=True)
        contact_df = (df.groupby(["contact", "subscribed"])
                        .size().reset_index(name="count"))
        fig = px.bar(contact_df, x="contact", y="count", color="subscribed",
                     color_discrete_map={"yes": COLORS["yes"], "no": COLORS["no"]},
                     barmode="group", title="Contact Type vs Subscription")
        styled_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">Previous Outcome vs Conversion</div>', unsafe_allow_html=True)
        pout_df = (df.groupby(["poutcome", "subscribed"])
                     .size().reset_index(name="count"))
        fig = px.bar(pout_df, x="poutcome", y="count", color="subscribed",
                     color_discrete_map={"yes": COLORS["yes"], "no": COLORS["no"]},
                     barmode="group", title="Previous Campaign Outcome vs Current")
        styled_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Day-of-month heatmap
    st.markdown('<div class="section-header">Conversion Rate Heatmap (Month × Day)</div>', unsafe_allow_html=True)
    heat = (df.groupby(["month", "day"])["subscribed"]
              .apply(lambda x: round((x == "yes").mean() * 100, 1))
              .reset_index(name="conv_rate"))
    heat["month"] = pd.Categorical(heat["month"], categories=month_order, ordered=True)
    heat_pivot = heat.pivot(index="month", columns="day", values="conv_rate")
    fig = px.imshow(heat_pivot,
                    color_continuous_scale=["#1e2130", COLORS["primary"], COLORS["yes"]],
                    title="Conversion Rate % by Month & Day of Month",
                    aspect="auto")
    fig.update_layout(**PLOTLY_THEME)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — DEEP DIVE
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">Correlation Heatmap (Numeric Features)</div>', unsafe_allow_html=True)
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    corr = df[num_cols].corr()
    fig = px.imshow(corr, text_auto=".2f",
                    color_continuous_scale="RdBu_r",
                    zmin=-1, zmax=1,
                    title="Pearson Correlation Matrix")
    fig.update_layout(**PLOTLY_THEME)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Feature vs Conversion Rate (Custom)</div>', unsafe_allow_html=True)
        cat_features = [c for c in ["job","marital","education","contact","poutcome","month"] if c in df.columns]
        chosen_cat = st.selectbox("Categorical feature", cat_features, key="feat_cat")
        feat_conv = (df.groupby(chosen_cat)["subscribed"]
                       .apply(lambda x: (x == "yes").mean() * 100)
                       .reset_index(name="Conversion Rate (%)")
                       .sort_values("Conversion Rate (%)", ascending=False))
        fig = px.bar(feat_conv, x=chosen_cat, y="Conversion Rate (%)",
                     color="Conversion Rate (%)",
                     color_continuous_scale=["#2a3560", COLORS["yes"]],
                     title=f"Conversion Rate by {chosen_cat.title()}")
        fig.update_layout(coloraxis_showscale=False, **PLOTLY_THEME)
        fig.update_xaxes(tickangle=30, showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Numeric Feature Distribution</div>', unsafe_allow_html=True)
        chosen_num = st.selectbox("Numeric feature", num_cols, key="feat_num")
        fig = px.violin(df, x="subscribed", y=chosen_num, color="subscribed",
                        color_discrete_map={"yes": COLORS["yes"], "no": COLORS["no"]},
                        box=True, points=False,
                        title=f"{chosen_num.title()} — by Subscription Outcome")
        fig.update_layout(**PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)

    # Raw data explorer
    st.markdown('<div class="section-header">📋 Filtered Data Explorer</div>', unsafe_allow_html=True)
    show_n = st.slider("Rows to display", 10, 500, 50, key="raw_n")
    show_sub = st.radio("Show", ["All", "Subscribed (Yes)", "Not Subscribed (No)"], horizontal=True)
    display_df = df.copy()
    if show_sub == "Subscribed (Yes)":
        display_df = display_df[display_df["subscribed"] == "yes"]
    elif show_sub == "Not Subscribed (No)":
        display_df = display_df[display_df["subscribed"] == "no"]
    st.dataframe(display_df.head(show_n), use_container_width=True, height=300)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("🏦 Bank Marketing EDA Dashboard · Built with Streamlit & Plotly · Upload bank-full.csv via sidebar")
