
# 🩺 Medical GenAI App — Final Project Documentation

## 📌 Project Overview

**medical_genai_app** is a **Retrieval-Augmented Generation (RAG)** based medical chatbot that:

* Ingests medical PDFs
* Converts text into embeddings
* Stores embeddings in FAISS
* Retrieves relevant medical context
* Uses an LLM to answer user questions
* Provides a Streamlit-based UI

The project follows **clean architecture** with **strict separation** between:

* UI (`app/`)
* Backend RAG logic (`core/`)
* Persistent data (`data/`)

---

## 📁 Final Folder Structure (Corrected)

```
medical_genai_app/
├─ .venv/                     # Virtual environment
├─ data/
│   └─ faiss_index/           # Persistent FAISS index
│       ├─ index.faiss
│       └─ index.pkl
└─ src/
   ├─ app/                    # Streamlit frontend
   │   ├─ streamlit_app.py
   │   ├─ chat_ui_logic.py
   │   ├─ pdf_uploader.py
   │   └─ ui_components.py
   │
   └─ core/                   # RAG backend
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

---

# 🖥️ Frontend Layer — `src/app/`

This layer **never touches FAISS directly**.
It only calls **backend APIs**.

---

## 1️⃣ `streamlit_app.py` — Application Entry Point

### Purpose

* Main Streamlit entry file
* Wires together UI components and chat logic

### Responsibilities

* Configure Streamlit
* Render header
* Render PDF uploader
* Render chat interface

### Typical Flow

```text
App start
 → Header
 → PDF upload (optional)
 → Chat UI
```

### Calls

* `render_header()` → `ui_components.py`
* `pdf_uploader()` → `pdf_uploader.py`
* `render_chat_ui()` → `chat_ui_logic.py`

---

## 2️⃣ `pdf_uploader.py` — Upload & Re-Index PDFs

### Purpose

* Accepts PDF uploads from the user
* Triggers ingestion automatically

### Responsibilities

* Upload PDFs via Streamlit
* Save them to a temporary folder
* Call `ingest_pdfs()` from backend

### Key Functions

| Function                | Description             |
| ----------------------- | ----------------------- |
| `pdf_uploader()`        | UI + upload handling    |
| `save_uploaded_files()` | Saves uploaded PDFs     |
| `trigger_ingestion()`   | Calls backend ingestion |

📌 **This is the only place ingestion is triggered from UI**

---

## 3️⃣ `chat_ui_logic.py` — Chat UI & State

### Purpose

* Handles chat interaction logic
* Maintains conversation state

### Responsibilities

* Manage `st.session_state.messages`
* Display chat history
* Send user question to backend
* Display LLM response

### Key Function

| Function           | Description    |
| ------------------ | -------------- |
| `render_chat_ui()` | Main chat loop |

---

## 4️⃣ `ui_components.py` — Reusable UI Elements

### Purpose

* Keep UI clean and modular

### Examples

* Page headers
* Dividers
* Status messages

📌 **No business logic here**

---

# 🧠 Backend Layer — `src/core/`

This layer contains **all RAG intelligence**.

---

## ⚙️ Configuration — `core/config/`

### `settings.py`

### Purpose

* Central configuration file

### Contains

* API keys
* Base directory paths
* FAISS index directory
* Model names
* Chunk sizes

📌 **Single source of truth**

---

## 🧬 Embeddings & Vector Store — `core/embeddings/`

### `faiss_index.py`

### Purpose

* Handles FAISS index lifecycle
* Ensures embedding consistency

### Key Functions

| Step     | Function                               | Description           |
| -------- | -------------------------------------- | --------------------- |
| Shared   | `get_embeddings()`                     | Loads embedding model |
| Step 3   | `create_faiss_index(texts)`            | Creates FAISS index   |
| Step 4.1 | `load_faiss_index()`                   | Loads index from disk |
| Step 4.2 | `retrieve_similar_documents(query, k)` | Vector search         |

📌 **Same embedding model used for ingestion & query**

---

## 📥 Ingestion Pipeline — `core/ingestion/`

### `pdf_parser.py`

### Purpose

* Extracts raw text from PDFs

### Key Function

| Function                      | Description |
| ----------------------------- | ----------- |
| `extract_text_from_pdf(path)` | PDF → text  |

---

### `ingest.py`

### Purpose

* Orchestrates **PDF → FAISS**

### Step-by-Step Functions

| Step | Function         | Description             |
| ---- | ---------------- | ----------------------- |
| 3.1  | `get_all_pdfs()` | Scan PDF directory      |
| 3.2  | `chunk_text()`   | Split text into chunks  |
| 3.3  | `ingest_pdfs()`  | Full ingestion pipeline |

### What `ingest_pdfs()` Does

1. Finds PDFs
2. Extracts text
3. Chunks text
4. Creates FAISS index
5. Saves index to `data/faiss_index/`

---

## 🔍 Query Layer — `core/query/`

### `query_index.py`

### Purpose

* Bridge between user query and FAISS

### Key Function

| Function                 | Description             |
| ------------------------ | ----------------------- |
| `search_faiss(query, k)` | Returns relevant chunks |

📌 **No LLM calls here**

---

### `chat_model.py`

### Purpose

* Generates final answer using RAG

### Responsibilities

1. Receive user question
2. Retrieve relevant chunks
3. Build RAG prompt
4. Call LLM
5. Return answer

### Key Function

| Function                    | Description      |
| --------------------------- | ---------------- |
| `generate_answer(question)` | RAG-based answer |

📌 Enforces:

> “Answer ONLY using provided medical documents.”

---

## 🛠️ Utilities — `core/utils/`

### Purpose

* Shared helper utilities
* No core logic

(Currently optional / extensible)

---

# 🔄 End-to-End Workflow (Simple View)

| Stage           | File                | Responsibility |
| --------------- | ------------------- | -------------- |
| Upload PDFs     | `pdf_uploader.py`   | User uploads   |
| Extract text    | `pdf_parser.py`     | PDF → text     |
| Chunk text      | `ingest.py`         | Text → chunks  |
| Embed           | `faiss_index.py`    | Text → vectors |
| Store           | `data/faiss_index/` | Persist index  |
| Ask question    | `chat_ui_logic.py`  | User input     |
| Retrieve        | `query_index.py`    | Similar chunks |
| Generate answer | `chat_model.py`     | LLM response   |
| Display         | `chat_ui_logic.py`  | UI output      |

---

# ✅ Why This Architecture Is Strong

✔ Clean separation of concerns
✔ UI never touches FAISS
✔ Ingestion independent of querying
✔ Easily extensible (memory, citations, streaming)
✔ Production-grade RAG structure

---
