# import streamlit as st
# import pandas as pd
# from datetime import datetime, timedelta
# import os

# # Page configuration
# st.set_page_config(
#     page_title="Library Book Management",
#     page_icon="📚",
#     layout="wide"
# )

# # File path for CSV
# CSV_FILE = "books.csv"

# def load_data():
#     """Load book data from CSV file"""
#     if os.path.exists(CSV_FILE):
#         return pd.read_csv(CSV_FILE)
#     else:
#         # Create initial dataframe if file doesn't exist
#         initial_data = {
#             'book_id': [1, 2, 3, 4, 5],
#             'title': ['The Great Gatsby', 'To Kill a Mockingbird', '1984', 
#                      'Pride and Prejudice', 'The Catcher in the Rye'],
#             'author': ['F. Scott Fitzgerald', 'Harper Lee', 'George Orwell', 
#                       'Jane Austen', 'J.D. Salinger'],
#             'isbn': ['9780743273565', '9780061120084', '9780451524935', 
#                     '9780141439518', '9780316769174'],
#             'status': ['Available', 'Borrowed', 'Available', 'Borrowed', 'Available'],
#             'borrower': ['', 'John Doe', '', 'Jane Smith', ''],
#             'due_date': ['', '2024-02-15', '', '2024-02-20', '']
#         }
#         df = pd.DataFrame(initial_data)
#         df.to_csv(CSV_FILE, index=False)
#         return df

# def save_data(df):
#     """Save book data to CSV file"""
#     df.to_csv(CSV_FILE, index=False)

# def borrow_book(df, book_id, borrower_name, days=14):
#     """Borrow a book"""
#     due_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
#     df.loc[df['book_id'] == book_id, 'status'] = 'Borrowed'
#     df.loc[df['book_id'] == book_id, 'borrower'] = borrower_name
#     df.loc[df['book_id'] == book_id, 'due_date'] = due_date
#     save_data(df)
#     return df

# def return_book(df, book_id):
#     """Return a book"""
#     df.loc[df['book_id'] == book_id, 'status'] = 'Available'
#     df.loc[df['book_id'] == book_id, 'borrower'] = ''
#     df.loc[df['book_id'] == book_id, 'due_date'] = ''
#     save_data(df)
#     return df

# def add_new_book(df, title, author, isbn):
#     """Add a new book to the library"""
#     new_id = df['book_id'].max() + 1 if not df.empty else 1
#     new_book = {
#         'book_id': new_id,
#         'title': title,
#         'author': author,
#         'isbn': isbn,
#         'status': 'Available',
#         'borrower': '',
#         'due_date': ''
#     }
#     df = pd.concat([df, pd.DataFrame([new_book])], ignore_index=True)
#     save_data(df)
#     return df

# def main():
#     st.title("📚 Library Book Management System")
    
#     # Load data
#     df = load_data()
    
#     # Sidebar for actions
#     st.sidebar.title("Library Actions")
#     action = st.sidebar.selectbox(
#         "Choose Action",
#         ["View Books", "Borrow Book", "Return Book", "Add New Book", "Search Books"]
#     )
    
#     if action == "View Books":
#         st.header("📖 All Books in Library")
        
#         # Display statistics
#         col1, col2, col3 = st.columns(3)
#         total_books = len(df)
#         available_books = len(df[df['status'] == 'Available'])
#         borrowed_books = len(df[df['status'] == 'Borrowed'])
        
#         col1.metric("Total Books", total_books)
#         col2.metric("Available Books", available_books)
#         col3.metric("Borrowed Books", borrowed_books)
        
#         # Display books in a table
#         st.dataframe(df, use_container_width=True)
        
#     elif action == "Borrow Book":
#         st.header("📥 Borrow a Book")
        
#         # Filter available books
#         available_books = df[df['status'] == 'Available']
        
