

# 📘 Multimodal Vector Search using ChromaDB

**Dataset:** *“Attention Is All You Need”* (Transformer paper)

---

## 🔍 What are we trying to build?

We want a system where you can ask questions like:

> *“What is the transformer architecture?”*
> *“Show me the attention diagram”*

…and the system will return:

* **Relevant text passages**
* **Relevant images (figures, diagrams)**
  from a **research paper PDF**.

This is called **multimodal retrieval** (text + images).

---

## 🧠 Core Idea (Big Picture)

Instead of keyword search:

* Convert **text → vectors**
* Convert **images → vectors**
* Store vectors in a **vector database**
* Search using **semantic similarity**

---

## 🧩 High-Level Architecture

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

---

## 🛠️ Technologies Used

| Component                        | Purpose                        |
| -------------------------------- | ------------------------------ |
| **PyMuPDF (fitz)**               | Extract text & images from PDF |
| **Pillow (PIL)**                 | Image handling                 |
| **Sentence-Transformers (CLIP)** | Multimodal embeddings          |
| **ChromaDB**                     | Vector database                |
| **Hugging Face**                 | Model hosting                  |

---

## 1️⃣ Why Vector Databases?

Traditional DBs store:

* strings
* numbers

Vector DBs store:

* **embeddings** (arrays of numbers)
* allow **semantic similarity search**

### Examples:

* ChromaDB
* FAISS
* Pinecone
* Weaviate
* Qdrant

---

## 2️⃣ Why CLIP?

CLIP (**Contrastive Language–Image Pretraining**) maps:

* text 📝
* images 🖼️

into **the same vector space**.

That means:

> Text query can retrieve images
> Image can retrieve text

Perfect for multimodal search.

---

## 3️⃣ Installation

```bash
pip install pymupdf sentence-transformers chromadb pillow numpy
```

---

## 4️⃣ Imports & Setup

```python
import os
import fitz  # PyMuPDF
import numpy as np
from PIL import Image
from typing import List, Dict, Any

from sentence_transformers import SentenceTransformer
import chromadb
```

---

## 5️⃣ Load CLIP Model (from Hugging Face)

```python
clip_model = SentenceTransformer("clip-ViT-B-32")
```

### What this model does:

* `encode(text)` → text embedding
* `encode(image)` → image embedding
* Output: same vector dimension

---

## 6️⃣ Embedding Functions (CRITICAL)

### Text Embedding

```python
def embed_text(text: str) -> np.ndarray:
    emb = clip_model.encode([text], convert_to_numpy=True)
    return emb[0]
```

### Image Embedding

```python
def embed_image(path: str) -> np.ndarray:
    img = Image.open(path).convert("RGB")
    emb = clip_model.encode([img], convert_to_numpy=True)
    return emb[0]
```

✅ **Same vector space**
✅ **Same embedding size**

---

## 7️⃣ Extract Text & Images from PDF

### Open PDF

```python
PDF_PATH = "attention is all you need.pdf"
doc = fitz.open(PDF_PATH)
```

---

### Extract Text Blocks

```python
text_chunks = []

for page_num, page in enumerate(doc):
    blocks = page.get_text("blocks")
    for b in blocks:
        text = b[4].strip()
        if len(text) > 50:
            text_chunks.append({
                "page": page_num,
                "text": text
            })
```

📌 **Why blocks?**
Blocks preserve layout better than raw text.

---

### Extract Images

```python
FIGURES_DIR = "figures"
os.makedirs(FIGURES_DIR, exist_ok=True)

image_metadata = []

for page_num, page in enumerate(doc):
    images = page.get_images(full=True)
    for img_index, img in enumerate(images):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]

        image_path = f"{FIGURES_DIR}/page{page_num}_img{img_index}.{image_ext}"
        with open(image_path, "wb") as f:
            f.write(image_bytes)

        image_metadata.append({
            "page": page_num,
            "path": image_path
        })
```

---

## 8️⃣ Caption Extraction Logic (Conceptual)

📌 Captions usually:

* Appear **below images**
* Start with “Figure X”

Logic:

