"""
Author: Bartev
Date: 2025-04-10

Follow video here
https://www.youtube.com/watch?v=Yk-unX4KnV4

Ken Jee (author of 66 days of data)

Get data from Ken Jee YouTube Data
https://www.kaggle.com/datasets/kenjee/ken-jee-youtube-data


"""

import itertools
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from plotly import express as px
from plotly import graph_objects as go

# functions


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Column names had `-` in them"""
    df.columns = [
        "Video",
        "Video title",
        "Video publish time",
        "Comments added",
        "Shares",
        "Dislikes",
        "Likes",
        "Subscribers lost",
        "Subscribers gained",
        "RPM (USD)",
        "CPM (USD)",
        "Average percentage viewed (%)",
        "Average view duration",
        "Views",
        "Watch time (hours)",
        "Subscribers",
        "Your estimated revenue (USD)",
        "Impressions",
        "Impressions click-through rate (%)",
    ]
    return df


def duration_to_seconds(duration_str):
    try:
        t = datetime.strptime(duration_str, "%H:%M:%S")
        return t.second + t.minute * 60 + t.hour * 3600
    except Exception:
        return None


def parse_dates_and_durations(df: pd.DataFrame) -> pd.DataFrame:
    df["Video publish time"] = pd.to_datetime(df["Video publish time"], errors="coerce")
    df["Avg_duration_sec"] = df["Average view duration"].apply(duration_to_seconds)
    return df


def add_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df["Engagement_ratio"] = (
        df["Comments added"] + df["Shares"] + df["Dislikes"] + df["Likes"]
    ) / df["Views"]

    df["Views / sub gained"] = df.apply(
        lambda row: (
            row["Views"] / row["Subscribers gained"]
            if row["Subscribers gained"]
            else None
        ),
        axis=1,
    )
    return df


def sort_by_date(
    df: pd.DataFrame, sort_col: str = "Video publish time"
) -> pd.DataFrame:
    return df.sort_values(sort_col, ascending=False)


def style_pos_neg(v):
    try:
        if v < 0:
            return "color:red;"
        elif v > 0:
            return "color:green;"
        else:
            return "color:gray;"
    except:
        return None


def audience_simple(country):
    """Map country codes to simplified labels."""
    mapping = {
        "US": "USA",
        "IN": "India",
    }
    return mapping.get(country, "Other")


# Load data


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Read the data, skipping the first data row
    Still reads the column names.
    First row is Totals
    """
    # 🚀 Full pipeline using method chaining + .pipe()
    data_path = Path("./data")
    file_path = data_path / "Aggregated_Metrics_By_Video.csv"

    df_agg = (
        pd.read_csv(file_path, skiprows=1)
        .pipe(clean_column_names)
        .pipe(parse_dates_and_durations)
        .pipe(add_metrics)
        .pipe(sort_by_date)
    )

    df_agg_sub = pd.read_csv(
        data_path / "Aggregated_Metrics_By_Country_And_Subscriber_Status.csv"
    )
    df_comments = pd.read_csv(data_path / "All_Comments_Final.csv")
    df_time = pd.read_csv(data_path / "Video_Performance_Over_Time.csv").assign(
        Date=lambda df: pd.to_datetime(df["Date"], errors="coerce")
    )

    return df_agg, df_agg_sub, df_comments, df_time


df_agg, df_agg_sub, df_comments, df_time = load_data()

# Engineer data
df_agg_diff = df_agg.copy()
metric_date_12mo = df_agg_diff["Video publish time"].max() - pd.DateOffset(months=12)
# median_agg = df_agg_diff[df_agg_diff["Video publish time"] >= metric_date_12mo]
median_agg = (
    df_agg_diff.pipe(lambda df: df[df["Video publish time"] >= metric_date_12mo])
    .select_dtypes(include="number")
    .median()
)

