import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="Expense Tracker", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>

.main {
background-color: #f5f7fb;
}

.card {
background-color: white;
padding: 20px;
border-radius: 10px;
box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
text-align: center;
}

.metric {
font-size: 28px;
font-weight: bold;
color: #2c3e50;
}

.label {
font-size: 16px;
color: gray;
}

</style>
""", unsafe_allow_html=True)

st.title("💰 Smart Expense Tracker Dashboard")

# ---------- SESSION STORAGE ----------
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# ---------- SIDEBAR ----------
st.sidebar.header("➕ Add Expense")

amount = st.sidebar.number_input("Amount", min_value=0)
category = st.sidebar.selectbox("Category",
["Food","Travel","Shopping","Bills","Other"])
expense_date = st.sidebar.date_input("Date", date.today())

if st.sidebar.button("Add Expense"):
    st.session_state.expenses.append({
        "Amount": amount,
        "Category": category,
        "Date": expense_date
    })

# ---------- DATA ----------
if st.session_state.expenses:

    df = pd.DataFrame(st.session_state.expenses)

    total_spending = df["Amount"].sum()
    total_transactions = len(df)
    avg_spending = df["Amount"].mean()

    # ---------- KPI CARDS ----------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="card">
        <div class="metric">₹{total_spending}</div>
        <div class="label">Total Spending</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
        <div class="metric">{total_transactions}</div>
        <div class="label">Transactions</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card">
        <div class="metric">₹{round(avg_spending,2)}</div>
        <div class="label">Average Expense</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # ---------- CHARTS ----------
    col4, col5 = st.columns(2)

    with col4:
        st.subheader("Category Spending")
        pie = px.pie(df, names="Category", values="Amount", hole=0.4)
        st.plotly_chart(pie, use_container_width=True)

    with col5:
        st.subheader("Daily Spending")
        daily = df.groupby("Date")["Amount"].sum().reset_index()
        line = px.line(daily, x="Date", y="Amount", markers=True)
        st.plotly_chart(line, use_container_width=True)

    # ---------- TABLE ----------
    st.subheader("Recent Transactions")
    st.dataframe(df, use_container_width=True)

else:
    st.info("Add your first expense from the sidebar 👈")