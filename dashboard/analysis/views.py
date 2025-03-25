"""
views.py

This module defines the views for the Django web dashboard, including:
- Loading and processing COVID-19 data from a CSV file.
- Generating various data visualizations (histograms, heatmaps, line charts, etc.).
- Providing an interactive dashboard for users to filter data by state.
- Supporting AJAX-based chart updates for dynamic user interaction.

Charts Included:
- Case Fatality Ratio Distribution
- Correlation Matrix Heatmap
- Daily Cases Trend
- Top N States by Case Type
- Recovery Rate Distribution
- Active vs. Confirmed Cases Scatter Plot

Author: [Aquil Iqbal]
Email : [aquiliqbal14@gmail.com]
"""

import base64
import io
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
import matplotlib

matplotlib.use('Agg')  # Non-interactive backend

# Load Dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_FILE = os.path.join(
#     BASE_DIR, r"C:\Users\aquil\ostds\assign1_covid\world_usage\processed_data.csv"
# )

DATA_FILE = os.path.join(
    BASE_DIR, "..", "..", "assign1_covid", "world_usage", "processed_data.csv"
)

# Load Data with Fixes


def load_data(state=None):
    df = pd.read_csv(DATA_FILE)
    df.dropna(inplace=True)

    df['Last_Update'] = pd.to_datetime(df['Last_Update'])

    # Keep only numeric columns to avoid 'could not convert string to float' errors
    numeric_columns = ['Confirmed', 'Deaths', 'Recovered', 'Active']

    # Convert numeric columns safely, coercing errors to NaN
    df[numeric_columns] = df[numeric_columns].apply(
        pd.to_numeric, errors='coerce')

    # Drop rows where numeric values are NaN after conversion
    df.dropna(subset=numeric_columns, inplace=True)

    # Ensure Province_State is treated as a string (categorical data)
    df['Province_State'] = df['Province_State'].astype(str)

    # Derive new calculated columns
    df['Case_Fatality_Ratio'] = (df['Deaths'] / df['Confirmed']) * 100
    df['Recovery_Rate'] = (df['Recovered'] / df['Confirmed']) * 100

    # Apply State Filter
    if state:
        df = df[df['Province_State'] == state]

    return df

# Convert Plot to Image


def get_plot(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode("utf-8")
    return "data:image/png;base64," + string

# Case Fatality Ratio Chart


def case_fatality_chart(state=None):
    df = load_data(state)
    if df.empty:
        return None
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['Case_Fatality_Ratio'], kde=True, ax=ax)
    ax.set_title("Case Fatality Ratio Distribution")
    return get_plot(fig)

# Correlation Matrix Chart


def correlation_matrix_chart(state=None):
    df = load_data(state)
    numeric_df = df.select_dtypes(include=['number'])
    if numeric_df.empty:
        return None
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(numeric_df.corr(), annot=True,
                cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title("Correlation Matrix Heatmap")
    return get_plot(fig)

# Daily Cases Trend Chart


def daily_cases_chart(state=None):
    df = load_data(state)
    if df.empty:
        return None
    daily_cases = df.groupby(df['Last_Update'].dt.date)['Confirmed'].sum()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=daily_cases.index, y=daily_cases.values, ax=ax)
    ax.set_title("Daily Cases Trend")
    return get_plot(fig)

# Top N States Chart


def top_n_states_chart(top_n=10, case_type="Confirmed"):
    df = load_data()
    if case_type not in df.columns:
        case_type = "Confirmed"  # Default to Confirmed cases if invalid column
    if df.empty:
        return None
    top_states = df.groupby("Province_State")[case_type].sum().nlargest(top_n)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=top_states.values, y=top_states.index, ax=ax)
    ax.set_title(f"Top {top_n} States by {case_type}")
    return get_plot(fig)

# Recovery Rate Distribution Chart


def recovery_rate_chart(state=None):
    df = load_data(state)
    if df.empty:
        return None
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['Recovery_Rate'], kde=True, ax=ax)
    ax.set_title("Recovery Rate Distribution")
    return get_plot(fig)

# Active vs Confirmed Cases Chart


def active_vs_confirmed_chart(state=None):
    df = load_data(state)
    if df.empty:
        return None
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x=df['Confirmed'], y=df['Active'], ax=ax)
    ax.set_title("Active Cases vs. Confirmed Cases")
    return get_plot(fig)

# Main Dashboard View


def dashboard(request):
    df = load_data()
    states = sorted(df["Province_State"].unique())

    context = {
        "states": states,
        "case_fatality_chart": case_fatality_chart() or "",
        "correlation_matrix_chart": correlation_matrix_chart() or "",
        "daily_cases_chart": daily_cases_chart() or "",
        "top_n_states_chart": top_n_states_chart() or "",
        "recovery_rate_chart": recovery_rate_chart() or "",
        "active_vs_confirmed_chart": active_vs_confirmed_chart() or "",
    }

    return render(request, "dashboard.html", context)

# AJAX Update Charts


def update_charts(request):
    state = request.GET.get("state")
    case_type = request.GET.get("case_type", "Confirmed")
    top_n = int(request.GET.get("top_n", 10))

    return JsonResponse({
        "case_fatality_chart": case_fatality_chart(state) or "",
        "correlation_matrix_chart": correlation_matrix_chart(state) or "",
        "daily_cases_chart": daily_cases_chart(state) or "",
        "top_n_states_chart": top_n_states_chart(top_n, case_type) or "",
        "recovery_rate_chart": recovery_rate_chart(state) or "",
        "active_vs_confirmed_chart": active_vs_confirmed_chart(state) or "",
    })
