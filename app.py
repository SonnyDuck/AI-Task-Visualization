import streamlit as st

from src.preprocessing import *
from src.visualization import *

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


st.subheader("Automation Desire Distribution")

fig = histogram(
    df,
    "Automation Desire Rating"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.subheader("Top Occupations")

top = top_occupations(
    df,
    top_n
)

fig = bar(
    top,
    "Occupation (O*NET-SOC Title)",
    "Automation Desire Rating"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.subheader("Automation Desire vs AI Capability")

scatter_df = scatter_dataset(df)

fig = scatter(scatter_df)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.subheader("Correlation")

corr = correlation_data(df)

fig = heatmap(corr)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.subheader("Reasons for Automation")

reason = automation_reasons(df)

fig = pie(reason)

st.plotly_chart(
    fig,
    use_container_width=True
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