#         if available_books.empty:
#             st.warning("No books available for borrowing.")
#         else:
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 selected_book = st.selectbox(
#                     "Select Book to Borrow",
#                     available_books.apply(
#                         lambda x: f"{x['title']} by {x['author']} (ID: {x['book_id']})", 
#                         axis=1
#                     )
#                 )
#                 book_id = int(selected_book.split("(ID: ")[1].replace(")", ""))
                
#             with col2:
#                 borrower_name = st.text_input("Borrower Name")
#                 borrow_days = st.slider("Borrow for (days)", 1, 30, 14)
            
#             if st.button("Borrow Book"):
#                 if borrower_name.strip():
#                     df = borrow_book(df, book_id, borrower_name, borrow_days)
#                     st.success(f"Book borrowed successfully! Due date: {(datetime.now() + timedelta(days=borrow_days)).strftime('%Y-%m-%d')}")
#                     st.rerun()
#                 else:
#                     st.error("Please enter borrower name.")
    
#     elif action == "Return Book":
#         st.header("📤 Return a Book")
        
#         # Filter borrowed books
#         borrowed_books = df[df['status'] == 'Borrowed']
        
#         if borrowed_books.empty:
#             st.warning("No books to return.")
#         else:
#             selected_book = st.selectbox(
#                 "Select Book to Return",
#                 borrowed_books.apply(
#                     lambda x: f"{x['title']} by {x['author']} - Borrowed by: {x['borrower']} (ID: {x['book_id']})", 
#                     axis=1
#                 )
#             )
#             book_id = int(selected_book.split("(ID: ")[1].replace(")", ""))
            
#             if st.button("Return Book"):
#                 df = return_book(df, book_id)
#                 st.success("Book returned successfully!")
#                 st.rerun()
    
#     elif action == "Add New Book":
#         st.header("➕ Add New Book")
        
#         with st.form("add_book_form"):
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 title = st.text_input("Book Title")
#                 author = st.text_input("Author")
            
#             with col2:
#                 isbn = st.text_input("ISBN")
            
#             submitted = st.form_submit_button("Add Book")
            
#             if submitted:
#                 if title and author and isbn:
#                     df = add_new_book(df, title, author, isbn)
#                     st.success("Book added successfully!")
#                     st.rerun()
#                 else:
#                     st.error("Please fill in all fields.")
    
#     elif action == "Search Books":
#         st.header("🔍 Search Books")
        
#         search_type = st.radio("Search by:", ["Title", "Author", "ISBN"])
#         search_query = st.text_input("Enter search term")
        
#         if search_query:
#             if search_type == "Title":
#                 results = df[df['title'].str.contains(search_query, case=False, na=False)]
#             elif search_type == "Author":
#                 results = df[df['author'].str.contains(search_query, case=False, na=False)]
#             else:  # ISBN
#                 results = df[df['isbn'].str.contains(search_query, case=False, na=False)]
            
#             if not results.empty:
#                 st.write(f"Found {len(results)} book(s):")
#                 st.dataframe(results, use_container_width=True)
#             else:
#                 st.warning("No books found matching your search.")
    
#     # Display overdue books warning
#     overdue_books = df[(df['status'] == 'Borrowed') & (df['due_date'] != '')]
#     if not overdue_books.empty:
#         overdue_books['due_date_dt'] = pd.to_datetime(overdue_books['due_date'])
#         actual_overdue = overdue_books[overdue_books['due_date_dt'] < datetime.now()]
        
#         if not actual_overdue.empty:
#             st.sidebar.warning(f"⚠️ {len(actual_overdue)} book(s) overdue!")

# if __name__ == "__main__":
#     main()
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import io

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

def merge_csv_data(existing_df, new_df, merge_strategy):
    """
    Merge new CSV data with existing data based on selected strategy
    
    Args:
        existing_df: Current master DataFrame
        new_df: New DataFrame from uploaded CSV
        merge_strategy: 'update_existing', 'add_new', or 'replace_all'
    """
    if merge_strategy == 'replace_all':
        return new_df
    
    elif merge_strategy == 'add_new':
        # Find books in new_df that don't exist in existing_df (by ISBN or title+author)
        existing_books = existing_df.apply(
            lambda x: f"{x['title'].lower()}_{x['author'].lower()}", axis=1
        ).tolist()
        
        new_books_mask = new_df.apply(
            lambda x: f"{x['title'].lower()}_{x['author'].lower()}" not in existing_books, 
            axis=1
        )
        
        books_to_add = new_df[new_books_mask].copy()
        
        if not books_to_add.empty:
            # Assign new book IDs
            max_id = existing_df['book_id'].max()
            books_to_add['book_id'] = range(max_id + 1, max_id + 1 + len(books_to_add))
            
            # Ensure status, borrower, and due_date columns exist
            for col in ['status', 'borrower', 'due_date']:
                if col not in books_to_add.columns:
                    books_to_add[col] = 'Available' if col == 'status' else ''
            
            merged_df = pd.concat([existing_df, books_to_add], ignore_index=True)
            return merged_df
        else:
            st.info("No new books found in the uploaded file.")
            return existing_df
    
    elif merge_strategy == 'update_existing':
        # Update existing records and add new ones
        merged_df = existing_df.copy()
        
        for _, new_row in new_df.iterrows():
            # Try to find existing book by ISBN first, then by title+author
            mask = (
                (existing_df['isbn'] == new_row['isbn']) if 'isbn' in new_row and pd.notna(new_row['isbn']) 
                else (
                    (existing_df['title'].str.lower() == new_row['title'].lower()) & 
                    (existing_df['author'].str.lower() == new_row['author'].lower())
                )
            )
            
            if mask.any():
                # Update existing record
                idx = mask.idxmax()
                for col in new_row.index:
                    if col in merged_df.columns and pd.notna(new_row[col]):
                        merged_df.at[idx, col] = new_row[col]
            else:
                # Add new record
                new_book = new_row.to_dict()
                if 'book_id' not in new_book or pd.isna(new_book['book_id']):
                    new_book['book_id'] = merged_df['book_id'].max() + 1
                merged_df = pd.concat([merged_df, pd.DataFrame([new_book])], ignore_index=True)
        
        return merged_df

def validate_csv_structure(df):
    """
    Validate that the uploaded CSV has the required structure
    """
    required_columns = ['title', 'author']
    optional_columns = ['book_id', 'isbn', 'status', 'borrower', 'due_date']
    
    missing_required = [col for col in required_columns if col not in df.columns]
    
    if missing_required:
        return False, f"Missing required columns: {', '.join(missing_required)}"
    
    # Add missing optional columns with default values
    for col in optional_columns:
        if col not in df.columns:
            if col == 'status':
                df[col] = 'Available'
            elif col == 'book_id':
                df[col] = range(1, len(df) + 1)
            else:
                df[col] = ''
    
    return True, "CSV structure is valid"

def main():
    st.title("📚 Library Book Management System")
    
    # Load data
    df = load_data()
    
    # Sidebar for actions
    st.sidebar.title("Library Actions")
    action = st.sidebar.selectbox(
        "Choose Action",
        ["View Books", "Borrow Book", "Return Book", "Add New Book", "Search Books", "Import CSV Data"]
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
    
    elif action == "Import CSV Data":
        st.header("📁 Import Books from CSV")
        
        st.info("""
        **Upload a CSV file to import books into your library.**  
        Required columns: `title`, `author`  
        Optional columns: `book_id`, `isbn`, `status`, `borrower`, `due_date`
        """)
        
        uploaded_file = st.file_uploader(
            "Choose a CSV file", 
            type=['csv'],
            help="Upload a CSV file with book records"
        )
        
        if uploaded_file is not None:
            try:
                # Read the uploaded CSV
                new_df = pd.read_csv(uploaded_file)
                
                # Display preview
                st.subheader("📋 Uploaded Data Preview")
                st.dataframe(new_df.head(), use_container_width=True)
                st.write(f"Total records in uploaded file: {len(new_df)}")
                
                # Validate CSV structure
                is_valid, validation_message = validate_csv_structure(new_df)
                
                if not is_valid:
                    st.error(f"❌ Invalid CSV structure: {validation_message}")
                else:
                    st.success("✅ CSV structure is valid!")
                    
                    # Merge strategy selection
                    st.subheader("🔄 Merge Strategy")
                    merge_strategy = st.radio(
                        "How would you like to merge the data?",
                        options=['update_existing', 'add_new', 'replace_all'],
                        format_func=lambda x: {
                            'update_existing': 'Update existing records and add new ones',
                            'add_new': 'Add only new records (skip existing)',
                            'replace_all': 'Replace all existing data'
                        }[x],
                        help="Choose how to combine the uploaded data with existing records"
                    )
                    
                    # Show impact analysis
                    st.subheader("📊 Impact Analysis")
                    
                    if merge_strategy == 'update_existing':
                        # Analyze potential updates
                        existing_titles = df['title'].str.lower().tolist()
                        new_titles = new_df['title'].str.lower().tolist()
                        
                        matching_titles = set(existing_titles) & set(new_titles)
                        new_titles_only = set(new_titles) - set(existing_titles)
                        
                        st.write(f"• {len(matching_titles)} existing books will be updated")
                        st.write(f"• {len(new_titles_only)} new books will be added")
                        
                    elif merge_strategy == 'add_new':
                        existing_books = df.apply(
                            lambda x: f"{x['title'].lower()}_{x['author'].lower()}", axis=1
                        ).tolist()
                        
                        new_books = new_df.apply(
                            lambda x: f"{x['title'].lower()}_{x['author'].lower()}", axis=1
                        ).tolist()
                        
                        new_books_only = set(new_books) - set(existing_books)
                        st.write(f"• {len(new_books_only)} new books will be added")
                        st.write(f"• {len(new_df) - len(new_books_only)} existing books will be skipped")
                    
                    else:  # replace_all
                        st.warning("⚠️ This will replace ALL existing data with the uploaded file!")
                        st.write(f"• Current records: {len(df)}")
                        st.write(f"• New records: {len(new_df)}")
                    
                    # Confirmation and import
                    if st.button("🚀 Import Data", type="primary"):
                        with st.spinner("Importing data..."):
                            try:
                                df_merged = merge_csv_data(df, new_df, merge_strategy)
                                save_data(df_merged)
                                df = df_merged
                                st.success(f"✅ Data imported successfully! Total records: {len(df_merged)}")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error during import: {str(e)}")
                
            except Exception as e:
                st.error(f"❌ Error reading CSV file: {str(e)}")
                st.info("Please ensure your file is a valid CSV with proper formatting.")
        
        # Download current data template
        st.subheader("📥 Download Template")
        st.download_button(
            label="Download Current Data as CSV",
            data=df.to_csv(index=False),
            file_name="library_books_backup.csv",
            mime="text/csv",
            help="Download current library data as a backup or template"
        )
    
    # Display overdue books warning
    overdue_books = df[(df['status'] == 'Borrowed') & (df['due_date'] != '')]
    if not overdue_books.empty:
        overdue_books['due_date_dt'] = pd.to_datetime(overdue_books['due_date'])
        actual_overdue = overdue_books[overdue_books['due_date_dt'] < datetime.now()]
        
        if not actual_overdue.empty:
            st.sidebar.warning(f"⚠️ {len(actual_overdue)} book(s) overdue!")

if __name__ == "__main__":
    main()
