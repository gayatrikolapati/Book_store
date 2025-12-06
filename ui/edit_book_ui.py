import streamlit as st
import requests


def show_edit_book(API):

    st.subheader("✏️ Edit Book")

    # Fetch books list safely
    try:
        books = requests.get(f"{API}/books").json()
    except:
        st.error("Failed to fetch books from backend.")
        return

    if not books:
        st.info("No books available to edit.")
        return

    # Dropdown: "Title (Author) — ID"
    book_options = {
        f"{b['title']} ({b['author']}) — ID: {b['id']}": b['id']
        for b in books
    }

    selected_label = st.selectbox("Select a book to edit:", list(book_options.keys()))
    selected_id = book_options[selected_label]

    # Fetch correct book entry
    book = next(b for b in books if b["id"] == selected_id)

    # Editable fields
    title = st.text_input("Title", book["title"])
    author = st.text_input("Author", book["author"])
    price = st.number_input("Price", value=float(book["price"]))
    quantity = st.number_input("Quantity", value=int(book["quantity"]))

    if st.button("Update Book"):
        update_data = {
            "title": title,
            "author": author,
            "price": price,
            "quantity": quantity
        }

        try:
            # FIXED: sending JSON instead of form-data
            res = requests.put(f"{API}/books/{selected_id}", json=update_data)
        except:
            st.error("Server error. Could not update book.")
            return

        if res.status_code == 200:
            st.success("Book updated successfully!")
            st.rerun()
        else:
            st.error(res.json().get("detail", "Failed to update book"))
