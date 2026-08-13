from sklearn.feature_extraction.text import TfidfVectorizer

# Kept as module-level state on purpose: this app processes ONE uploaded
# document at a time (see vector_db.py), so the vectorizer only needs to
# know the vocabulary of the current document.
_vectorizer = None


def create_embeddings(chunks: list[str]):
    """
    Fit a fresh TF-IDF vectorizer on a document's chunks and return their
    vectors. Call this once per uploaded document (this happens inside
    rag_chat in pipeline.py).

    Replaces the old sentence-transformers/torch model, which pulled in
    500MB+ of PyTorch/CUDA packages and OOM-killed the app on Render's
    512MB free tier. TF-IDF is lexical (keyword-based) rather than semantic,
    so it won't catch pure synonyms/paraphrases as well as a transformer
    embedding model would -- but for small, single-document RAG it works
    fine and uses only a few MB of RAM.
    """
    global _vectorizer
    _vectorizer = TfidfVectorizer()
    embeddings = _vectorizer.fit_transform(chunks)
    return embeddings.toarray().astype("float32")


def embed_query(query: str):
    """
    Embed a single query using the vectorizer that was fit on the most
    recently uploaded document. Must be called AFTER create_embeddings()
    has run at least once.
    """
    if _vectorizer is None:
        raise ValueError(
            "No document embeddings available for retrieval. Upload a file and try again."
        )
    embeddings = _vectorizer.transform([query])
    return embeddings.toarray().astype("float32")
