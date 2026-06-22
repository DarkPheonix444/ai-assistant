import time

from core.models.manager import ModelManager

from agents.planner.planner import (
    PlannerAgent
)

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


total_start = time.time()


print("Loading models...")

model_manager = ModelManager()

planner = PlannerAgent(
    model_manager,
    None
)

coder = CoderAgent(
    model_manager
)

print("Models loaded")


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


print("\nGenerating plan...\n")

plan = planner.create_plan(
    user_request=
    "files are not  created you need to create them. "
    "Create add.py with add(a,b). "
    "Create main.py. "
    "Import add from add.py. "
    "Print add(5,7).",
    project_tree=""
)

print("\nPlan:\n")

for todo in plan.todos:

    print(
        f"{todo.id}. {todo.title}"
    )

    print(
        f"   {todo.description}"
    )

    print()


print("\nExecuting Todos...\n")

for todo in plan.todos:

    print(
        f"Processing: {todo.title}"
    )

    result = coder.generate_code(
        task_description=todo.description,
        context=""
    )

    execution = executor.execute(
        result.files
    )

    for change in execution[
        "changes"
    ]:

        print(
            f"\nModified: "
            f"{change['path']}"
        )

        print(
            change["diff"]
        )

        print()


print("\nUnloading model...")

model_manager.unload_model()

print(
    f"\nTotal Runtime: "
    f"{time.time() - total_start:.2f}s"
)