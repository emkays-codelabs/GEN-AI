

---

# 🩺 Medical GenAI App — Poetry Project Setup Guide

## 📌 Project Summary

**Medical GenAI App** is a **Retrieval-Augmented Generation (RAG)** system that enables users to:

* Upload medical PDFs
* Create a persistent FAISS vector index
* Ask natural language questions
* Receive LLM-generated answers grounded in documents

The project follows:

* **Clean Architecture**
* **Strict UI / Backend separation**
* **Persistent vector storage**
* **Reproducible dependency management using Poetry**

---

## 🚀 Why Poetry for This Project?

Poetry is ideal here because:

✔ Deterministic dependency resolution
✔ Clean virtual environment isolation
✔ Easy collaboration
✔ Clear distinction between dev and prod deps
✔ Python path safety for `src/` layout

This project **benefits heavily** from Poetry because it uses:

* LangChain ecosystem
* FAISS
* Transformers
* Streamlit
* LLM providers

---

## 📁 Validated Project Structure

```
medical_genai_app/
├─ pyproject.toml              # Poetry configuration
├─ poetry.lock                 # Locked dependency graph
├─ .env                        # Environment variables
├─ data/
│   └─ faiss_index/            # Persistent FAISS index
│       ├─ index.faiss
│       └─ index.pkl
└─ src/
   ├─ app/                     # Streamlit frontend
   │   ├─ streamlit_app.py
   │   ├─ chat_ui_logic.py
   │   ├─ pdf_uploader.py
   │   └─ ui_components.py
   │
   └─ core/                    # RAG backend
       ├─ config/
       │   └─ settings.py
       ├─ embeddings/
       │   └─ faiss_index.py
       ├─ ingestion/
       │   ├─ pdf_parser.py
       │   └─ ingest.py
       ├─ query/
       │   ├─ query_index.py
       │   └─ chat_model.py
       └─ utils/
```

📌 This is a **proper `src/` layout**, fully compatible with Poetry.

---

## 🧱 Step 1: Install Poetry

```bash
pip install poetry
```

Verify:

```bash
poetry --version
```

---

## 🧱 Step 2: Initialize Poetry Project

From project root:

```bash
poetry init
```

Key choices:

* **Package name**: `medical-genai-app`
* **Python version**: `>=3.10,<3.13`
* **Dependencies**: add later

This creates:

* `pyproject.toml`

---

## 📦 Step 3: Add Dependencies

### Core Dependencies

```bash
poetry add \
  streamlit \
  langchain \
  langchain-community \
  sentence-transformers \
  faiss-cpu \
  pypdf \
  python-dotenv
```

### If using EuriAI / custom provider

```bash
poetry add euriai
```

### Development Dependencies

```bash
poetry add --group dev black ruff pytest ipykernel
```

---

## 🧠 Dependency Rationale

| Package               | Why                |
| --------------------- | ------------------ |
| streamlit             | Web UI             |
| langchain             | RAG orchestration  |
| langchain-community   | FAISS, embeddings  |
| sentence-transformers | Embeddings         |
| faiss-cpu             | Vector search      |
| pypdf                 | PDF parsing        |
| python-dotenv         | Environment config |
| euriai                | Chat model backend |
| pytest                | Testing            |
| black / ruff          | Code quality       |

---

## 🔐 Step 4: Environment Variables

Create `.env` in root:

```env
EURI_API_KEY=your_api_key_here
```

Load it in `settings.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## ⚙️ Step 5: `settings.py` (Critical)

Central configuration file:

```python
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[3]

DATA_DIR = BASE_DIR / "data"
FAISS_INDEX_DIR = DATA_DIR / "faiss_index"

EURI_API_KEY = os.getenv("EURI_API_KEY")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 4
```

📌 **Every module imports paths from here — never hardcode paths**

---

## 🧬 Step 6: Ingestion Workflow (One-Time or On Upload)

Triggered by:

* `pdf_uploader.py`

Flow:

```
PDF Upload
 → temp folder
 → extract_text_from_pdf()
 → chunk_text()
 → create_faiss_index()
 → save_local(data/faiss_index)
```

This happens **outside chat runtime**.

---

## 🔍 Step 7: Query Workflow (Runtime)

Triggered by:

* Chat input in Streamlit

Flow:

```
User Question
 → search_faiss()
 → retrieve_similar_documents()
 → generate_answer()
 → display response
```

📌 FAISS is **loaded from disk**, not rebuilt.

---

## 🧪 Step 8: Running the App (Poetry Way)

### Activate environment

```bash
poetry shell
```

### Run Streamlit

```bash
streamlit run src/app/streamlit_app.py
```

OR

```bash
poetry run streamlit run src/app/streamlit_app.py
```

---

## ✅ Key Architectural Checkpoints

✔ Same embedding model for ingest + query
✔ FAISS index persists across restarts
✔ UI does not import FAISS directly
✔ LLM only sees retrieved chunks
✔ Config centralized
✔ No hardcoded paths
✔ No global state outside Streamlit session

---

## ⚠️ Common Pitfalls (Avoid These)

❌ Rebuilding FAISS on every question
❌ Different embedding models for ingest/query
❌ Hardcoding `"data/faiss_index"`
❌ LLM answering without context guardrails
❌ Mixing UI and RAG logic

---

## 🧭 Recommended Next Enhancements

* Source citations in UI
* Conversation-aware retrieval
* Streaming responses
* Docker + Poetry export
* Multi-document indexing

---

## 🏁 Final Note

This is **production-quality RAG structure**.
With Poetry + this architecture, you have:

> ✔ Reproducibility
> ✔ Scalability
> ✔ Clarity
> ✔ Maintainability
---
