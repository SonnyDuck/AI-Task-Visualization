import pandas as pd


def load_data(path="data/processed/final_dataset.csv"):
    """Load processed dataset."""
    return pd.read_csv(path)


def clean_data(df):
    """Basic data cleaning."""

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Standardize column names
    df.columns = df.columns.str.strip()

    return df

def get_kpis(df):

    return {
        "workers": df["User ID"].nunique(),
        "tasks": df["Task ID"].nunique(),
        "occupations": df["Occupation (O*NET-SOC Title)"].nunique(),
        "avg_desire": round(df["Automation Desire Rating"].mean(), 2),
        "avg_capacity": round(df["Automation Capacity Rating"].mean(), 2)
    }

def top_occupations(df, top_n=10):

    return (
        df.groupby("Occupation (O*NET-SOC Title)")[
            "Automation Desire Rating"
        ]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

def automation_distribution(df):

    return df["Automation Desire Rating"]

def scatter_dataset(df):

    return df[
        [
            "Automation Desire Rating",
            "Automation Capacity Rating",
            "Occupation (O*NET-SOC Title)"
        ]
    ].dropna()

def correlation_data(df):

    columns = [
        "Automation Desire Rating",
        "Automation Capacity Rating",
        "Core Skill Rating",
        "Enjoyment Rating",
        "Human Agency Scale Rating_x",
        "Importance"
    ]

    return df[columns].corr(numeric_only=True)

def automation_reasons(df):

    reason_cols = [c for c in df.columns if "Reason" in c]

    result = (
        df[reason_cols]
        .apply(pd.to_numeric, errors="coerce")
        .fillna(0)
        .sum()
        .sort_values(ascending=False)
        .astype(float)
        .reset_index()
    )

    result.columns = ["Reason", "Count"]

    return result