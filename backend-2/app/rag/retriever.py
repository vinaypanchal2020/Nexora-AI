from app.rag.embedding import embed_query
from app.rag import vector_db


def retrieve_chunks(query: str, top_k: int = 3):
    # Convert the user query into a vector using the vectorizer that was
    # already fit on the uploaded document's chunks.
    query_embedding = embed_query(query)

    if vector_db.index is None:
        raise ValueError(
            "No document embeddings available for retrieval. Upload a file and try again."
        )

    # Search FAISS index for the top_k search results
    _, positions = vector_db.index.search(
        query_embedding.astype('float32'),
        top_k
    )

    # Get the original chunks
    results = []
    for pos in positions[0]:
        if pos != -1:
            results.append(vector_db.chunk_store[pos])

    return results