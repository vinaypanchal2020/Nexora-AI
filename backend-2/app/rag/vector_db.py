import faiss
import numpy as np

# Holds the FAISS index that stores the embedding vectors.
index = None

# List of original text pieces that match each vector row in `index`.
chunk_store = []


def store_embeddings(chunks, embeddings):
    global index, chunk_store

    # Save the original text chunks so we can find text from vectors.
    chunk_store = chunks

    # Convert input to float32 numpy array because FAISS needs float32.
    embeddings = np.array(embeddings).astype('float32')

    # Get the vector size (number of dimensions) from embeddings.
    dimension = embeddings.shape[1]

    # Make a simple exact-search index using L2 distance.
    index = faiss.IndexFlatL2(dimension)

    # Put all vectors into the index in the same order as `chunk_store`.
    index.add(embeddings)

    return index