numeric_cols = np.array(
    (df_agg_diff.dtypes == "float64") | (df_agg_diff.dtypes == "int64")
)
# Use like
# df_agg_diff.columns[numeric_cols] == numeric_columns
numeric_columns = df_agg_diff.select_dtypes("number").columns

df_agg_diff.iloc[:, numeric_cols] = (
    df_agg_diff.iloc[:, numeric_cols] - median_agg
).div(median_agg)

# Merge daily data with publish data to get delta
df_time_diff = pd.merge(
    df_time,
    df_agg.loc[:, ["Video", "Video publish time"]],
    left_on="External Video ID",
    right_on="Video",
).assign(days_published=lambda x: (x["Date"] - x["Video publish time"]).dt.days)

# Get last 12 months of data rather than all data
date_12mo = df_agg["Video publish time"].max() - pd.DateOffset(months=12)
df_time_diff_yr = df_time_diff[lambda x: x["Video publish time"] >= date_12mo]


# Get daily view data (first 30), median & percentiles
def pct_80(x):
    return np.percentile(x, 80)


def pct_20(x):
    return np.percentile(x, 20)


views_days = (
    pd.pivot_table(
        df_time_diff_yr,
        index="days_published",
        values="Views",
        aggfunc=[
            np.mean,
            np.median,
            pct_80,
            pct_20,
            # lambda x: np.percentile(x, 80),  # 80th percentile
            # lambda x: np.percentile(x, 20),  # 20th percentile
        ],
    )
    .reset_index()
    .pipe(
        lambda df: df.set_axis(
            [
                "days_published",
                "mean_views",
                "median_views",
                "80pct_views",
                "20pct_views",
            ],
            axis=1,
        )
    )
    .loc[lambda df: df["days_published"].between(0, 30)]
)
views_cumulative = views_days.loc[
    :, ["days_published", "median_views", "80pct_views", "20pct_views"]
].assign(
    **{
        "median_views": lambda df: df["median_views"].cumsum(),
        "80pct_views": lambda df: df["80pct_views"].cumsum(),
        "20pct_views": lambda df: df["20pct_views"].cumsum(),
    }
)


## What metrics will be relevant?
## Difference from baseline
## Percent change by video

# Build dashboard
add_sidebar = st.sidebar.selectbox(
    "Aggregate or Individual Video", ("Aggregate Metrics", "Individual Video Analysis")
)


## Total picture
if add_sidebar == "Aggregate Metrics":
    st.write("Agg")
    agg_metrics_cols = [
        "Video publish time",
        "Views",
        "Likes",
        "Subscribers",
        "Shares",
        "Comments added",
        "RPM (USD)",
        # "Average % viewed",
        "Avg_duration_sec",
        "Engagement_ratio",
        "Views / sub gained",
        "Dislikes",
        "Subscribers lost",
        "Subscribers gained",
        "CPM (USD)",
        "Average percentage viewed (%)",
        "Average view duration",
        "Watch time (hours)",
        "Your estimated revenue (USD)",
        "Impressions",
        "Impressions click-through rate (%)",
    ]
    df_agg_metrics = df_agg[agg_metrics_cols]

    metric_date_6mo = df_agg_metrics["Video publish time"].max() - pd.DateOffset(
        months=6
    )

    metric_date_12mo = df_agg_metrics["Video publish time"].max() - pd.DateOffset(
        months=12
    )
    metric_medians6mo = (
        df_agg_metrics.pipe(
            lambda df: df[df_agg_metrics["Video publish time"] >= metric_date_6mo]
        )
        .select_dtypes(include="number")
        .median()
    )
    metric_medians12mo = (
        df_agg_metrics.pipe(
            lambda df: df[df_agg_metrics["Video publish time"] >= metric_date_12mo]
        )
        .select_dtypes(include="number")
        .median()
    )

    # Define the columns, then create a cycle, so 1, 2, 3, 4, 5, 1, 2,...
    columns = st.columns(5)
    column_cycle = itertools.cycle(columns)

    for idx in metric_medians6mo.index:
        with next(column_cycle):
            delta = (
                metric_medians6mo[idx] - metric_medians12mo[idx]
            ) / metric_medians12mo[idx]
            st.metric(
                label=idx, value=round(metric_medians6mo[idx], 1), delta=f"{delta:.2%}"
            )

    final_cols = [
        "Video title",
        # "Video publish time",
        "Publish_date",
        "Views",
        "Likes",
        "Subscribers",
        # "Shares",
        # "Comments added",
        # "RPM (USD)",
        # "Average % viewed",
        "Avg_duration_sec",
        "Engagement_ratio",
        "Views / sub gained",
        # "Dislikes",
        # "Subscribers lost",
        # "Subscribers gained",
        # "CPM (USD)",
        # "Average percentage viewed (%)",
        # "Average view duration",
        # "Watch time (hours)",
        # "Your estimated revenue (USD)",
        # "Impressions",
        # "Impressions click-through rate (%)",
    ]
    df_agg_diff["Publish_date"] = df_agg_diff["Video publish time"].apply(
        lambda x: x.date()
    )
    df_agg_diff_final = df_agg_diff.loc[:, final_cols]

    final_numeric_cols = df_agg_diff_final.select_dtypes(include="number").columns
    st.dataframe(
        df_agg_diff_final.style.format("{:.1%}", subset=final_numeric_cols).applymap(
            style_pos_neg, subset=final_numeric_cols
        )
    )

