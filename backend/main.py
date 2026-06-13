from core.project_loader.loader import ProjectLoader

from core.embeddings.chunker import Chunker
from core.embeddings.embedder import Embedder
from core.embeddings.vector_store import VectorStore
from core.embeddings.manager import EmbeddingManager
from core.embeddings.model_loader import (
    EmbeddingModelLoader
)


print("Loading project...")

loader = ProjectLoader()

project = loader.load(
    r"C:\Users\kanan\Desktop\ai-assistant\backend"
)

print(
    f"Files found: {project.total_files}"
)

print("\nLoading embedding model...")

model_loader = EmbeddingModelLoader()

model = model_loader.load()

embedder = Embedder(model)

print("Model loaded")

chunker = Chunker()

vector_store = VectorStore(
    dimension=384
)

embedding_manager = EmbeddingManager(
    chunker,
    embedder,
    vector_store
)

print("\nIndexing project...")

embedding_manager.index_project(
    project.files
)

print(
    f"Total vectors: "
    f"{vector_store.total_vectors()}"
)

print("\nSearching...")

results = embedding_manager.search(
    "How would you add embeddings to planner?",
    k=5
)

print("\nTop Results:\n")

for result in results:

    print(
        f"File: {result.file_path}"
    )

    print(
        f"Chunk ID: {result.chunk_id}"
    )

    print("-" * 50)

print("\nDone")