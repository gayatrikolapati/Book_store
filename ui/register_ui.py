import streamlit as st
import requests

API = "http://127.0.0.1:8000"

def show_register():
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
            age = st.number_input("Age", min_value=0, max_value=120)
            password = st.text_input("Password", type="password")

            submit = st.form_submit_button("Request OTP")

        if submit:
            if not name or not email or not password or age == 0:
                st.error("All fields are required")
                return

            user_data = {
                "name": name,
                "email": email,
                "age": int(age),
                "password": password,
            }

            # validate with backend
            try:
                v = requests.post(f"{API}/validate-user", json=user_data)
            except Exception:
                st.error("Backend not reachable. Start FastAPI server.")
                return

            if v.status_code != 200:
                try:
                    detail = v.json().get("detail")
                    if isinstance(detail, list) and detail:
                        msg = detail[0].get("msg", "Validation error")
                    else:
                        msg = str(detail)
                except Exception:
                    msg = "Validation failed"
                st.error(msg)
                return

            # request OTP
            try:
                r = requests.post(f"{API}/request-otp", params={"email": email})
            except Exception:
                st.error("Backend error while requesting OTP.")
                return

            if r.status_code == 200:
                st.success("OTP sent to your email.")
                st.session_state.otp_sent = True
                st.session_state.reg_data = user_data
                st.rerun()
            else:
                try:
                    msg = r.json().get("detail", "Failed to send OTP")
                except Exception:
                    msg = "Failed to send OTP"
                st.error(msg)

    # ---------- STEP 2: OTP VERIFY ----------
    else:
        reg_data = st.session_state.reg_data
        st.info(f"OTP sent to {reg_data['email']}")

        otp = st.text_input("Enter OTP")

        col1, col2 = st.columns(2)
        with col1:
            verify_btn = st.button("Verify OTP")
        with col2:
            change_btn = st.button("Change Details")

        if change_btn:
            st.session_state.otp_sent = False
            st.session_state.reg_data = {}
            st.rerun()

        if verify_btn:
            try:
                r = requests.post(
                    f"{API}/verify-otp",
                    json=reg_data,
                    params={"otp": otp},
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
                try:
                    msg = r.json().get("detail", "Invalid OTP")
                except Exception:
                    msg = "Server error while verifying OTP"
                st.error(msg)
