import streamlit as st
import requests


def show_register(API):

    st.title("📝 Register (with OTP verification)")

    if "otp_sent" not in st.session_state:
        st.session_state.otp_sent = False
    if "reg_data" not in st.session_state:
        st.session_state.reg_data = {}

    # ---------- STEP 1: USER DETAILS ----------
    if not st.session_state.otp_sent:
        with st.form("register_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            age = st.number_input("Age", min_value=1, max_value=120)
            password = st.text_input("Password", type="password")

            submit = st.form_submit_button("Request OTP")

        if submit:
            if not name or not email or not password:
                st.error("All fields are required")
                return

            user_data = {
                "name": name,
                "email": email,
                "age": int(age),
                "password": password,
            }

            # Validate user details with backend
            try:
                v = requests.post(f"{API}/validate-user", json=user_data)
            except Exception:
                st.error("Backend not reachable.")
                return

            if v.status_code != 200:
                detail = v.json().get("detail", "Validation error")
                if isinstance(detail, list):
                    detail = detail[0].get("msg", "Validation error")
                st.error(detail)
                return

            # Request OTP
            try:
                r = requests.post(f"{API}/request-otp", params={"email": email})
            except Exception:
                st.error("Backend error while requesting OTP.")
                return

            if r.status_code == 200:
                st.success("OTP sent successfully!")
                st.session_state.otp_sent = True
                st.session_state.reg_data = user_data
                st.rerun()
            else:
                st.error(r.json().get("detail", "Failed to send OTP"))

    # ---------- STEP 2: OTP VERIFY ----------
    else:
        reg_data = st.session_state.reg_data
        st.info(f"OTP sent to {reg_data['email']}")

        otp = st.text_input("Enter OTP")

        col1, col2 = st.columns(2)
        verify_btn = col1.button("Verify OTP")
        change_btn = col2.button("Change Details")

        if change_btn:
            st.session_state.otp_sent = False
            st.session_state.reg_data = {}
            st.rerun()

        if verify_btn:
            try:
                r = requests.post(
                    f"{API}/verify-otp",
                    json=reg_data,
                    params={"otp": otp}
                )
            except Exception:
                st.error("Backend error while verifying OTP.")
                return

            if r.status_code == 200:
                st.success("Registration successful! You can now login.")
                st.session_state.otp_sent = False
                st.session_state.reg_data = {}
                st.rerun()
            else:
                st.error(r.json().get("detail", "Invalid OTP"))