1. Get image bounding box
2. Find nearest text block below
3. Assign as caption

(This is heuristic-based and imperfect — but practical)

---

## 9️⃣ Initialize ChromaDB

```python
client = chromadb.Client()
```

---

## 🔟 Create Two Separate Indexes

Why two?

| Index           | Reason                   |
| --------------- | ------------------------ |
| **Text Index**  | Optimized for paragraphs |
| **Image Index** | Optimized for figures    |

```python
text_collection = client.create_collection("paper_text")
image_collection = client.create_collection("paper_images")
```

---

## 1️⃣1️⃣ Store Text Embeddings

```python
for i, chunk in enumerate(text_chunks):
    emb = embed_text(chunk["text"])
    text_collection.add(
        ids=[f"text_{i}"],
        embeddings=[emb],
        documents=[chunk["text"]],
        metadatas=[{"page": chunk["page"]}]
    )
```

---

## 1️⃣2️⃣ Store Image Embeddings

```python
for i, img in enumerate(image_metadata):
    emb = embed_image(img["path"])
    image_collection.add(
        ids=[f"img_{i}"],
        embeddings=[emb],
        metadatas=[{
            "page": img["page"],
            "path": img["path"]
        }]
    )
```

---

## 1️⃣3️⃣ Query Function (THE HEART)

```python
def answer_query(
    query: str,
    top_k_text: int = 5,
    top_k_img: int = 5,
    top_k_overall: int = 8
) -> List[Dict[str, Any]]:

    q_emb = embed_text(query)

    text_results = text_collection.query(
        query_embeddings=[q_emb],
        n_results=top_k_text
    )

    img_results = image_collection.query(
        query_embeddings=[q_emb],
        n_results=top_k_img
    )

    combined = []

    for i in range(len(text_results["ids"][0])):
        combined.append({
            "type": "text",
            "content": text_results["documents"][0][i],
            "distance": text_results["distances"][0][i]
        })

    for i in range(len(img_results["ids"][0])):
        combined.append({
            "type": "image",
            "path": img_results["metadatas"][0][i]["path"],
            "distance": img_results["distances"][0][i]
        })

    combined.sort(key=lambda x: x["distance"])
    return combined[:top_k_overall]
```

---

## 1️⃣4️⃣ Example Query

```python
answer_query(
    "what is transformer architecture",
    top_k_text=2,
    top_k_img=1,
    top_k_overall=3
)
```

### Output:

* Text explaining self-attention
* Transformer block diagram image

---

## 🔁 Workflow Summary Diagram

```
PDF
 ├── Extract Text ──► Embed ──► Text Vector DB
 ├── Extract Images ─► Embed ──► Image Vector DB
 │
User Query
 └── Embed Query
       ├── Search Text DB
       ├── Search Image DB
       └── Merge + Rank Results
```

---

## 🚀 Model Improvements

Suggested upgrades:

* **EVA-CLIP** → better image understanding
* **BLIP / BLIP-2** → caption-aware embeddings
* **LayoutLM** → better PDF structure understanding

---

## 🔄 Alternative Vector Databases

| DB       | Strength        |
| -------- | --------------- |
| FAISS    | Fast local      |
| Pinecone | Managed cloud   |
| Weaviate | Schema + Graph  |
| Qdrant   | Rust, very fast |

---

## 🧠 Key Concepts You Learned

* What embeddings are
* Why vector databases matter
* How multimodal models work
* How to extract structured data from PDFs
* How RAG systems are built internally

---

## 🎯 Key Takeaways

✅ **Vector search beats keyword search**
✅ **CLIP enables cross-modal retrieval**
✅ **Data preparation matters more than models**
✅ **Separate indexes improve quality**
✅ **This is the foundation of ChatPDF systems**

---

## 🔮 What’s Next (Project)

Next class project:

* Multiple PDFs
* Chat interface
* Source citations
* CI/CD pipeline
* Production-ready RAG system

If you want, next I can:

* Draw this as a **proper architecture diagram**
* Convert this into a **README.md**
* Debug your current notebook line-by-line
* Extend this into a **chatbot UI**

Just tell me 👍

