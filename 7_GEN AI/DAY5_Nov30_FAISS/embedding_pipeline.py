"""
embedding_pipeline.py

Purpose:
---------
1. Define a long text (bio_text).
2. Split it into overlapping chunks for semantic processing.
3. Send each chunk to an embedding API to get vector representations.
4. Extract only the embedding vectors from the response.
5. Convert embeddings into a NumPy array for FAISS.
6. Build a FAISS index for semantic search.
7. Query the FAISS index with new text.

💡 Diagram Summary (Text Style):
---------------------------------
[ bio_text ] 
     |
     v
[ chunk_text() ] -> list of chunks
     |
     v
[ Embedding API ] -> list of embedding vectors (dicts)
     |
     v
[ Extract embeddings ] -> NumPy array of shape (num_chunks, embedding_dim)
     |
     v
[ FAISS Index ] <- add embeddings
     |
     v
[ Query text ] -> get_query_embedding() -> query_vector
     |
     v
[ FAISS search ] -> distances + indices
     |
     v
[ Retrieve top matching chunks from list of chunks ]
"""

# ==============================
# Imports
# ==============================
import requests
import numpy as np
import faiss

# ==============================
# 1. Function: Chunk Text
# ==============================
def chunk_text(text, chunk_size=20, overlap=3):
    """
    Splits text into smaller overlapping chunks.
    
    Args:
        text (str): input text
        chunk_size (int): number of words per chunk
        overlap (int): words to repeat between chunks
    
    Returns:
        list[str]: list of text chunks
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        start = start + chunk_size - overlap
    return chunks

# ==============================
# 2. Define Text
# ==============================
bio_text = """
Sudhanshu's commitment to affordable education wasn't just a business strategy—it was his life's mission.
Over the years, iNeuron has helped over 1.5 million students from 34+ countries, providing them with the
skills they need to succeed in today's competitive job market. Many of these students, like Sudhanshu
himself, came from disadvantaged backgrounds.

In 2022, iNeuron was acquired by PhysicsWallah in a deal worth ₹250 crore. While this acquisition was a
significant milestone, Sudhanshu remained focused on his mission. Even after the acquisition, iNeuron
continued to offer some of the most affordable and accessible tech courses in the world.

Sudhanshu's journey isn't just one of entrepreneurial success; it's also a story of dedication to teaching.
Throughout his career, he has remained a passionate educator, constantly looking for ways to empower others
through knowledge.
"""

# ==============================
# 3. Chunk the Text
# ==============================
chunks = chunk_text(bio_text, chunk_size=20, overlap=3)
print(f"Total chunks created: {len(chunks)}")
print("First chunk:\n", chunks[0])

# ==============================
# 4. Get Embeddings for Chunks
# ==============================
API_URL = "https://api.euron.one/api/v1/euri/embeddings"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer euri-cc3925dc19d652dcb0bd8aacaa7e3cb2fb7925101bf01ec565cf0b9e3cd66b4e"  # 🔴 Replace with your real key
}

data = {
    "input": chunks,
    "model": "text-embedding-3-small"
}

response = requests.post(API_URL, headers=headers, json=data)

# Convert list of dictionaries to list of lists because FAISS expects a list of vectors
embedding_result = response.json()["data"]          # list of embedding objects
embeddings = [item["embedding"] for item in embedding_result]
print("Number of embeddings:", len(embeddings))
print("Dimension of each embedding:", len(embeddings[0]))

# Convert to NumPy array for FAISS
embeddings_array = np.array(embeddings, dtype=np.float32)
print("Embeddings array shape:", embeddings_array.shape)

# ==============================
# 5. Build FAISS Index
# ==============================
faiss_index = faiss.IndexFlatL2(embeddings_array.shape[1])  # L2 distance
faiss_index.add(embeddings_array)
print("FAISS index created and embeddings added!")

# ==============================
# 6. Function: Get Query Embedding
# ==============================
def get_query_embedding(query_text):
    """
    Converts a query string into an embedding vector.
    Returns a NumPy array of shape (1, embedding_dim) ready for FAISS search.
    """
    data = {
        "input": [query_text],  # API expects a list
        "model": "text-embedding-3-small"
    }
    response = requests.post(API_URL, headers=headers, json=data)
    query_result = response.json()["data"]                  # list of embedding objects
    query_embeddings = [item["embedding"] for item in query_result]
    query_array = np.array(query_embeddings, dtype=np.float32).reshape(1, -1)
    return query_array

# ==============================
# 7. Query FAISS Index
# ==============================
query_text = "tell me about sudhanshu early life"
query_vector = get_query_embedding(query_text)

# Search top 2 similar chunks
distances, indices = faiss_index.search(query_vector, 2)

print("\nQuery:", query_text)
print("Indices of top 2 matching chunks:", indices)
print("Distances of top 2 matches:", distances)

# Print top matching chunks
for rank, idx in enumerate(indices[0]):
    print(f"\nRank {rank+1} chunk (index {idx}):")
    print(chunks[idx])
