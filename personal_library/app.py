
import streamlit as st
import json

# File path for storing books
FILE_PATH = "my_library.json"

# Load books from JSON
def load_books():
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save books to JSON
def save_books(books):
    with open(FILE_PATH, "w") as file:
        json.dump(books, file, indent=4)

# Add new book
def add_book(title, author, year, genre, read_status):
    books = load_books()
    new_book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read_status": read_status
    }
    books.append(new_book)
    save_books(books)

# Remove book by title
def remove_book(title_to_remove):
    books = load_books()
    updated_books = [book for book in books if book['title'].lower() != title_to_remove.lower()]
    save_books(updated_books)

# Search books by query
def search_books(query):
    books = load_books()
    return [book for book in books if query.lower() in book['title'].lower() or query.lower() in book['author'].lower()]

# Display books
def display_books(books):
    if books:
        for i, book in enumerate(books, 1):
            status = "✔️ Read" if book['read_status'] else "❌ Unread"
            st.write(f"{i}. **{book['title']}** by {book['author']} ({book['year']}) - Genre: {book['genre']} - {status}")
    else:
        st.info("Your library is empty. Add some books! 📚")

# Main App
def main():
    st.set_page_config(page_title="Library Manager", layout="wide")

    # Custom Styling
    st.markdown("""
        <style>
        .stApp { background-color: #fdfcfb; color: #1e1e1e; }
        .stButton>button {
            background-color: #6c63ff;
            color: white;
            border-radius: 10px;
            padding: 10px 18px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #5548c8;
        }
        .stTextInput input, .stNumberInput input, .stSelectbox select {
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
        }
        .stSidebar { background-color: #f0f4ff; }
        </style>
    """, unsafe_allow_html=True)

    st.title("📚 **Library Manager** 📚")

    menu = ["🏠 Home", "➕ Add a Book", "🔍 Search Books", "📖 View Library", "🗑️ Remove a Book"]
    choice = st.sidebar.radio("Select an option", menu)

    if choice == "🏠 Home":
        st.header("Welcome to Your Personal Library! ✨")
        st.write("Organize your reading journey with ease using this personal library manager.")

    elif choice == "➕ Add a Book":
        st.header("Add a New Book 📖")
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=1000, max_value=9999)
        genre = st.text_input("Genre")
        read_status = st.selectbox("Have you read this book?", ["Yes", "No"])

        if st.button("Add Book ➕"):
            if title and author and genre:
                add_book(title, author, year, genre, read_status == "Yes")
                st.success(f"Book '{title}' added successfully! 🎉")
            else:
                st.error("Please fill in all fields.")

    elif choice == "🔍 Search Books":
        st.header("Search for a Book 🔍")
        query = st.text_input("Enter title or author:")
        if query:
            results = search_books(query)
            if results:
                st.success(f"Found {len(results)} book(s):")
                display_books(results)
            else:
                st.warning("No books matched your search.")

    elif choice == "📖 View Library":
        st.header("Your Library 📚")
        books = load_books()
        if books:
            st.success(f"You have {len(books)} book(s) in your library:")
            display_books(books)
        else:
            st.info("Library is empty.")

    elif choice == "🗑️ Remove a Book":
        st.header("Remove a Book from Your Library 🗑️")
        books = load_books()
        if books:
            titles = [book['title'] for book in books]
            selected = st.selectbox("Select a book to remove:", titles)
            if st.button("Remove Book ❌"):
                remove_book(selected)
                st.success(f"'{selected}' has been removed.")
        else:
            st.info("No books to remove.")

    st.sidebar.markdown("----")
    st.sidebar.markdown("Made with ❤️ by Malik Wahab")
    st.sidebar.write("Give your feedback anytime!")

if __name__ == "__main__":
    main()
