
# 📘 Multimodal Vector Search using ChromaDB

### Text + Image Semantic Retrieval from Research PDFs

**Dataset:** *“Attention Is All You Need”* (Transformer paper)

---

## 1️⃣ What Are We Trying to Build?

We are building a system that allows **natural language questions** over a research PDF, such as:

* *“What is the transformer architecture?”*
* *“Show me the attention diagram”*

…and returns:

* 📄 **Relevant text passages**
* 🖼️ **Relevant images (figures, diagrams)**

This is called **multimodal semantic retrieval** — retrieving **text + images** using **meaning**, not keywords.

---

## 2️⃣ Core Idea (Big Picture)

Traditional search:

* Keyword-based
* Exact word matching
* No understanding of meaning

Our system:

1. Convert **text → vectors**
2. Convert **images → vectors**
3. Store vectors in a **vector database**
4. Search using **semantic similarity**

> If two things mean the same thing, their vectors will be close — even if the words differ.

---

## 3️⃣ High-Level Architecture

```
PDF
 │
 ├── Text chunks ──► Text Embeddings ──► Text Vector Index
 │
 └── Images ───────► Image Embeddings ─► Image Vector Index
                           ▲
                           │
                    CLIP Model
                           │
User Query (text) ──► Query Embedding
                           │
                 Semantic Search (Similarity)
                           │
                   Ranked Results (Text + Images)
```

### Key Insight

* Text and images are **separate modalities**
* A **single model (CLIP)** connects them
* One text query can retrieve **both text and images**

---

## 4️⃣ Technologies Used

| Component                    | Purpose                    |
| ---------------------------- | -------------------------- |
| PyMuPDF (fitz)               | Layout-aware PDF parsing   |
| Pillow (PIL)                 | Image loading & processing |
| Sentence-Transformers (CLIP) | Multimodal embeddings      |
| ChromaDB (Cloud)             | Vector database            |
| Hugging Face                 | Model hosting              |

---

## 5️⃣ Why Vector Databases?

Traditional databases store:

* Strings
* Numbers
* Rows & columns

Vector databases store:

* **Embeddings** (high-dimensional vectors)
* Optimized similarity indexes (ANN)

They enable:

* Semantic search
* Fast similarity queries
* Scalable retrieval

### Popular Vector Databases

* ChromaDB
* FAISS
* Pinecone
* Weaviate
* Qdrant

---

## 6️⃣ Why CLIP?

CLIP (**Contrastive Language–Image Pretraining**) embeds:

* 📝 Text
* 🖼️ Images

into the **same vector space**.

### Why this matters

* Text → Image retrieval
* Image → Text retrieval
* Cross-modal semantic search

This is the **core enabler** of multimodal systems.

---

## 7️⃣ Project Structure (Fully Explained)

```
chroma_multimodal_app/
├── pyproject.toml
├── README.md
├── .env
├── data/
│   └── attention_is_all_you_need.pdf
├── figures/
├── src/
│   └── core/
│       ├── config/
│       │   └── settings.py
│       ├── embeddings/
│       │   └── clip_embeddings.py
│       ├── ingestion/
│       │   ├── pdf_parser.py
│       │   └── ingest.py
│       ├── query/
│       │   ├── query_index.py
│       │   └── ask.py
│       ├── utils/
│       │   ├── chroma_client.py
│       │   └── file_utils.py
│       └── main.py
└── tests/
```

### Why this structure?

* Clear separation of concerns
* Scales cleanly to large systems
* Production-grade organization

---

## 8️⃣ Configuration & Environment

### `.env`

Stores secrets:

* Chroma API key
* Tenant
* Database name

### `settings.py`

Centralized configuration:

* PDF path
* Figures directory
* Model name (`clip-ViT-B-32`)
* Collection names
* Text length thresholds

---

## 9️⃣ PDF Parsing (Why Layout Matters)

We extract text using:

```python
page.get_text("blocks")
```

Each block contains:

* Bounding box `(x0, y0, x1, y1)`
* Text content

### Why blocks?

