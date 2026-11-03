import streamlit as st
from rag_engine import generate_answer
from vector_store import (
    add_pdf_to_vector_store,
    get_uploaded_documents
)

# Page configuration
st.set_page_config(
    page_title="RAG Notes Assistant",
    page_icon="📚",
    layout="centered"
)

# Application heading
st.title("📚 RAG Notes Assistant")
st.caption(
    "Your personal AI study assistant. "
    "Ask questions from your uploaded study notes."
)

st.divider()

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("About")
    st.write(
        "This application uses Retrieval-Augmented Generation "
        "(RAG) to answer questions from your study notes."
    )
    st.divider()

    # PDF Upload Section
    st.header("📁 Upload Documents")

    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Process PDFs", use_container_width=True):

        if uploaded_files:

            for uploaded_file in uploaded_files:

                try:
                    with st.spinner(
                        f"Processing {uploaded_file.name}..."
                    ):

                        result = add_pdf_to_vector_store(
                            uploaded_file.getvalue(),
                            uploaded_file.name
                        )

                    st.success(
                        f"{result['source']} processed successfully!"
                    )

                    st.write(
                        f"Pages: {result['total_pages']} | "
                        f"Chunks: {result['total_chunks']}"
                    )

                except Exception as error:
                    st.error(
                        f"Error processing {uploaded_file.name}: {error}"
                    )

            st.rerun()

        else:
            st.warning("Please upload at least one PDF.")

    # Display uploaded documents
    
    st.subheader("📚 Current Knowledge Base")

    documents = get_uploaded_documents()

    if documents:
        for document in documents:
            st.write(f"📄 {document['source']}")
    else:
        st.info("No documents in the knowledge base.")


    documents = get_uploaded_documents()

    if documents:

        for document in documents:

            with st.expander(document["source"]):

                st.write(
                    f"Pages: {document['total_pages']}"
                )

                st.write(
                    f"Chunks: {document['total_chunks']}"
                )

    else:
        st.info("No documents uploaded yet.")

    st.divider()

    st.subheader("Current Knowledge Base")
    st.write("📄 Python_Notes.pdf")

    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Display previous conversation
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Display source references for assistant messages
        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("View Sources"):
                for source in message["sources"]:
                    st.markdown(
                        f"**Document:** {source['source']}"
                    )
                    st.markdown(
                        f"**Page:** {source['page']}"
                    )

# Chat input
question = st.chat_input(
    "Ask something about your notes..."
)

if question:

    # Display user question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Searching your notes and generating an answer..."):

            try:
                answer, sources = generate_answer(question)

                st.markdown(answer)

                # Display source references
                if sources:
                    with st.expander("View Sources"):
                        for source in sources:
                            st.markdown(
                                f"**Document:** {source['source']}"
                            )
                            st.markdown(
                                f"**Page:** {source['page']}"
                            )
                            st.divider()

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except Exception as error:
                st.error(
                    "Something went wrong while generating the answer."
                )
                st.caption(str(error))
