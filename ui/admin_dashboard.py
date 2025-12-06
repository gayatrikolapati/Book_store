import streamlit as st
import requests

API = "http://127.0.0.1:8000"

# Import UI components
from ui.add_book_ui import show_add_book
from ui.edit_book_ui import show_edit_book
from ui.delete_book_ui import show_delete_book


def _fetch_stats():
    try:
        books = requests.get(f"{API}/books").json()
    except:
        books = []

    try:
        users = requests.get(f"{API}/users").json()
    except:
        users = []

    total_books = len(books)
    total_users = len(users)
    total_stock = sum(int(b["quantity"]) for b in books) if books else 0
    out_of_stock = sum(1 for b in books if int(b["quantity"]) == 0)

    return books, users, total_books, total_users, total_stock, out_of_stock



def show_admin_dashboard(API):
    if not st.session_state.get("is_admin", False):
        st.error("Admin access only.")
        return

    books, users, total_books, total_users, total_stock, out_of_stock = _fetch_stats()

    st.title("🛠️ Admin Dashboard")

    # ------------ TOP STATS ------------
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Books", total_books)
    c2.metric("Registered Users", total_users)
    c3.metric("Total Stock", total_stock)
    c4.metric("Out of Stock", out_of_stock)

    st.markdown("---")

    # ------------ TABS ------------
    tab_dash, tab_books, tab_users, tab_reports = st.tabs(
        ["Dashboard", "Books", "Users", "Reports"]
    )

    # ------------ DASHBOARD TAB ------------
    with tab_dash:
        st.subheader("Overview")
        st.write("Admin overview and charts will appear here.")

    # ------------ BOOKS TAB (THE ONE YOU WANT) ------------
    with tab_books:
        st.subheader("📘 Books — Admin Controls")

        action = st.selectbox(
            "Choose an action:",
            ["Add Book", "Edit Book", "Delete Book"]
        )

        if action == "Add Book":
            show_add_book(API)

        elif action == "Edit Book":
            show_edit_book(API)

        elif action == "Delete Book":
            show_delete_book(API)

    # ------------ USERS TAB ------------
    with tab_users:
        st.subheader("Users List")
        if users:
            for u in users:
                st.write(f"• {u['name']} — {u['email']} (Age: {u['age']})")
        else:
            st.info("No users registered yet.")

    # ------------ REPORTS TAB ------------
    with tab_reports:
        st.subheader("Reports")
        st.write("Add charts and reports here later.")

    # Logout button
    st.markdown("---")
    if st.button("Logout Admin"):
        st.session_state.logged_in = False
        st.session_state.is_admin = False
        st.session_state.user_name = None
        st.session_state.menu = "Home"
        st.rerun()
