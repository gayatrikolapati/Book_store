import streamlit as st
import requests

def show_edit_book(API):

    st.subheader("✏️ Edit Book")

    # Fetch books list
    books = requests.get(f"{API}/books").json()

    if not books:
        st.info("No books available to edit.")
        return

    # Make dropdown choices: "Title (Author) - ID"
    book_options = {
        f"{b['title']} ({b['author']})  —  ID: {b['id']}": b['id']
        for b in books
    }

    selected_label = st.selectbox("Select a book to edit:", list(book_options.keys()))
    selected_id = book_options[selected_label]

    # Fetch book details
    book = next(b for b in books if b["id"] == selected_id)

    # Editable fields
    title = st.text_input("Title", book["title"])
    author = st.text_input("Author", book["author"])
    price = st.number_input("Price", value=float(book["price"]))
    quantity = st.number_input("Quantity", value=int(book["quantity"]))

    if st.button("Update Book"):
        res = requests.put(
            f"{API}/books/{selected_id}",
            data={
                "title": title,
                "author": author,
                "price": price,
                "quantity": quantity
            }
        )

        if res.status_code == 200:
            st.success("Book updated successfully!")
            st.rerun()
        else:
            st.error(res.json().get("detail", "Failed to update book"))
