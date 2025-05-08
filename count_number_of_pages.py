# check all pdfs in a directory and count how many pages are there in total

import os
from PyPDF2 import PdfReader

def count_pages_in_pdf(pdf_path):
    """
    Count the number of pages in a PDF file.
    """
    try:
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            return len(reader.pages)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return 0
    return count_pages_in_pdf(pdf_path)

def count_pages_in_pdfs(pdfs_dir):
    """
    Count the total number of pages in all PDF files in a directory.
    """
    total_pages = 0
    pdf_files = []
    for root, _, files in os.walk(pdfs_dir):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))

    for pdf_path in pdf_files:
        pages = count_pages_in_pdf(pdf_path)
        total_pages += pages
        print(f"{pdf_path}: {pages} pages")

    print(f"Total number of pages in all PDFs: {total_pages}")

if __name__ == "__main__":
    pdfs_dir = "pdfs"  # Replace with your PDF directory
    count_pages_in_pdfs(pdfs_dir)