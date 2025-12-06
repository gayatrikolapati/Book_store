import streamlit as st
import requests

# ❗ REMOVE HARDCODED API = "127.0.0.1"


from ui.add_book_ui import show_add_book
from ui.edit_book_ui import show_edit_book
from ui.delete_book_ui import show_delete_book


# -------------------------------------------------------
# Fetching Stats — FIXED to use API passed from main
# -------------------------------------------------------
def _fetch_stats(API):
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



# -------------------------------------------------------
# ADMIN DASHBOARD
# -------------------------------------------------------
def show_admin_dashboard(API):

    if not st.session_state.get("is_admin", False):
        st.error("❌ Access denied. Admins only.")
        return

    st.title("🛠️ Admin Dashboard")

    # Fetch stats — FIXED
    books, users, total_books, total_users, total_stock, out_of_stock = _fetch_stats(API)

    # ---------------- TOP STATISTICS ----------------
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Books", total_books)
    c2.metric("Registered Users", total_users)
    c3.metric("Total Stock", total_stock)
    c4.metric("Out of Stock", out_of_stock)

    st.markdown("---")

    section = st.sidebar.radio(
        "📌 Select Section",
        ["Books", "Users", "Analytics"],
        index=0,
        key="admin_section"
    )

    # ============================================================
    # 🔵 BOOKS SECTION → ADD / EDIT / DELETE
    # ============================================================
    if section == "Books":
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

    # ============================================================
    # 🔵 USERS SECTION — SHOW ALL USERS
    # ============================================================
    if section == "Users":
        st.subheader("👥 Registered Users")

        try:
            users = requests.get(f"{API}/users").json()
        except:
            users = []

        if not users:
            st.info("No users registered yet.")
        else:
            for u in users:
                st.markdown(
                    f"**Name:** {u['name']}<br>"
                    f"**Email:** {u['email']}<br>"
                    f"**Age:** {u['age']}<br><hr>",
                    unsafe_allow_html=True
                )

    # ============================================================
    # 🔵 ANALYTICS SECTION
    # ============================================================
    if section == "Analytics":
        st.subheader("📊 Analytics Dashboard")
        st.info("Future feature: charts, trends, reports, usage analytics.")

    # ---------------- LOGOUT BUTTON ----------------
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.is_admin = False
        st.session_state.user_name = None
        st.session_state.menu = "Home"
        st.rerun()