if add_sidebar == "Individual Video Analysis":
    st.write("Ind")
    # `options` is an iterable (list, set, tuple, st.dataframe (uses 1st col))
    video_select = st.selectbox(
        label="Pick a Video", options=df_agg["Video title"], index=None
    )

    agg_filtered = df_agg[lambda x: x["Video title"] == video_select]
    agg_sub_filtered = (
        df_agg_sub.loc[lambda x: x["Video Title"] == video_select]
        .assign(Country=lambda x: x["Country Code"].apply(audience_simple))
        .sort_values("Is Subscribed")
    )
    # Set consistent category order for the y-axis and legend
    category_orders = {
        "Is Subscribed": [True, False],
        "Country": ["USA", "India", "Other"],  # ← country_order
    }
    # Fix the color mapping
    color_map = {
        "USA": "#1f77b4",  # blue
        "India": "#ff7f0e",  # orange
        "Other": "#2ca02c",  # green
    }
    fig = px.bar(
        data_frame=agg_sub_filtered,
        x="Views",
        y="Is Subscribed",
        color="Country",
        orientation="h",
        category_orders=category_orders,
        # color_discrete_map=color_map,
    )
    st.plotly_chart(fig)

    agg_time_filtered = df_time_diff[lambda x: x["Video Title"] == video_select]
    first_30 = agg_time_filtered[
        lambda x: x["days_published"].between(0, 30)
    ].sort_values("days_published")

    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(
            x=views_cumulative["days_published"],
            y=views_cumulative["20pct_views"],
            mode="lines",
            name="20th percentile",
            line=dict(color="purple", dash="dash"),
        )
    )
    fig2.add_trace(
        go.Scatter(
            x=views_cumulative["days_published"],
            y=views_cumulative["median_views"],
            mode="lines",
            name="50th percentile",
            line=dict(color="black", dash="dash"),
        )
    )
    fig2.add_trace(
        go.Scatter(
            x=views_cumulative["days_published"],
            y=views_cumulative["80pct_views"],
            mode="lines",
            name="80th percentile",
            line=dict(color="royalblue", dash="dash"),
        )
    )
    fig2.add_trace(
        go.Scatter(
            x=first_30["days_published"],
            y=first_30["Views"].cumsum(),
            mode="lines",
            name="Current Video",
            line=dict(color="firebrick", width=8),
        )
    )
    fig2.update_layout(
        title="View comparison first 30 days",
        xaxis_title="Days Since Published",
        yaxis_title="Cumulative Views",
    )
    st.plotly_chart(fig2)
