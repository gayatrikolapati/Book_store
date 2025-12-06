import streamlit as st
import requests

def show_add_book(API):
    st.subheader("➕ Add a New Book")

    title = st.text_input("Book Title")
    author = st.text_input("Author")
    price = st.number_input("Price", min_value=0.0)
    quantity = st.number_input("Quantity", min_value=0)

    if st.button("Add Book"):
        data = {
            "admin_username": "Gayatri",
            "admin_password": "Honey@123",
            "title": title,
            "author": author,
            "price": price,
            "quantity": quantity
        }

        r = requests.post(f"{API}/books", data=data)
        
        if r.status_code == 200:
            st.success("Book added successfully!")
        else:
            st.error(r.json().get("detail"))
