
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from pdf_reader import extract_text_from_pdf
from text_chunker import create_chunks


# Initialize the embedding model
embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)


def generate_embeddings(chunks):

    embedded_chunks = []

    for chunk in chunks:

        # Convert text into a numerical vector
        embedding = embed_model.get_text_embedding(
            chunk["text"]
        )

        # Store the original text and its embedding
        embedded_chunks.append({
            "chunk_id": chunk["chunk_id"],
            "page": chunk["page"],
            "text": chunk["text"],
            "embedding": embedding
        })

    return embedded_chunks


if __name__ == "__main__":

    pdf_path = "data/Python_Notes.pdf"

    # Step 1: Extract PDF text
    pages = extract_text_from_pdf(pdf_path)

    # Step 2: Divide text into chunks
    chunks = create_chunks(pages)

    # Step 3: Generate embeddings
    embedded_chunks = generate_embeddings(chunks)

    print("\nEmbedding generation successful!")

    print("Total chunks:", len(chunks))
    print("Total embeddings:", len(embedded_chunks))

    # Display the first embedding
    first_embedding = embedded_chunks[0]["embedding"]

    print("\nFirst chunk:")
    print(embedded_chunks[0]["text"])

    print("\nEmbedding dimensions:", len(first_embedding))

    print("\nFirst 10 vector values:")
    print(first_embedding[:10])
