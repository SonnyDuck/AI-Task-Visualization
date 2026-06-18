import plotly.express as px
import plotly.graph_objects as go

def histogram(df, column):

    fig = px.histogram(
        df,
        x=column,
        nbins=20
    )

    return fig

def bar(df, x, y):

    fig = px.bar(
        df,
        x=x,
        y=y
    )

    return fig

def scatter(df):

    fig = px.scatter(
        df,
        x="Automation Desire Rating",
        y="Automation Capacity Rating",
        color="Occupation (O*NET-SOC Title)"
    )

    return fig

def heatmap(corr):

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto"
    )

    return fig

def pie(df):

    fig = px.pie(
        df,
        names="Reason",
        values="Count"
    )

    return fig