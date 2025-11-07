import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# Page configuration
st.set_page_config(
    page_title="Library Book Management",
    page_icon="📚",
    layout="wide"
)

# File path for CSV
CSV_FILE = "books.csv"

def load_data():
    """Load book data from CSV file"""
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        # Create initial dataframe if file doesn't exist
        initial_data = {
            'book_id': [1, 2, 3, 4, 5],
            'title': ['The Great Gatsby', 'To Kill a Mockingbird', '1984', 
                     'Pride and Prejudice', 'The Catcher in the Rye'],
            'author': ['F. Scott Fitzgerald', 'Harper Lee', 'George Orwell', 
                      'Jane Austen', 'J.D. Salinger'],
            'isbn': ['9780743273565', '9780061120084', '9780451524935', 
                    '9780141439518', '9780316769174'],
            'status': ['Available', 'Borrowed', 'Available', 'Borrowed', 'Available'],
            'borrower': ['', 'John Doe', '', 'Jane Smith', ''],
            'due_date': ['', '2024-02-15', '', '2024-02-20', '']
        }
        df = pd.DataFrame(initial_data)
        df.to_csv(CSV_FILE, index=False)
        return df

def save_data(df):
    """Save book data to CSV file"""
    df.to_csv(CSV_FILE, index=False)

def borrow_book(df, book_id, borrower_name, days=14):
    """Borrow a book"""
    due_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
    df.loc[df['book_id'] == book_id, 'status'] = 'Borrowed'
    df.loc[df['book_id'] == book_id, 'borrower'] = borrower_name
    df.loc[df['book_id'] == book_id, 'due_date'] = due_date
    save_data(df)
    return df

def return_book(df, book_id):
    """Return a book"""
    df.loc[df['book_id'] == book_id, 'status'] = 'Available'
    df.loc[df['book_id'] == book_id, 'borrower'] = ''
    df.loc[df['book_id'] == book_id, 'due_date'] = ''
    save_data(df)
    return df

def add_new_book(df, title, author, isbn):
    """Add a new book to the library"""
    new_id = df['book_id'].max() + 1 if not df.empty else 1
    new_book = {
        'book_id': new_id,
        'title': title,
        'author': author,
        'isbn': isbn,
        'status': 'Available',
        'borrower': '',
        'due_date': ''
    }
    df = pd.concat([df, pd.DataFrame([new_book])], ignore_index=True)
    save_data(df)
    return df

def main():
    st.title("📚 Library Book Management System")
    
    # Load data
    df = load_data()
    
    # Sidebar for actions
    st.sidebar.title("Library Actions")
    action = st.sidebar.selectbox(
        "Choose Action",
        ["View Books", "Borrow Book", "Return Book", "Add New Book", "Search Books"]
    )
    
    if action == "View Books":
        st.header("📖 All Books in Library")
        
        # Display statistics
        col1, col2, col3 = st.columns(3)
        total_books = len(df)
        available_books = len(df[df['status'] == 'Available'])
        borrowed_books = len(df[df['status'] == 'Borrowed'])
        
        col1.metric("Total Books", total_books)
        col2.metric("Available Books", available_books)
        col3.metric("Borrowed Books", borrowed_books)
        
        # Display books in a table
        st.dataframe(df, use_container_width=True)
        
    elif action == "Borrow Book":
        st.header("📥 Borrow a Book")
        
        # Filter available books
        available_books = df[df['status'] == 'Available']
        
        if available_books.empty:
            st.warning("No books available for borrowing.")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                selected_book = st.selectbox(
                    "Select Book to Borrow",
                    available_books.apply(
                        lambda x: f"{x['title']} by {x['author']} (ID: {x['book_id']})", 
                        axis=1
                    )
                )
                book_id = int(selected_book.split("(ID: ")[1].replace(")", ""))
                
            with col2:
                borrower_name = st.text_input("Borrower Name")
                borrow_days = st.slider("Borrow for (days)", 1, 30, 14)
            
            if st.button("Borrow Book"):
                if borrower_name.strip():
                    df = borrow_book(df, book_id, borrower_name, borrow_days)
                    st.success(f"Book borrowed successfully! Due date: {(datetime.now() + timedelta(days=borrow_days)).strftime('%Y-%m-%d')}")
                    st.rerun()
                else:
                    st.error("Please enter borrower name.")
    
    elif action == "Return Book":
        st.header("📤 Return a Book")
        
        # Filter borrowed books
        borrowed_books = df[df['status'] == 'Borrowed']
        
        if borrowed_books.empty:
            st.warning("No books to return.")
        else:
            selected_book = st.selectbox(
                "Select Book to Return",
                borrowed_books.apply(
                    lambda x: f"{x['title']} by {x['author']} - Borrowed by: {x['borrower']} (ID: {x['book_id']})", 
                    axis=1
                )
            )
            book_id = int(selected_book.split("(ID: ")[1].replace(")", ""))
            
            if st.button("Return Book"):
                df = return_book(df, book_id)
                st.success("Book returned successfully!")
                st.rerun()
    
    elif action == "Add New Book":
        st.header("➕ Add New Book")
        
        with st.form("add_book_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Book Title")
                author = st.text_input("Author")
            
            with col2:
                isbn = st.text_input("ISBN")
            
            submitted = st.form_submit_button("Add Book")
            
            if submitted:
                if title and author and isbn:
                    df = add_new_book(df, title, author, isbn)
                    st.success("Book added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all fields.")
    
    elif action == "Search Books":
        st.header("🔍 Search Books")
        
        search_type = st.radio("Search by:", ["Title", "Author", "ISBN"])
        search_query = st.text_input("Enter search term")
        
        if search_query:
            if search_type == "Title":
                results = df[df['title'].str.contains(search_query, case=False, na=False)]
            elif search_type == "Author":
                results = df[df['author'].str.contains(search_query, case=False, na=False)]
            else:  # ISBN
                results = df[df['isbn'].str.contains(search_query, case=False, na=False)]
            
            if not results.empty:
                st.write(f"Found {len(results)} book(s):")
                st.dataframe(results, use_container_width=True)
            else:
                st.warning("No books found matching your search.")
    
    # Display overdue books warning
    overdue_books = df[(df['status'] == 'Borrowed') & (df['due_date'] != '')]
    if not overdue_books.empty:
        overdue_books['due_date_dt'] = pd.to_datetime(overdue_books['due_date'])
        actual_overdue = overdue_books[overdue_books['due_date_dt'] < datetime.now()]
        
        if not actual_overdue.empty:
            st.sidebar.warning(f"⚠️ {len(actual_overdue)} book(s) overdue!")

if __name__ == "__main__":
    main()
