import streamlit as st
import requests

API = "http://127.0.0.1:8000"


def show_books(admin_override=False):
    """Main Books Page – Works for User & Admin Mode"""

    # Fetch books
    try:
        books = requests.get(f"{API}/books").json()
    except:
        st.error("Could not fetch books from API.")
        return

    st.title("📚 Books")

    # Search + sort
    search = st.text_input("Search by title or author")

    sort_by = st.selectbox(
        "Sort by",
        ["Title", "Author", "Price", "Quantity"]
    )

    # Apply filters
    if search:
        q = search.lower()
        books = [b for b in books if q in b["title"].lower() or q in b["author"].lower()]

    if sort_by == "Title":
        books.sort(key=lambda x: x["title"])
    elif sort_by == "Author":
        books.sort(key=lambda x: x["author"])
    elif sort_by == "Price":
        books.sort(key=lambda x: float(x["price"]))
    elif sort_by == "Quantity":
        books.sort(key=lambda x: int(x["quantity"]))

    # Detect admin mode
    is_admin = admin_override or st.session_state.get("is_admin", False)

    # Show each book
    for book in books:
        st.markdown("---")
        st.subheader(f"{book['title']}")

        st.write(f"**Author:** {book['author']}")
        st.write(f"**Price:** ₹{book['price']}")
        st.write(f"**In Stock:** {book['quantity']}")

        # ---------------- ADMIN CONTROLS ----------------
        if is_admin:
      

            col1, col2 = st.columns(2)

            # -------- EDIT BUTTON --------
            with col1:
                if st.button(f"Edit {book['id']}"):
                    st.session_state.edit_book_id = book["id"]
                    st.session_state.menu = "Admin Dashboard"
                    st.session_state.admin_action = "Edit"
                    st.rerun()

            # -------- DELETE BUTTON --------
            with col2:
                if st.button(f"Delete {book['id']}"):
                    delete_book(book["id"])
                    st.success("Book deleted!")
                    st.rerun()


def delete_book(book_id):
    """Function to call API delete"""
    try:
        res = requests.delete(f"{API}/books/{book_id}")
        return res.status_code == 200
    except:
        return False
