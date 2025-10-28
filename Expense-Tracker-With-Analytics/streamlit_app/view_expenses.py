# View / visualize expenses page

# view_expenses.py
import streamlit as st
from utils import get_all_expenses, get_category_summary

def show_view_expenses():
    st.header("📊 View All Expenses")

    df = get_all_expenses()

    if df.empty:
        st.warning("No expenses found yet. Add some!")
        return

    st.dataframe(df, use_container_width=True)

    total = df["amount"].sum()
    st.subheader(f"💰 Total Spending: ₹{total:.2f}")

    st.divider()
    st.subheader("📈 Category-wise Summary")

    summary_df = get_category_summary()
    if not summary_df.empty:
        st.bar_chart(summary_df.set_index("category"))
    else:
        st.info("No summary data available yet.")