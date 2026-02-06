
## ✅ Step 2.1 — Initialize Poetry (dependency-only mode)

From **inside the project root** (`medical_genai_app`):

```cmd
poetry init
```

During prompts:

* Project name → `medical-genai-app`
* Version → `0.1.0`
* Description → anything
* Author → optional
* Dependencies → **NO**
* Dev dependencies → **NO**
* Confirm → **YES**

This only creates metadata — **we will fix it next**.

---

## ✅ Step 2.2 — FIX `pyproject.toml` (CRITICAL)

Open the file your `.bat` created:

```cmd
notepad pyproject.toml
```

### 🔥 DELETE EVERYTHING and paste this exactly

```toml
[tool.poetry]
name = "medical-genai-app"
version = "0.1.0"
description = "GenAI application with FAISS, LangChain, Streamlit"
authors = ["your-name <you@email.com>"]
readme = "README.md"

# IMPORTANT: this is an APPLICATION, not a library
package-mode = false

[tool.poetry.dependencies]
# FAISS + Torch compatibility
python = ">=3.10,<3.15"

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```

### ✅ CHECK THESE (NON-NEGOTIABLE)

* ❌ NO `[project]`
* ❌ NO `packages = [...]`
* ❌ NO `^3.10`
* ✅ `package-mode = false`
* ✅ `<3.15` (FAISS safety)

Save and close.

---

## ✅ Step 2.3 — Sync lock file & environment

```cmd
poetry lock
poetry install
```

Expected:

* ✔ no “Installing current project”
* ✔ no package errors
* ✔ virtualenv created

If you see:

```
pyproject.toml changed significantly
```

→ this step already fixes it.

---

# 🧪 PART 3 — ENVIRONMENT SANITY CHECK

Run:

```cmd
poetry run python
```

Inside Python:

```python
import sys
print(sys.version)
exit()
```

✔ Python is 3.10–3.14
✔ Poetry environment works

---

# 📦 PART 4 — DEPENDENCY INSTALL ORDER (REFERENCE)

Now you start layering the stack **on top of your existing structure**.

### 🔹 Layer 1 — embeddings + vector DB

```cmd
poetry add sentence-transformers faiss-cpu
```

### 🔹 Layer 2 — PDF ingestion

```cmd
poetry add pypdf fpdf
```

### 🔹 Layer 3 — LangChain

```cmd
poetry add langchain langchain-community
```

### 🔹 Layer 4 — LLM provider

```cmd
poetry add euriai
```

### 🔹 Layer 5 — UI

```cmd
poetry add streamlit
```

👉 **Never install all at once** — this order matters.

---

# ▶️ PART 5 — How THIS PROJECT is run

### Python modules

```cmd
poetry run python src/core/main.py
```

### Streamlit app

```cmd
poetry run streamlit run src/app/streamlit_app.py
```

Imports inside code should be like:

```python
from core.utils.vector_store import FaissVectorStore
from core.llms.euriai_client import EuriAIClient
```

Your `__init__.py` loop in the `.bat` already guarantees this works ✅

---

# 🧠 COMMON ERRORS (AND FIXES)

### ❌ `No file/folder found for package`

✔ You already fixed this with:

```toml
package-mode = false
```

---

### ❌ `faiss-cpu forbidden`

✔ You already fixed this with:

```toml
python = ">=3.10,<3.15"
```

---

### ❌ Lock mismatch

```cmd
poetry lock
poetry install
```

---

# 🏁 FINAL STATUS

With:

* your **`.bat`**
* this **Part 2 Poetry setup**
* controlled dependency layering

You now have a **repeatable, future-proof GenAI project template**.

---

