import streamlit as st


def show_home():
    st.title("🏠 Home")

    logged_in = st.session_state.get("logged_in", False)
    is_admin = st.session_state.get("is_admin", False)

    # Show login state
    if logged_in:
        role = "Admin" if is_admin else "User"
        name = st.session_state.get("user_name") or role
        st.success(f"Logged in as {role}: {name}")
    else:
        st.info("Use the sidebar to Register or Login to continue.")

    # If not logged in → stop
    if not logged_in:
        return

    # If admin → show admin instructions
    if is_admin:
        st.info("Go to **Admin Dashboard** from the sidebar to manage books and users.")
        return

    # ---------- USER DASHBOARD ----------
    st.subheader("Your Library")

    col1, col2 = st.columns(2)

    wishlist = st.session_state.get("wishlist", [])
    purchases = st.session_state.get("purchases", [])
    borrowed = st.session_state.get("borrowed", [])
    activity = st.session_state.get("activity", [])

    # ---------------- LEFT COLUMN ----------------
    with col1:
        st.markdown("### ⭐ Wishlist")
        if not wishlist:
            st.write("No books in wishlist yet.")
        else:
            for item in wishlist:
                st.write(f"• {item.get('title')} (₹{item.get('price')})")

        st.markdown("### 📦 Purchases (Simulation)")
        if not purchases:
            st.write("You haven't purchased any books yet.")
        else:
            for p in purchases:
                st.write(f"• {p['title']} – ₹{p['price']}")

    # ---------------- RIGHT COLUMN ----------------
    with col2:
        st.markdown("### 📚 Borrowed Books")
        if not borrowed:
            st.write("No active borrowed books.")
        else:
            for b in borrowed:
                st.write(f"• {b['title']}")

        st.markdown("### 🕒 Recent Activity")
        if not activity:
            st.write("No recent actions.")
        else:
            for a in reversed(activity[-10:]):  # last 10 actions
                st.write(f"- {a}")
