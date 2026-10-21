"""
Text Embedding Module using Sentence-Transformers (all-MiniLM-L6-v2)
Author: Dilkhush Raj (https://github.com/Dilkhush144)
"""

import numpy as np
from sentence_transformers import SentenceTransformer

# Streamlit resource cache if available
try:
    import streamlit as st
    cache_decorator = st.cache_resource
except ImportError:
    def cache_decorator(func):
        return func


@cache_decorator
def load_embedding_model(model_name: str = "all-MiniLM-L6-v2") -> SentenceTransformer:
    """
    Loads and caches the SentenceTransformer model on CPU to ensure stable memory usage on free hosting tiers.
    """
    return SentenceTransformer(model_name, device="cpu")


def embed_single(text: str) -> np.ndarray:
    """
    Computes a normalized dense vector embedding for a given text snippet.
    """
    if not text or not text.strip():
        # Return a zero vector of dimension 384 for empty text
        return np.zeros(384, dtype=np.float32)

    model = load_embedding_model()
    # Normalize embedding vector to allow fast cosine similarity via dot product
    vector = model.encode([text], normalize_embeddings=True, show_progress_bar=False)[0]
    return np.asarray(vector, dtype=np.float32)
