import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="💰 Finance Dashboard", layout="wide")

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("transactions.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.strftime("%B")
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("📊 Filters")
month = st.sidebar.selectbox("Select Month", df["Month"].unique())
filtered_df = df[df["Month"] == month]

# Income, Expense, Savings
income = filtered_df[filtered_df['Type'] == 'Income']['Amount'].sum()
expense = filtered_df[filtered_df['Type'] == 'Expense']['Amount'].sum()
savings = income - expense
goal = st.sidebar.slider("Set Monthly Savings Goal", 1000, 50000, 10000)

# Top KPIs
st.title("🚀 FinPro Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"₹{income:,.0f}")
col2.metric("Total Expenses", f"₹{expense:,.0f}")
col3.metric("Net Savings", f"₹{savings:,.0f}")

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    pie = px.pie(filtered_df[filtered_df["Type"] == "Expense"],
                 names="Category",
                 values="Amount",
                 hole=0.4,
                 title="Spending by Category",
                 color_discrete_sequence=px.colors.sequential.Agsunset)
    st.plotly_chart(pie, use_container_width=True)

with col2:
    line = px.line(filtered_df, x="Date", y="Amount", color="Type",
                   title="Transaction Trend",
                   color_discrete_map={"Expense": "red", "Income": "green"})
    st.plotly_chart(line, use_container_width=True)

# Savings Progress
st.subheader("🏦 Savings Progress")
progress = min(savings / goal, 1.0)
st.progress(progress)

# Transaction Table
st.subheader("📂 Transactions")
st.dataframe(filtered_df.sort_values("Date", ascending=False), use_container_width=True)
