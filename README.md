# ⚖️ Legal AI Assistant (RAG-based)

An intelligent Legal AI Assistant built using Retrieval-Augmented
Generation (RAG) that provides legal information across multiple domains
like Consumer Law, Food Safety, and Cyber Crime.

⚠️ Disclaimer: This assistant provides information based on government
legal sources. It is not a substitute for professional legal advice.
Please consult a qualified lawyer for real cases.

------------------------------------------------------------------------

## 🚀 Features

-   Multi-domain legal query support (Consumer, Food, Cyber)
-   RAG-based context-aware answers
-   Pinecone Vector Database integration
-   Query expansion + reranking
-   Next.js interactive UI
-   Dark mode + animations

------------------------------------------------------------------------

## 🏗️ Architecture

User → Frontend (Next.js) → FastAPI Backend → Pinecone Vector DB →
Retrieval + Reranking → LLM → Response

------------------------------------------------------------------------

## 🛠️ Tech Stack

Frontend: Next.js, Tailwind, Framer Motion\
Backend: FastAPI, Python\
AI: Sentence Transformers, CrossEncoder\
DB: Pinecone

------------------------------------------------------------------------

## 📂 Project Structure

Law Assistant Bot/ │ ├── main.py ├── src/ │ ├── chunker.py │ ├──
embedder.py │ ├── logger.py │ ├── pdf_loader.py │ ├──
pinecone_uploader.py │ ├── query_rewriter.py │ ├── rag_pipeline.py │ ├──
retriever.py │ └── section_parser.py │ ├── frontend/ │ ├── app/ │ ├──
components/ │ ├── data/ │ ├── raw_data/ │ └── processed_data/ │ ├──
logs/ ├── .env ├── pyproject.toml ├── uv.lock ├── docker-compose.yml ├──
.gitignore └── README.md

------------------------------------------------------------------------

## ⚙️ Setup (using uv)

``` bash
uv sync
uv run uvicorn main:app --reload
```

Frontend:

``` bash
cd frontend
npm install
npm run dev
```

------------------------------------------------------------------------

## 📌 Future Improvements

-   Auto domain detection
-   Chat memory
-   Streaming responses
-   Deployment (Docker + Vercel + Render)

------------------------------------------------------------------------

## 👨‍💻 Author

Shakti Sarada Prasad

