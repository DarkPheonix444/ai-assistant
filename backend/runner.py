import time

from core.models.manager import ModelManager

from agents.coder.coder import (
    CoderAgent
)

from executor.code_executor import (
    CodeExecutor
)

from tools.file_editor.editor import (
    FileEditor
)

from tools.file_editor.diff import (
    DiffGenerator
)

from tools.file_editor.backup import (
    BackupManager
)

from tools.file_editor.rollback import (
    RollbackManager
)

from tools.file_editor.transaction import (
    TransactionManager
)


PROJECT_ROOT = (
    r"C:\Users\kanan\Desktop\ai_testing"
)

total_start = time.time()

print("Loading model...")

model_manager = ModelManager()

coder = CoderAgent(
    model_manager
)

print("Model loaded")


backup_manager = BackupManager()

rollback_manager = RollbackManager()

transaction_manager = TransactionManager(
    backup_manager,
    rollback_manager
)

file_editor = FileEditor()

diff_generator = DiffGenerator()

executor = CodeExecutor(
    transaction_manager,
    file_editor,
    diff_generator
)

print("Executor loaded")

print("\nGenerating code...\n")

result = coder.generate_code(
    task_description=
    "Files do not exist. "
    "Create add.py with add(a,b). "
    "Create main.py. "
    "Import add from add.py. "
    "Print add(5,7).",
    context=
    f"Project root: {PROJECT_ROOT}"
)

print("\nExecuting...\n")

execution = executor.execute(
    result.files
)

for change in execution["changes"]:

    print(
        f"\nModified: {change['path']}"
    )

    print(
        change["diff"]
    )

print("\nUnloading model...")

model_manager.unload_model()

print(
    f"\nTotal Runtime: "
    f"{time.time() - total_start:.2f}s"
)