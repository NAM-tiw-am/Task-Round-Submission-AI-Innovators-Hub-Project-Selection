
import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Bank Marketing Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Bank Marketing Subscription Dashboard")
st.markdown("Analyze customer subscription behavior and cross-sell opportunities.")

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    df = pd.read_csv("bank-full.csv", sep=";")
    return df

df = load_data()

# =====================================================
# PREPROCESSING
# =====================================================

df["subscribed"] = (df["y"] == "yes").astype(int)

# Age groups
df["age_group"] = pd.cut(
    df["age"],
    bins=[18, 30, 45, 60, 100],
    labels=["18-30", "31-45", "46-60", "60+"],
    include_lowest=True
)

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Filters")

selected_jobs = st.sidebar.multiselect(
    "Job Type",
    options=sorted(df["job"].unique()),
    default=sorted(df["job"].unique())
)

selected_housing = st.sidebar.multiselect(
    "Housing Loan",
    options=["yes", "no"],
    default=["yes", "no"]
)

age_range = st.sidebar.slider(
    "Age Range",
    int(df["age"].min()),
    int(df["age"].max()),
    (
        int(df["age"].min()),
        int(df["age"].max())
    )
)

# =====================================================
# APPLY FILTERS
# =====================================================

filtered = df[
    (df["job"].isin(selected_jobs))
    & (df["housing"].isin(selected_housing))
    & (df["age"] >= age_range[0])
    & (df["age"] <= age_range[1])
]

# =====================================================
# KPI SECTION
# =====================================================

total_customers = len(filtered)

total_subscribers = filtered["subscribed"].sum()

subscription_rate = (
    total_subscribers / total_customers * 100
    if total_customers > 0
    else 0
)

avg_balance = filtered["balance"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Customers", f"{total_customers:,}")
col2.metric("Subscribers", f"{total_subscribers:,}")
col3.metric("Subscription Rate", f"{subscription_rate:.2f}%")
col4.metric("Average Balance", f"€{avg_balance:,.0f}")

st.divider()

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Job Analysis",
        "Balance Analysis",
        "Age Analysis",
        "Housing Loan",
        "Data Explorer"
    ]
)

# =====================================================
# TAB 1 - JOB ANALYSIS
# =====================================================

with tab1:

    st.subheader("Subscription Rate by Job Type")

    job_rate = (
        filtered
        .groupby("job")["subscribed"]
        .mean()
        .reset_index()
    )

    job_rate["subscription_rate"] = (
        job_rate["subscribed"] * 100
    )

    fig = px.bar(
        job_rate.sort_values(
            "subscription_rate",
            ascending=False
        ),
        x="job",
        y="subscription_rate",
        text="subscription_rate",
        title="Subscription Rate by Job"
    )

    fig.update_traces(texttemplate="%{text:.1f}%")

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# TAB 2 - BALANCE ANALYSIS
# =====================================================

with tab2:

    st.subheader("Balance vs Subscription")

    num_bins = st.slider(
        "Balance Buckets",
        min_value=4,
        max_value=15,
        value=8
    )

    balance_df = filtered.copy()

    balance_df["balance_group"] = pd.qcut(
        balance_df["balance"],
        q=num_bins,
        duplicates="drop"
    )

    balance_rate = (
        balance_df
        .groupby("balance_group")["subscribed"]
        .mean()
        .reset_index()
    )

    # Convert interval objects to strings
    balance_rate["balance_group"] = (
        balance_rate["balance_group"]
        .astype(str)
    )

    balance_rate["subscription_rate"] = (
        balance_rate["subscribed"] * 100
    )

    fig = px.line(
        balance_rate,
        x="balance_group",
        y="subscription_rate",
        markers=True,
        title="Subscription Rate by Balance Bucket"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# TAB 3 - AGE ANALYSIS
# =====================================================

with tab3:

    st.subheader("Subscription Rate by Age Group")

    age_rate = (
        filtered
        .groupby("age_group")["subscribed"]
        .mean()
        .reset_index()
    )

    age_rate["subscription_rate"] = (
        age_rate["subscribed"] * 100
    )

    fig = px.bar(
        age_rate,
        x="age_group",
        y="subscription_rate",
        text="subscription_rate",
        title="Subscription Rate by Age Group"
    )

    fig.update_traces(texttemplate="%{text:.1f}%")

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# TAB 4 - HOUSING LOAN
# =====================================================

with tab4:

    st.subheader(
        "Impact of Existing Housing Loan"
    )

    housing_rate = (
        filtered
        .groupby("housing")["subscribed"]
        .mean()
        .reset_index()
    )

    housing_rate["subscription_rate"] = (
        housing_rate["subscribed"] * 100
    )

    fig = px.bar(
        housing_rate,
        x="housing",
        y="subscription_rate",
        text="subscription_rate",
        title="Subscription Rate by Housing Loan Status"
    )

    fig.update_traces(texttemplate="%{text:.1f}%")

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# TAB 5 - DATA EXPLORER
# =====================================================

with tab5:

    st.subheader("Filtered Dataset")

    st.dataframe(
        filtered,
        use_container_width=True
    )

    csv = filtered.to_csv(index=False)

    st.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name="filtered_bank_data.csv",
        mime="text/csv"
    )

