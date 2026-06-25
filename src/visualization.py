import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def apply_premium_layout(fig):
    """Applies a clean, modern design theme to a Plotly figure."""
    fig.update_layout(
        template="plotly_white",
        font_family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        margin=dict(t=30, l=30, r=20, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(
            bgcolor="#ffffff",
            font_size=13,
            font_family="Inter, sans-serif",
            bordercolor="#e2e8f0"
        ),
        xaxis=dict(
            gridcolor="#f1f5f9",
            linecolor="#e2e8f0",
            title=dict(font=dict(size=12, color="#475569")),
            tickfont=dict(size=10, color="#64748b")
        ),
        yaxis=dict(
            gridcolor="#f1f5f9",
            linecolor="#e2e8f0",
            title=dict(font=dict(size=12, color="#475569")),
            tickfont=dict(size=10, color="#64748b")
        )
    )

def histogram(df, column):
    fig = px.histogram(
        df,
        x=column,
        nbins=20,
        color_discrete_sequence=["#3b82f6"]
    )
    apply_premium_layout(fig)
    fig.update_layout(
        height=400,
        bargap=0.08
    )
    fig.update_traces(
        marker=dict(
            line=dict(width=0.5, color="#ffffff")
        )
    )
    return fig

def bar(df, x, y):
    fig = px.bar(
        df,
        x=x,
        y=y,
        color_discrete_sequence=["#10b981"]
    )
    apply_premium_layout(fig)
    fig.update_layout(
        height=400,
        xaxis=dict(tickangle=35)
    )
    fig.update_traces(
        marker=dict(
            line=dict(width=0.5, color="#ffffff")
        )
    )
    return fig

def scatter(df):
    fig = px.scatter(
        df,
        x="Automation Desire Rating",
        y="Automation Capacity Rating",
        color="Occupation (O*NET-SOC Title)",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    apply_premium_layout(fig)
    fig.update_layout(
        height=450,
        legend=dict(
            title=None,
            font=dict(size=9, color="#64748b"),
            orientation="h",
            yanchor="bottom",
            y=-0.55,
            xanchor="center",
            x=0.5
        )
    )
    fig.update_traces(
        marker=dict(
            size=9,
            opacity=0.75,
            line=dict(width=0.8, color="#ffffff")
        )
    )
    return fig

def heatmap(corr):
    custom_scale = [
        [0.0, "#f8fafc"],
        [0.2, "#eff6ff"],
        [0.4, "#bfdbfe"],
        [0.6, "#60a5fa"],
        [0.8, "#2563eb"],
        [1.0, "#1e3a8a"]
    ]
    
    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale=custom_scale
    )
    apply_premium_layout(fig)
    fig.update_layout(
        height=450,
        coloraxis_showscale=False
    )
    return fig

def pie(df):
    df["Count"] = pd.to_numeric(df["Count"], errors="coerce").fillna(0)

    fig = px.pie(
        df,
        names="Reason",
        values="Count",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    apply_premium_layout(fig)
    fig.update_layout(
        height=450,
        legend=dict(
            title=None,
            font=dict(size=9, color="#64748b"),
            orientation="h",
            yanchor="bottom",
            y=-0.35,
            xanchor="center",
            x=0.5
        )
    )
    fig.update_traces(
        textposition='inside',
        textinfo='percent',
        hole=0.42,
        marker=dict(
            line=dict(width=1.5, color="#ffffff")
        )
    )
    return fig