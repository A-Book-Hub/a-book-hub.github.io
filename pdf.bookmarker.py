import fitz  # PyMuPDF

def save_bookmark(page_number, filename='bookmark.txt'):
    with open(filename, 'w') as f:
        f.write(str(page_number))

def load_bookmark(filename='bookmark.txt'):
    try:
        with open(filename, 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0  # Default to the first page if no bookmark found

def open_pdf_with_bookmark(pdf_file, bookmark_file='bookmark.txt'):
    doc = fitz.open(pdf_file)
    page_number = load_bookmark(bookmark_file)
    page = doc.load_page(page_number)  # Load the saved page
    print(f"Opening PDF at page {page_number + 1}")
    
    # Save the current page as a bookmark before closing
    new_bookmark_page = int(input(f"Enter the page number to bookmark (current: {page_number + 1}): ")) - 1
    save_bookmark(new_bookmark_page, bookmark_file)
    doc.close()

# Example usage
pdf_file = 'example.pdf'  # Replace with the path to your PDF
bookmark_file = 'bookmark.txt'
open_pdf_with_bookmark(pdf_file, bookmark_file)