* Preserve layout
* Maintain paragraphs
* Enable caption detection
* Support explainability

---

## 🔟 Text Chunk Extraction

### Steps

1. Iterate pages
2. Extract text blocks
3. Clean text
4. Skip short/noisy chunks
5. Store metadata

### Metadata Stored

* Page number
* Bounding box
* Original text

This enables grounding and UI highlighting.

---

## 1️⃣1️⃣ Image Extraction

Using:

```python
page.get_images(full=True)
```

### Steps

1. Extract image bytes
2. Save to `/figures`
3. Record bounding boxes
4. Store metadata

Images become **searchable entities**, not just files.

---

## 1️⃣2️⃣ Caption Extraction Logic

### Why captions matter

Images alone lack semantic meaning.

### Heuristic

1. Get image bounding box
2. Find text blocks **below** the image
3. Choose the closest vertically
4. Assign as caption

This heuristic is imperfect but **works well for academic PDFs**.

---

## 1️⃣3️⃣ CLIP Embeddings

### Model

```
clip-ViT-B-32
```

### Embedding Functions

* `embed_text(text)`
* `embed_image(image_path)`

Both produce vectors in:

* Same dimension
* Same semantic space

---

## 1️⃣4️⃣ ChromaDB Collections

Two collections:

| Collection | Purpose                   |
| ---------- | ------------------------- |
| Text       | Paragraph-level semantics |
| Images     | Visual semantics          |

Stored in **Chroma Cloud**.

---

## 1️⃣5️⃣ Ingestion Pipeline

Implemented in `ingest.py`.

### Steps

1. Load PDF
2. Extract text & images
3. Generate embeddings
4. Upload to ChromaDB with metadata

This is an **offline process**.

---

## 1️⃣6️⃣ Query Pipeline (Core Logic)

Implemented in `query_index.py`.

### Flow

1. User query → text
2. Embed query using CLIP
3. Search text collection
4. Search image collection
5. Merge results
6. Rank by similarity

---

## 1️⃣7️⃣ CLI Query Interface

`ask.py` provides:

* Command-line querying
* Debugging & demos
* Developer-friendly testing

---

## 1️⃣8️⃣ End-to-End Workflow

```
[Ingestion]
PDF → parse → embed → ChromaDB

[Query]
Query → embed → search → merge → rank → results
```

---

## 1️⃣9️⃣ Architecture Patterns Used

* Multimodal indexing
* Vector similarity search
* Metadata-aware retrieval
* Retrieval-Augmented Generation (RAG foundation)

---

## 2️⃣0️⃣ Model Improvements (Suggested Upgrades)

| Model         | Benefit                            |
| ------------- | ---------------------------------- |
| EVA-CLIP      | Better image understanding         |
| BLIP / BLIP-2 | Caption-aware embeddings           |
| LayoutLM      | Strong PDF structure understanding |

The system is **model-agnostic**.

---

## 2️⃣1️⃣ Alternative Vector Databases

| Database | Strength          |
| -------- | ----------------- |
| FAISS    | Fast local search |
| Pinecone | Managed cloud     |
| Weaviate | Schema + graph    |
| Qdrant   | Rust, very fast   |

---

## 2️⃣2️⃣ Key Concepts You Learned

* Embeddings & vector spaces
* Semantic vs keyword search
* Multimodal retrieval
* PDF layout understanding
* Metadata-driven AI systems
* Real-world RAG architectures

---

## 2️⃣3️⃣ Key Takeaways

✅ Vector search beats keyword search
✅ CLIP enables cross-modal retrieval
✅ Data preparation matters more than models
✅ Separate indexes improve quality
✅ This is the foundation of **ChatPDF systems**

---

## 2️⃣4️⃣ Final Mental Model

> Everything becomes vectors.
> Queries become vectors.
> Similar vectors mean similar meaning.

---

## 2️⃣5️⃣ Why This Project Matters

This architecture is used in:

* ChatPDF systems
* Enterprise document search
* Legal & medical RAG pipelines
* Multimodal AI assistants

