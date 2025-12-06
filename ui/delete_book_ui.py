import streamlit as st
import requests

def show_delete_book(API):

    st.subheader("🗑️ Delete Book")

    # Fetch books list
    books = requests.get(f"{API}/books").json()

    if not books:
        st.info("No books available to delete.")
        return

    # Dropdown options
    book_options = {
        f"{b['title']} ({b['author']})  —  ID: {b['id']}": b['id']
        for b in books
    }

    selected_label = st.selectbox("Select a book to delete:", list(book_options.keys()))
    selected_id = book_options[selected_label]

    st.warning(f"You are about to delete: **{selected_label}**")

    if st.button("Delete Book"):
        res = requests.delete(f"{API}/books/{selected_id}")

        if res.status_code == 200:
            st.success("Book deleted successfully!")
            st.rerun()
        else:
            st.error(res.json().get("detail", "Failed to delete book"))
