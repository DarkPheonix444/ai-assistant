from core.models.manager import ModelManager

from agents.planner.planner import PlannerAgent

from state.task_state import TaskState

from agents.planner.schema import TodoStatus

from core.project_loader.loader import ProjectLoader


manager = ModelManager()

planner = PlannerAgent(manager)

state = TaskState()

loader = ProjectLoader()


project = loader.load(
    r"C:\Users\kanan\Desktop\ai-assistant\backend"
)

print("Creating plan...")

plan = planner.create_plan(
    "how would u add teh embedding to the planner agent",
    project.tree_text
)

print("\nGenerated Plan:")
print(plan)

print("\nSaving Plan...")
state.save_plan(plan)

print("Saved!")

state.update_todo_status(
    plan.task_id,
    1,
    TodoStatus.COMPLETED
)

loaded_plan = state.load_plan(
    plan.task_id
)

print("\nLoaded Plan:")
print(loaded_plan)

print("\nTodos:")

for todo in loaded_plan.todos:

    print(
        f"{todo.id}. "
        f"{todo.title} "
        f"[{todo.status}]"
    )

manager.unload_model()

print("\nDone")