import streamlit as st
import requests


# ==================================================
# CONFIGURATION
# ==================================================

API_URL = "http://127.0.0.1:8000"


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Meher Library Management",
    page_icon="📚",
    layout="wide"
)


# ==================================================
# TITLE
# ==================================================

st.title("📚 Meher Library Management System")
st.write("Manage your books easily using the Library Management System.")


# ==================================================
# SIDEBAR MENU
# ==================================================

st.sidebar.title("📖 Menu")

menu = st.sidebar.radio(
    "Choose an option",
    [
        "🏠 Home",
        "➕ Add Book",
        "📚 View Books",
        "🔍 Search Book",
        "✏️ Update Book",
        "🗑️ Delete Book"
    ]
)


# ==================================================
# HOME
# ==================================================

if menu == "🏠 Home":

    st.header("Welcome to Meher Library 📚")

    st.success("FastAPI Backend is connected!")

    col1, col2, col3 = st.columns(3)

    try:
        response = requests.get(f"{API_URL}/books")

        if response.status_code == 200:
            books = response.json()

            with col1:
                st.metric("📚 Total Books", len(books))

            with col2:
                available_books = sum(
                    1 for book in books
                    if book["available"]
                )
                st.metric("✅ Available", available_books)

            with col3:
                unavailable_books = sum(
                    1 for book in books
                    if not book["available"]
                )
                st.metric("❌ Unavailable", unavailable_books)

        else:
            st.error("Could not connect to FastAPI.")

    except requests.exceptions.ConnectionError:
        st.error(
            "FastAPI server is not running. "
            "Please start Uvicorn first."
        )


# ==================================================
# ADD BOOK
# ==================================================

elif menu == "➕ Add Book":

    st.header("➕ Add New Book")

    title = st.text_input("📖 Book Title")
    author = st.text_input("✍️ Author")
    isbn = st.text_input("🔢 ISBN")
    category = st.text_input("📂 Category")

    if st.button("➕ Add Book", type="primary"):

        if title and author and isbn and category:

            try:

                response = requests.post(
                    f"{API_URL}/books",
                    json={
                        "title": title,
                        "author": author,
                        "isbn": isbn,
                        "category": category
                    }
                )

                if response.status_code == 200:

                    st.success("🎉 Book added successfully!")

                    book = response.json()

                    st.write("Book ID:", book["id"])

                elif response.status_code == 400:

                    st.warning(
                        "⚠️ A book with this ISBN already exists."
                    )

                else:

                    st.error(
                        f"Something went wrong. "
                        f"Status: {response.status_code}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ FastAPI server is not running."
                )

        else:

            st.warning(
                "⚠️ Please fill all fields."
            )


# ==================================================
# VIEW BOOKS
# ==================================================

elif menu == "📚 View Books":

    st.header("📚 All Books")

    try:

        response = requests.get(
            f"{API_URL}/books"
        )

        if response.status_code == 200:

            books = response.json()

            if books:

                for book in books:

                    with st.container(border=True):

                        col1, col2 = st.columns([3, 1])

                        with col1:

                            st.subheader(
                                f"📖 {book['title']}"
                            )

                            st.write(
                                f"**Author:** {book['author']}"
                            )

                            st.write(
                                f"**ISBN:** {book['isbn']}"
                            )

                            st.write(
                                f"**Category:** {book['category']}"
                            )

                        with col2:

                            st.write(
                                f"**Book ID:** {book['id']}"
                            )

                            if book["available"]:
                                st.success("✅ Available")
                            else:
                                st.error("❌ Not Available")

            else:

                st.info(
                    "📚 No books found in the library."
                )

        else:

            st.error("Could not fetch books.")

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ FastAPI server is not running."
        )


# ==================================================
# SEARCH BOOK
# ==================================================

elif menu == "🔍 Search Book":

    st.header("🔍 Search Book")

    book_id = st.number_input(
        "Enter Book ID",
        min_value=1,
        step=1
    )

    if st.button("🔍 Search"):

        try:

            response = requests.get(
                f"{API_URL}/books/{book_id}"
            )

            if response.status_code == 200:

                book = response.json()

                st.success("Book found! 🎉")

                st.subheader(
                    f"📖 {book['title']}"
                )

                st.write(
                    f"**Book ID:** {book['id']}"
                )

                st.write(
                    f"**Author:** {book['author']}"
                )

                st.write(
                    f"**ISBN:** {book['isbn']}"
                )

                st.write(
                    f"**Category:** {book['category']}"
                )

                if book["available"]:
                    st.success("✅ Available")
                else:
                    st.error("❌ Not Available")

            elif response.status_code == 404:

                st.error("❌ Book not found.")

            else:

                st.error("Something went wrong.")

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ FastAPI server is not running."
            )


# ==================================================
# UPDATE BOOK
# ==================================================

elif menu == "✏️ Update Book":

    st.header("✏️ Update Book")

    book_id = st.number_input(
        "Book ID",
        min_value=1,
        step=1
    )

    title = st.text_input("📖 New Book Title")
    author = st.text_input("✍️ New Author")
    isbn = st.text_input("🔢 New ISBN")
    category = st.text_input("📂 New Category")

    if st.button("✏️ Update Book", type="primary"):

        if title and author and isbn and category:

            try:

                response = requests.put(
                    f"{API_URL}/books/{book_id}",
                    json={
                        "title": title,
                        "author": author,
                        "isbn": isbn,
                        "category": category
                    }
                )

                if response.status_code == 200:

                    st.success(
                        "🎉 Book updated successfully!"
                    )

                elif response.status_code == 404:

                    st.error(
                        "❌ Book not found."
                    )

                elif response.status_code == 400:

                    st.warning(
                        "⚠️ Another book already uses this ISBN."
                    )

                else:

                    st.error(
                        f"Something went wrong. "
                        f"Status: {response.status_code}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ FastAPI server is not running."
                )

        else:

            st.warning(
                "⚠️ Please fill all fields."
            )


# ==================================================
# DELETE BOOK
# ==================================================

elif menu == "🗑️ Delete Book":

    st.header("🗑️ Delete Book")

    book_id = st.number_input(
        "Enter Book ID",
        min_value=1,
        step=1
    )

    if st.button(
        "🗑️ Delete Book",
        type="primary"
    ):

        try:

            response = requests.delete(
                f"{API_URL}/books/{book_id}"
            )

            if response.status_code == 200:

                st.success(
                    "✅ Book deleted successfully!"
                )

            elif response.status_code == 404:

                st.error(
                    "❌ Book not found."
                )

            else:

                st.error(
                    f"Something went wrong. "
                    f"Status: {response.status_code}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ FastAPI server is not running."
            )
