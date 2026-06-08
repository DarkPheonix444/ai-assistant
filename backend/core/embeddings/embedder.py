from typing import Protocol
import numpy as np


class EmbeddingModel(Protocol):

    def encode(
        self,
        texts: list[str] | str,
        **kwargs
    ) -> np.ndarray:
        ...


class Embedder:

    def __init__(self, model: EmbeddingModel | None = None):
        self.model = model

    def set_model(self, model: EmbeddingModel) -> None:
        self.model = model

    def embed(self, texts: list[str]) -> np.ndarray:

        if self.model is None:
            raise ValueError(
                "Embedding model not loaded"
            )

        return self.model.encode(texts)

    def embed_query(self, query: str) -> np.ndarray:

        if self.model is None:
            raise ValueError(
                "Embedding model not loaded"
            )

        return self.model.encode(query)