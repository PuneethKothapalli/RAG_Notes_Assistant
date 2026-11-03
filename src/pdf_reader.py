from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):

    # Open the PDF document
    reader = PdfReader(pdf_path)

    extracted_pages = []

    # Read each page individually
    for page_number, page in enumerate(reader.pages, start=1):

        # Extract text from the current page
        text = page.extract_text() or ""

        # Store page number and extracted text
        extracted_pages.append({
            "page": page_number,
            "text": text
        })

    return extracted_pages


# Test the PDF reader
if __name__ == "__main__":

    pdf_path = "data/Python_Notes.pdf"

    pages = extract_text_from_pdf(pdf_path)

    print("PDF extraction successful!")
    print(f"Total pages: {len(pages)}")

    for page in pages:
        print(f"\n--- Page {page['page']} ---")
        print(page["text"][:500])
