from llama_index.core.node_parser import SentenceSplitter


def create_chunks(pages):

    # Initialize the text splitter
    splitter = SentenceSplitter(
        chunk_size=512,
        chunk_overlap=50
    )

    all_chunks = []

    # Process each page
    for page in pages:

        text = page["text"]

        # Split page text into smaller chunks
        chunks = splitter.split_text(text)

        # Store chunk information
        for chunk in chunks:

            all_chunks.append({
                "chunk_id": len(all_chunks) + 1,
                "page": page["page"],
                "text": chunk
            })

    return all_chunks


if __name__ == "__main__":

    from pdf_reader import extract_text_from_pdf

    pdf_path = "data/Python_Notes.pdf"

    pages = extract_text_from_pdf(pdf_path)

    chunks = create_chunks(pages)

    print("Text chunking successful!")
    print("Total pages:", len(pages))
    print("Total chunks:", len(chunks))

    for i, chunk in enumerate(chunks[:5], start=1):

        print(f"\n--- Chunk {i} ---")
        print("Page:", chunk["page"])
        print(chunk["text"])
