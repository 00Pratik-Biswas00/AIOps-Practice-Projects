import streamlit as st
import pandas as pd
from utils import get_all_expenses, get_category_summary, API_URL
from edit_expense import edit_expense_form
from delete_expense import handle_delete_expense
from datetime import datetime
import requests

def show_view_expenses():
    st.subheader("📊 View & Manage Expenses")

    current_month = datetime.now().strftime("%Y-%m")
    df_full = get_all_expenses()

    # ✅ Filter current month data
    df_full = df_full[df_full["date"].str.startswith(current_month)]

    if df_full.empty:
        st.warning("No expenses found yet. Add some!")
        return

    # ✅ Keep only necessary columns
    expected_cols = ["date", "category", "amount", "note", "month_category", "date_id"]
    df_full = df_full[[c for c in expected_cols if c in df_full.columns]]

    # ✅ Sort by date (latest first)
    df_full["date"] = pd.to_datetime(df_full["date"], errors="coerce")
    df_full = df_full.sort_values(by="date", ascending=False).reset_index(drop=True)

    st.write("### 💸 Expense List ")

    # ✅ Table headers
    header_cols = st.columns([2, 2, 2, 3, 1, 1])
    headers = ["Date", "Category", "Amount", "Note", "Edit", "Delete"]
    for col, name in zip(header_cols, headers):
        col.markdown(f"**{name}**")

    # ✅ Track which expense is being edited
    if "edit_index" not in st.session_state:
        st.session_state.edit_index = None

    editing_active = st.session_state.edit_index is not None

    # ✅ Loop through sorted rows
    for i, row in df_full.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 3, 1, 1])

        # ✅ Format date nicely
        formatted_date = row.get("date").strftime("%Y-%m-%d") if pd.notnull(row.get("date")) else "-"
        col1.write(formatted_date)
        col2.write(row.get("category", "-"))
        col3.write(f"₹{row.get('amount', 0):.2f}")
        col4.write(row.get("note", "-"))

        # ✅ Disable edit/delete buttons when form is open
        edit_disabled = editing_active and st.session_state.edit_index != i
        delete_disabled = editing_active

        edit_btn = col5.button("✏️", key=f"edit_{i}", disabled=edit_disabled)
        del_btn = col6.button("🗑️", key=f"del_{i}", disabled=delete_disabled)

        # --- When Edit button is clicked ---
        if edit_btn:
            st.session_state.edit_index = i
            st.rerun()

        # --- When Delete button is clicked ---
        if del_btn:
            handle_delete_expense(row)
            st.rerun()

        # --- Show edit form if this row is selected ---
        if st.session_state.edit_index == i:
            edit_expense_form(row, i)  # ✅ Pass both arguments correctly

# --- Summary ---
    total = df_full["amount"].sum()
    st.subheader(f"💰 Total Spending: ₹{total:.2f}")
 
    st.divider()
    st.subheader("📈 Category-wise Summary (Current Month)")
 
    summary_df = get_category_summary()
    if not summary_df.empty:
        st.dataframe(summary_df, use_container_width=True)
    else:
        st.info("No summary data available yet for this month.")

        # ---------------- Download previous month backup ----------------
    st.divider()
    st.subheader("📥 Download Previous Backup Data")

    # Option A: quick static list (works now)
    months_available = ["2025-09", "2025-10", "2025-11"]  # <-- you can update or generate dynamically later
    selected_month = st.selectbox("Select Backup Month", months_available, index=0)

    if st.button("Download Backup 🚀"):
        api_url = f"{API_URL}/download?month={selected_month}"
        response = requests.get(api_url)

        if response.status_code == 200:
            url = response.json().get("download_url")
            st.markdown(f"✅ Click to download:\n\n👉 [Download File]({url})")
        else:
            st.error("⚠️ Backup not found for that month!")
