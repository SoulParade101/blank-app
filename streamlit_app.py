import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Tailoring Business Dashboard", layout="wide")

st.title("🧵 Tailoring Business Management Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Test Sheet for App using Python.xlsx")
    
    # Standardize column names (edit if needed)
    df.columns = df.columns.str.strip()

    # Convert date columns
    if "Order Date" in df.columns:
        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df["Quarter"] = df["Order Date"].dt.to_period("Q")
    
    return df

df = load_data()

st.sidebar.header("Filters")

# -----------------------------
# CUSTOMER FILTER
# -----------------------------
if "Customer Name" in df.columns:
    customer_filter = st.sidebar.multiselect(
        "Select Customer",
        options=df["Customer Name"].unique(),
        default=df["Customer Name"].unique()
    )
    df = df[df["Customer Name"].isin(customer_filter)]

# -----------------------------
# 1️⃣ COMMISSION VS TAILOR CHARGES
# -----------------------------
st.header("1️⃣ Commission vs Tailor Charges")

if "Commission" in df.columns and "Tailor Charges" in df.columns:

    summary = df[["Commission", "Tailor Charges"]].sum().reset_index()
    summary.columns = ["Category", "Amount"]

    fig1 = px.bar(summary, x="Category", y="Amount",
                  text="Amount",
                  title="Commission vs Tailor Charges")

    st.plotly_chart(fig1, use_container_width=True)

    net_earnings = df["Commission"].sum() - df["Tailor Charges"].sum()
    st.metric("Net Earnings (Overall)", f"₹ {net_earnings:,.2f}")

# -----------------------------
# 2️⃣ QoQ NET EARNINGS
# -----------------------------
st.header("2️⃣ QoQ Net Commission Earnings")

if "Quarter" in df.columns:
    qoq = df.groupby("Quarter")[["Commission", "Tailor Charges"]].sum().reset_index()
    qoq["Net Earnings"] = qoq["Commission"] - qoq["Tailor Charges"]

    fig2 = px.line(qoq,
                   x=qoq["Quarter"].astype(str),
                   y="Net Earnings",
                   markers=True,
                   title="Quarter-on-Quarter Net Earnings")

    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# 3️⃣ INFLOW VS OUTFLOW
# -----------------------------
st.header("3️⃣ Inflow vs Outflow (Clothes)")

if "Quantity Collected" in df.columns and "Quantity Delivered" in df.columns:

    inflow_outflow = pd.DataFrame({
        "Type": ["Collected", "Delivered"],
        "Quantity": [
            df["Quantity Collected"].sum(),
            df["Quantity Delivered"].sum()
        ]
    })

    fig3 = px.pie(inflow_outflow,
                  names="Type",
                  values="Quantity",
                  title="Cloth Inflow vs Outflow")

    st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# 4️⃣ RECURRING CUSTOMER ANALYSIS
# -----------------------------
st.header("4️⃣ Customer Recurrence Analysis")

if "Customer Name" in df.columns:

    customer_counts = df["Customer Name"].value_counts().reset_index()
    customer_counts.columns = ["Customer Name", "Order Count"]

    fig4 = px.bar(customer_counts,
                  x="Customer Name",
                  y="Order Count",
                  title="Customer Recurrence Frequency")

    st.plotly_chart(fig4, use_container_width=True)

    recurring = customer_counts[customer_counts["Order Count"] > 1]
    st.subheader("Recurring Customers")
    st.dataframe(recurring)

# -----------------------------
# DOWNLOAD REPORT
# -----------------------------
st.header("📄 Download Summary Report")

summary_report = df.describe(include="all")

st.download_button(
    label="Download Report as CSV",
    data=summary_report.to_csv().encode("utf-8"),
    file_name="tailoring_summary_report.csv",
    mime="text/csv"
)



