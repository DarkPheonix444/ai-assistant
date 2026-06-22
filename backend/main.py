import time

from core.project_loader.loader import ProjectLoader

from core.embeddings.chunker import Chunker
from core.embeddings.embedder import Embedder
from core.embeddings.vector_store import VectorStore
from core.embeddings.manager import EmbeddingManager
from core.embeddings.model_loader import (
    EmbeddingModelLoader
)

from core.models.manager import ModelManager

from agents.planner.planner import (
    PlannerAgent
)

total_start = time.time()


print("Loading project...")

t = time.time()

loader = ProjectLoader()

project = loader.load(
    r"C:\Users\kanan\Desktop\ai-assistant\backend"
)

print(
    f"Files found: {project.total_files}"
)

print(
    f"Project Load Time: "
    f"{time.time() - t:.2f}s"
)



print("\nLoading embedding model...")

t = time.time()

model_loader = EmbeddingModelLoader()

model = model_loader.load()

embedder = Embedder(model)

print("Model loaded")

print(
    f"Embedding Model Load Time: "
    f"{time.time() - t:.2f}s"
)



t = time.time()

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

print(
    f"Indexing Time: "
    f"{time.time() - t:.2f}s"
)


print("\nLoading planner model...")

t = time.time()

model_manager = ModelManager()

planner = PlannerAgent(
    model_manager,
    embedding_manager
)

print("Planner loaded")

print(
    f"Planner Init Time: "
    f"{time.time() - t:.2f}s"
)


print("\nGenerating plan...")

t = time.time()

plan = planner.create_plan(
    user_request=
    "Create add.py with add(a,b). "
    "Create main.py. "
    "Import add from add.py. "
    "Print add(5,7).",
    project_tree=project.tree_text
)

print(
    f"Plan Generation Time: "
    f"{time.time() - t:.2f}s"
)


print("\nGenerated Plan:\n")

for todo in plan.todos:

    print(
        f"{todo.id}. {todo.title}"
    )

    print(
        f"   {todo.description}"
    )

    print()


t = time.time()

model_manager.unload_model()

print(
    f"Model Unload Time: "
    f"{time.time() - t:.2f}s"
)


print("\nDone")

print(
    f"Total Runtime: "
    f"{time.time() - total_start:.2f}s"
)