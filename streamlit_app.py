import streamlit as st
from ui.home import show_home
from ui.register_ui import show_register
from ui.login_ui import show_login
from ui.books_ui import show_books
from ui.admin_ui import show_admin_dashboard

# ---------------- GLOBAL API URL (VERY IMPORTANT) ----------------
API = "https://book-store-stvm.onrender.com"

st.set_page_config(
    page_title="Bookstore System",
    page_icon="📚",
    layout="wide"
)

# ---------------- SESSION STATE SETUP ----------------
if "menu" not in st.session_state:
    st.session_state.menu = "Home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

if "user_name" not in st.session_state:
    st.session_state.user_name = None

# User data storage
if "wishlist" not in st.session_state:
    st.session_state.wishlist = []
if "purchases" not in st.session_state:
    st.session_state.purchases = []
if "borrowed" not in st.session_state:
    st.session_state.borrowed = []
if "ratings" not in st.session_state:
    st.session_state.ratings = {}
if "activity" not in st.session_state:
    st.session_state.activity = []


# ---------------- SIDEBAR NAVIGATION ----------------
base_menus = ["Home", "Register", "Login", "Books", "Admin Dashboard"]

# Hide Admin Dashboard if not an admin
menus = base_menus.copy()
if not st.session_state.is_admin:
    menus.remove("Admin Dashboard")

choice = st.sidebar.radio(
    "Navigate",
    menus,
    index=menus.index(st.session_state.menu) if st.session_state.menu in menus else 0,
)

st.session_state.menu = choice


# ---------------- PAGE ROUTING ----------------
if choice == "Home":
    show_home()

elif choice == "Register":
    show_register()

elif choice == "Login":
    show_login()

elif choice == "Books":
    show_books(API)    # FIXED: API added

elif choice == "Admin Dashboard":
    show_admin_dashboard(API)   # FIXED: API passed correctly

