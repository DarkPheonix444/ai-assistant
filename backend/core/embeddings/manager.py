from pathlib import Path

from .chunker import Chunker
from .embedder import Embedder
from .vector_store import VectorStore
from .schema import ChunkMetadata


class EmbeddingManager:

    def __init__(
        self,
        chunker: Chunker,
        embedder: Embedder,
        vector_store: VectorStore
    ):

        self.chunker = chunker
        self.embedder = embedder
        self.vector_store = vector_store

    def index_file(
        self,
        file_path: str
    ) -> None:

        file_path = Path(file_path)

        text = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        chunks = self.chunker.chunk(text)
        if not chunks:
            return
        metadata = []

        for idx, chunk_text in enumerate(chunks):

            metadata.append(
                ChunkMetadata(
                    chunk_id=f"{file_path}_{idx}",
                    file_path=str(file_path),
                    text=chunk_text,
                    start_char=0,
                    end_char=0
                )
            )

        vectors = self.embedder.embed(
            chunks
        )
        print("\n========== DEBUG ==========")
        print("File:", file_path)
        print("Chunks:", len(chunks))
        print("Metadata:", len(metadata))
        print("Vectors Type:", type(vectors))
        print("Vectors Shape:", vectors.shape)
        print("===========================\n")


        self.vector_store.add(
            vectors,
            metadata
        )
    def index_project(
        self,
        files
        ) -> None:

        for file in files:

            self.index_file(
                str(file.path)
                )  
    def search(
        self,
        query: str,
        k: int = 5
    ):

        query_vector = self.embedder.embed_query(
            query
        )

        return self.vector_store.search(
            query_vector,
            k
        )