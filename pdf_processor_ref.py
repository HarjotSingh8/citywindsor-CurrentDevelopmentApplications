import fitz
from typing import List, Tuple

def extract_text_with_positions(pdf_path: str) -> List[Tuple[str, int, fitz.Rect]]:
    """
    Extract text and position information from the PDF.

    Args:
        pdf_path: Path to the input PDF file

    Returns:
        List of tuples containing (text, page_number, text_rectangle)
    """
    doc = fitz.open(pdf_path)
    text_positions = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        if text.strip():  # Skip empty text
                            bbox = fitz.Rect(span["bbox"])
                            text_positions.append((text, page_num, bbox))

    doc.close()
    return text_positions

def main():
    pdf_path = input("Enter the path to the PDF file: ")
    text_positions = extract_text_with_positions(pdf_path)

    for text, page_num, bbox in text_positions:
        print(f"Page {page_num + 1}: {text} (Location: {bbox})")

if __name__ == "__main__":
    main()