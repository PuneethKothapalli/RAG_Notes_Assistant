import chromadb
import hashlib
from io import BytesIO
from pypdf import PdfReader

from pdf_reader import extract_text_from_pdf
from text_chunker import create_chunks
from embedding_generator import (
    embed_model,
    generate_embeddings
)


# Step 1: Initialize persistent ChromaDB
client = chromadb.PersistentClient(
    path="./chroma_db"
)


# Step 2: Create or access a collection
collection = client.get_or_create_collection(
    name="python_notes"
)


def store_embeddings(embedded_chunks):

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    # Step 3: Prepare data for ChromaDB
    for chunk in embedded_chunks:

        chunk_id = f"python_notes_{chunk['chunk_id']}"

        ids.append(chunk_id)
        documents.append(chunk["text"])
        embeddings.append(chunk["embedding"])

        metadatas.append({
            "page": chunk["page"],
            "source": "Python_Notes.pdf"
        })

    # Step 4: Store vectors and metadata
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print("\nEmbeddings stored successfully!")


def add_pdf_to_vector_store(pdf_bytes, source_name):

    # 1. Generate a unique ID for this PDF
    doc_id = hashlib.sha256(pdf_bytes).hexdigest()[:16]

    # 2. Extract text from the uploaded PDF
    reader = PdfReader(BytesIO(pdf_bytes))

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append({
            "page": page_number,
            "text": text
        })

    # Check whether the PDF contains extractable text
    if not any(page["text"].strip() for page in pages):
        raise ValueError(
            "No extractable text found in this PDF."
        )

    # 3. Split extracted text into chunks
    chunks = create_chunks(pages)

    if not chunks:
        raise ValueError("No text chunks were generated.")

    # 4. Generate embeddings
    embedded_chunks = generate_embeddings(chunks)

    # 5. Prepare data for ChromaDB
    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for chunk in embedded_chunks:

        chunk_id = f"{doc_id}_{chunk['chunk_id']}"

        ids.append(chunk_id)
        documents.append(chunk["text"])
        embeddings.append(chunk["embedding"])

        metadatas.append({
            "doc_id": doc_id,
            "chunk_number": chunk["chunk_id"],
            "page": chunk["page"],
            "source": source_name
        })

    # 6. Store embeddings in ChromaDB
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return {
        "doc_id": doc_id,
        "source": source_name,
        "total_pages": len(pages),
        "total_chunks": len(chunks)
    }




def get_uploaded_documents():

    results = collection.get(
        include=["metadatas"]
    )

    documents = {}

    for metadata in results["metadatas"]:

        # Skip old records that don't have doc_id
        if not metadata or "doc_id" not in metadata:
            continue

        doc_id = metadata["doc_id"]

        if doc_id not in documents:
            documents[doc_id] = {
                "doc_id": doc_id,
                "source": metadata["source"],
                "total_chunks": 0,
                "pages": set()
            }

        documents[doc_id]["total_chunks"] += 1
        documents[doc_id]["pages"].add(metadata["page"])

    uploaded_documents = []

    for document in documents.values():

        document["total_pages"] = len(document["pages"])
        del document["pages"]

        uploaded_documents.append(document)

    return uploaded_documents




def delete_document(doc_id):

    # Delete all chunks belonging to this document
    collection.delete(
        where={"doc_id": doc_id}
    )

    print(f"Document {doc_id} deleted successfully!")



def search_notes(question, top_k=3):

    # Convert question into an embedding
    query_embedding = embed_model.get_query_embedding(
        question
    )

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


def search_notes_with_neighbors(question, top_k=5, window=1):
    # Step 1: Generate embedding for the user's question
    query_embedding = embed_model.get_query_embedding(question)

    # Step 2: Retrieve the most relevant chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrieved_ids = results["ids"][0]

    # Handle cases where no chunks are found
    if not retrieved_ids:
        return {
            "ids": [[]],
            "documents": [[]],
            "metadatas": [[]]
        }

    # Step 3: Identify neighboring chunk IDs
    neighbor_ids = set()

    for chunk_id in retrieved_ids:
        # Example: python_notes_10 -> 10
        chunk_number = int(chunk_id.split("_")[-1])

        # Include the previous, current, and next chunks
        for number in range(
            max(1, chunk_number - window),
            chunk_number + window + 1
        ):
            neighbor_ids.add(f"python_notes_{number}")

    # Step 4: Retrieve neighboring chunks from ChromaDB
    expanded_results = collection.get(
        ids=sorted(
            neighbor_ids,
            key=lambda x: int(x.split("_")[-1])
        ),
        include=["documents", "metadatas"]
    )

    # Step 5: Sort chunks in their original document order
    records = sorted(
        zip(
            expanded_results["ids"],
            expanded_results["documents"],
            expanded_results["metadatas"]
        ),
        key=lambda x: int(x[0].split("_")[-1])
    )

    return {
        "ids": [[record[0] for record in records]],
        "documents": [[record[1] for record in records]],
        "metadatas": [[record[2] for record in records]]
    }



if __name__ == "__main__":

    pdf_path = "data/Python_Notes.pdf"

    # Extract PDF text
    pages = extract_text_from_pdf(pdf_path)

    # Generate chunks
    chunks = create_chunks(pages)

    # Generate embeddings
    embedded_chunks = generate_embeddings(chunks)

    # Store embeddings
    store_embeddings(embedded_chunks)

    # Test semantic search
    question = "What are the features of Python?"

    results = search_notes(question)

    print("\nSemantic Search Results:")

    for i, document in enumerate(
        results["documents"][0],
        start=1
    ):

        metadata = results["metadatas"][0][i - 1]

        print(f"\nResult {i}")
        print("Page:", metadata["page"])
        print("Content:", document[:300])
