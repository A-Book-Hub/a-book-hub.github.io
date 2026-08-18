import fitz  # PyMuPDF

# Step 1: Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text[:5000]  # Limit for demonstration purposes

# Let's create a placeholder file path for now.
pdf_path = "/mnt/data/sample_book.pdf"

# Attempting to extract text from the PDF (if the file is uploaded)
try:
    extracted_text = extract_text_from_pdf(pdf_path)
except Exception as e:
    extracted_text = str(e)

extracted_text[:1000]  # Show preview of the extracted text
Result
"no such file: '/mnt/data/sample_book.pdf'"