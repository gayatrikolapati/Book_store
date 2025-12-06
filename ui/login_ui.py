import streamlit as st
import requests

API = "http://127.0.0.1:8000"

def show_login():

    st.title("🔐 Login Portal")

    # --------------------------------------------------
    # STEP 1: LET USER CHOOSE LOGIN TYPE
    # --------------------------------------------------
    login_choice = st.selectbox(
        "Choose Login Type:",
        ["Select", "User Login", "Admin Login"]
    )

    st.write("---")

    # ==================================================
    # =============== USER LOGIN FORM ==================
    # ==================================================
    if login_choice == "User Login":

        st.subheader("👤 User Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login as User"):
            if not email or not password:
                st.error("Please enter both email and password.")
                return

            # Try to login through backend
            try:
                r = requests.post(
                    f"{API}/login",
                    params={"email": email, "password": password}
                )

                if r.status_code != 200:
                    st.error(r.json().get("detail", "Invalid login"))
                    return

                data = r.json()

                # ✔ Login success
                st.session_state.logged_in = True
                st.session_state.is_admin = False
                st.session_state.user_name = data.get("name")

                st.success("User login successful!")
                st.session_state.menu = "Home"
                st.rerun()

            except Exception as e:
                st.error(f"Server error: {e}")

    # ==================================================
    # =============== ADMIN LOGIN FORM =================
    # ==================================================
    elif login_choice == "Admin Login":

        st.subheader("🛠️ Admin Login")

        username = st.text_input("Admin Username")
        password = st.text_input("Admin Password", type="password")

        if st.button("Login as Admin"):

            # ✔ Use SAME admin credentials from FastAPI
            if username == "Gayatri" and password == "H":
                st.session_state.logged_in = True
                st.session_state.is_admin = True
                st.session_state.user_name = "Admin"

                st.success("Admin login successful!")
                st.session_state.menu = "Admin Dashboard"
                st.rerun()
            else:
                st.error("Invalid admin credentials.")

    # ==================================================
    # IF LOGIN TYPE NOT SELECTED
    # ==================================================
    else:
        st.info("Please choose User Login or Admin Login.")
