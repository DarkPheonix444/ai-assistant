import faiss
import pickle
import numpy as np
from pathlib import Path


class VectorStore:

    def __init__(self, dimension: int):

        self.dimension = dimension

        self.index = faiss.IndexFlatL2(
            dimension
        )

        self.metadata: list = []

    def add(
        self,
        vectors: np.ndarray,
        metadata: list
    ) -> None:

        vectors = vectors.astype(
            np.float32
        )

        self.index.add(vectors)

        self.metadata.extend(
            metadata
        )

    def search(
        self,
        query_vector: np.ndarray,
        k: int = 5
    ) -> list:

        query_vector = query_vector.astype(
            np.float32
        )

        distances, indices = self.index.search(
            query_vector.reshape(1, -1),
            k
        )

        results = []

        for idx in indices[0]:

            if idx == -1:
                continue

            if idx < len(self.metadata):

                results.append(
                    self.metadata[idx]
                )

        return results

    def save(
        self,
        index_path: str | Path,
        metadata_path: str | Path
    ) -> None:

        faiss.write_index(
            self.index,
            str(index_path)
        )

        with open(
            metadata_path,
            "wb"
        ) as file:

            pickle.dump(
                self.metadata,
                file
            )

    def load(
        self,
        index_path: str | Path,
        metadata_path: str | Path
    ) -> None:

        self.index = faiss.read_index(
            str(index_path)
        )

        with open(
            metadata_path,
            "rb"
        ) as file:

            self.metadata = pickle.load(
                file
            )

    def total_vectors(self) -> int:

        return self.index.ntotal

    def clear(self) -> None:

        self.index = faiss.IndexFlatL2(
            self.dimension
        )

        self.metadata.clear()