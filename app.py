import streamlit as st

from src.preprocessing import *
from src.visualization import *

tab1, tab2, tab3 = st.tabs([
    "📊 Dashboard",
    "📈 Statistics",
    "🗂 Dataset"
])

st.set_page_config(
    page_title="AI Task Visualization",
    page_icon="📊",
    layout="wide"
)

df = load_data()
df = clean_data(df)

st.title("📊 AI Task Visualization Dashboard")

st.markdown(
    """
    Interactive dashboard built with Streamlit and Plotly.
    """
)

with st.expander("📌 About Dataset"):

    st.markdown("""
    This dashboard explores workers' perceptions of AI automation.

    **Dataset includes:**
    - Worker preferences
    - Expert AI capability ratings
    - Occupation metadata
    - Demographic information
    """)

st.sidebar.header("Filters")

occupations = sorted(
    df["Occupation (O*NET-SOC Title)"]
    .dropna()
    .unique()
)

selected = st.sidebar.multiselect(
    "Occupation",
    occupations,
    default=occupations
)

df = df[
    df["Occupation (O*NET-SOC Title)"]
    .isin(selected)
]

top_n = st.sidebar.slider(
    "Top Occupations",
    5,
    20,
    10
)

kpi = get_kpis(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Workers",
    kpi["workers"]
)

col2.metric(
    "Tasks",
    kpi["tasks"]
)

col3.metric(
    "Automation Desire",
    kpi["avg_desire"]
)

col4.metric(
    "Automation Capacity",
    kpi["avg_capacity"]
)


col1, col2 = st.columns(2)

with col1:
    st.subheader("Automation Desire Distribution")

    fig = histogram(
        df,
        "Automation Desire Rating"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top Occupations")

    top = top_occupations(df, top_n)

    fig = bar(
        top,
        "Occupation (O*NET-SOC Title)",
        "Automation Desire Rating"
    )

    st.plotly_chart(fig, use_container_width=True)


col1, col2 = st.columns(2)

with col1:

    st.subheader("Automation Desire vs AI Capability")

    scatter_df = scatter_dataset(df)

    fig = scatter(scatter_df)

    st.plotly_chart(fig, use_container_width=True)

with col2:

    st.subheader("Reasons for Automation")

    reason = automation_reasons(df)

    fig = pie(reason)

    st.plotly_chart(fig, use_container_width=True)

st.subheader("Correlation Matrix")

corr = correlation_data(df)

fig = heatmap(corr)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Summary Statistics")

st.dataframe(
    df.describe().T
)

st.subheader("Dataset")

show = st.checkbox(
    "Show raw data"
)

if show:
    st.dataframe(df)

csv = df.to_csv(index=False)

st.download_button(
    "Download CSV",
    csv,
    file_name="filtered_dataset.csv",
    mime="text/csv"
)

st.divider()

st.caption(
    "Developed with Streamlit • Plotly • Pandas"
)