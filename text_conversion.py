# Read files from pdfs directory, replicate the structure of pdfs directory into texts directory
# save the text files in the same paths as the pdfs in the texts directory
# only extract text from pdfs

import os
from PyPDF2 import PdfReader
import sys

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    """
    # from PyPDF2 import PdfReader

    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None
    return text

def save_text_file(text, text_path):
    """
    Save text to a file.
    """
    try:
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"Error writing {text_path}: {e}")
        return False
    return True

def convert_pdfs_to_texts(pdfs_dir, texts_dir):
    """
    Convert all PDF files in a directory to text files with a progress indicator.
    """
    if not os.path.exists(texts_dir):
        os.makedirs(texts_dir)

    pdf_files = []
    for root, _, files in os.walk(pdfs_dir):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))

    total_files = len(pdf_files)
    for idx, pdf_path in enumerate(pdf_files, start=1):
        relative_path = os.path.relpath(pdf_path, pdfs_dir)
        text_path = os.path.join(texts_dir, relative_path.replace(".pdf", ".txt"))

        # Skip if text file already exists
        if os.path.exists(text_path):
            print(f"[{idx}/{total_files}] Text file already exists for {pdf_path}, skipping.")
            continue

        text = extract_text_from_pdf(pdf_path)
        if text is not None:
            text_dir = os.path.dirname(text_path)
            if not os.path.exists(text_dir):
                os.makedirs(text_dir)
            save_text_file(text, text_path)
            print(f"[{idx}/{total_files}] Successfully converted {pdf_path} to text.")
        else:
            print(f"[{idx}/{total_files}] Failed to extract text from {pdf_path}")

if __name__ == "__main__":
    pdfs_dir = "pdfs"
    texts_dir = "texts"
    convert_pdfs_to_texts(pdfs_dir, texts_dir)
    print("PDF to text conversion completed.")