import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def histogram(df, column):

    fig = px.histogram(
        df,
        x=column,
        nbins=20
    )
    fig.update_layout(
        template="plotly_white",
        height=450
    )

    return fig

def bar(df, x, y):

    fig = px.bar(
        df,
        x=x,
        y=y
    )
    fig.update_layout(
        template="plotly_white",
        height=450
    )

    return fig

def scatter(df):

    fig = px.scatter(
        df,
        x="Automation Desire Rating",
        y="Automation Capacity Rating",
        color="Occupation (O*NET-SOC Title)"
    )
    fig.update_layout(
        template="plotly_white",
        height=500
    )

    return fig

def heatmap(corr):

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto"
    )
    fig.update_layout(
        template="plotly_white",
        height=500
)

    return fig

def pie(df):
    df["Count"] = pd.to_numeric(df["Count"], errors="coerce").fillna(0)

    fig = px.pie(
        df,
        names="Reason",
        values="Count"
    )
    fig.update_layout(
        template="plotly_white",
        height=450
)

    return fig