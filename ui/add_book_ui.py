import streamlit as st
import requests

def show_add_book(API):
    st.subheader("➕ Add a New Book")

    title = st.text_input("Book Title")
    author = st.text_input("Author")
    price = st.number_input("Price", min_value=0.0, step=0.1)
    quantity = st.number_input("Quantity", min_value=0, step=1)

    if st.button("Add Book"):
        data = {
            "admin_username": "Gayatri",
            "admin_password": "Honey@123",
            "title": title,
            "author": author,
            "price": float(price),
            "quantity": int(quantity)
        }

        response = requests.post(f"{API}/books", json=data)

        if response.status_code in (200, 201):
            st.success("Book added successfully!")
        else:
            try:
                st.error(response.json().get("detail"))
            except:
                st.error("Unknown error")
