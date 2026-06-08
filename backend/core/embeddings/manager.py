from pathlib import Path

from .chunker import Chunker
from .embedder import Embedder
from .vector_store import VectorStore
from .schemas import ChunkMetadata


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

        self.vector_store.add(
            vectors,
            metadata
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