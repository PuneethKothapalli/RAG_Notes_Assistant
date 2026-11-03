# 📚 RAG Notes Assistant

### AI-Powered Document Question Answering Using Retrieval-Augmented Generation

RAG Notes Assistant is an AI-powered document question-answering application that allows users to interact with their study materials using natural language.

Built using **Python, Streamlit, Google Gemini API, Hugging Face Embeddings, and ChromaDB**, the application extracts information from PDF documents, retrieves relevant content through semantic search, and generates context-aware responses using a Large Language Model (LLM).

The project demonstrates the practical implementation of a Retrieval-Augmented Generation (RAG) pipeline for document-based question answering.

---

## 🚀 Features

- **PDF Text Extraction:** Extract text and page-level information from PDF documents using PyPDF.
- **Intelligent Text Chunking:** Split extracted content into smaller chunks using LlamaIndex SentenceSplitter with configurable chunk size and overlap.
- **Embedding Generation:** Convert text chunks into vector representations using the Hugging Face `BAAI/bge-small-en-v1.5` model.
- **Vector Storage:** Store document embeddings, text and metadata using ChromaDB.
- **Semantic Search:** Retrieve relevant document content based on the semantic meaning of user queries.
- **Neighboring-Chunk Retrieval:** Expand retrieved context using surrounding chunks to improve information coverage.
- **AI-Powered Answer Generation:** Generate natural-language responses using the Google Gemini API.
- **Source References:** Display document names and page numbers associated with retrieved information.
- **Interactive Chat Interface:** Ask questions and view responses through a Streamlit web application.
- **PDF Upload:** Upload and process multiple PDF documents through the application.
- **Document Management:** View uploaded documents along with their page counts and chunk counts.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| Google Gemini API | LLM-based answer generation |
| LlamaIndex | Text processing and LLM integration |
| Hugging Face | Pre-trained embedding models |
| BAAI/bge-small-en-v1.5 | Text embedding generation |
| ChromaDB | Vector database and similarity search |
| PyPDF | PDF text extraction |
| SentenceSplitter | Text chunking |
| python-dotenv | Environment variable management |

---

## 🏗️ System Architecture

The application follows a Retrieval-Augmented Generation (RAG) architecture consisting of two major pipelines.

### 1. Document Ingestion Pipeline

The ingestion pipeline processes PDF documents and stores their content in a vector database.

```text
       PDF Documents
             |
             v
      Text Extraction
             |
             v
       Text Chunking
             |
             v
    Embedding Generation
             |
             v
        ChromaDB
             |
             v
    Document Metadata
```

### 2. Question Answering Pipeline

The retrieval pipeline finds relevant document content and generates answers using Gemini.

```text
       User Question
             |
             v
    Query Embedding
             |
             v
      Semantic Search
             |
             v
   Relevant Chunk Retrieval
             |
             v
   Neighboring-Chunk Retrieval
             |
             v
     Context Preparation
             |
             v
        Gemini API
             |
             v
     Generated Answer
             |
             v
    Answer + Source References
```

---

## 📂 Project Structure

```text
RAG-Notes-Assistant/
│
├── __pycache__/
│
├── .venv/
│
├── chroma_db/
│
├── data/
│   └── Python_Notes.pdf
│
├── src/
│   ├── embedding_generator.py
│   ├── pdf_reader.py
│   ├── rag_engine.py
│   ├── text_chunker.py
│   └── vector_store.py
│
├── app.py
├── .env
├── .gitignore
└── requirements.txt
```

**Directory overview:**

| File / Directory | Description |
|---|---|
| `app.py` | Streamlit application entry point |
| `src/pdf_reader.py` | Extracts text from PDF documents |
| `src/text_chunker.py` | Splits extracted text into manageable chunks |
| `src/embedding_generator.py` | Generates vector embeddings |
| `src/vector_store.py` | Manages ChromaDB storage and retrieval |
| `src/rag_engine.py` | Coordinates retrieval and Gemini response generation |
| `data/` | Stores local PDF documents |
| `chroma_db/` | Stores the persistent ChromaDB vector database |
| `.env` | Stores environment variables and API credentials |
| `requirements.txt` | Lists project dependencies |
| `.gitignore` | Specifies files and directories excluded from Git |

*Note: `.venv/`, `__pycache__/`, `.env`, and local database and document files are excluded from the GitHub repository.*

---

## ⚙️ Installation and Setup

Follow these steps to run the application locally.

### Prerequisites

- Python 3.10 or later
- Git
- Google Gemini API key
- Internet connection for API access and initial embedding model download

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/RAG-Notes-Assistant.git
```

Navigate to the project directory:

```bash
cd RAG-Notes-Assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory.

Add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Obtain an API key from [Google AI Studio](https://aistudio.google.com/).

**Security Note:** Never commit your `.env` file or expose your API key in public repositories.

### 5. Run the Application

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

Open the following address in your browser:

```text
http://localhost:8501
```

---

## 🧠 Understanding Retrieval-Augmented Generation

Retrieval-Augmented Generation combines information retrieval with generative AI.

Instead of relying entirely on the language model's pre-trained knowledge, RAG retrieves relevant information from external documents and supplies it as context to the language model.

In this project:

1. PDF content is extracted and divided into chunks.
2. Each chunk is converted into a numerical vector using an embedding model.
3. ChromaDB stores the vectors and associated document information.
4. User questions are converted into embeddings.
5. Semantic similarity search identifies relevant chunks.
6. Neighboring chunks provide additional context.
7. Gemini generates an answer using the retrieved information.

This approach helps ground generated responses in the content of the uploaded study materials.

---

## 🔐 Environment Variables

The application requires the following environment variable:

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | API key for accessing the Google Gemini API |

The Hugging Face embedding model is downloaded locally when first initialized. A Hugging Face token is not required for the public embedding model under normal usage.

---

## ⚠️ Current Limitations

- PDF extraction currently focuses on text-based PDFs. Scanned documents may require OCR.
- Answer quality depends on the quality and completeness of retrieved document context.
- Gemini API availability and rate limits can affect response generation.
- The vector database is currently maintained locally.
- Multi-document ingestion and listing are implemented; comprehensive cross-document retrieval and document deletion through the interface are still under development.

---

## 🛣️ Future Enhancements

- [ ] Complete multi-document question answering.
- [ ] Add document deletion functionality.
- [ ] Implement hybrid search combining keyword and semantic retrieval.
- [ ] Integrate reranking for improved retrieval accuracy.
- [ ] Add conversation memory and chat history management.
- [ ] Improve the user interface and document management experience.
- [ ] Support scanned PDFs using OCR.
- [ ] Add document previews and richer source citations.
- [ ] Deploy the application for public access.

---

## 🤝 Contributing

Contributions, suggestions and improvements are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Implement your changes.
4. Commit your changes.
5. Push the branch to your fork.
6. Submit a Pull Request.

---

## 📄 License

This project is currently intended for educational and portfolio purposes.

A specific open-source license has not yet been selected.

---

## 👨‍💻 Author

**Puneeth Kothapalli**

- GitHub: [PuneethKothapalli](https://github.com/PuneethKothapalli)
- LinkedIn: [Connect with me](https://www.linkedin.com/in/venkata-puneeth-kothapalli-76827a343/)

---

⭐ If you find this project interesting, consider giving the repository a star!