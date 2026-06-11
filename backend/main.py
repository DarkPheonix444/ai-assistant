from core.models.manager import ModelManager

from agents.planner.planner import PlannerAgent

from state.task_state import TaskState
from agents.planner.schema import TodoStatus

manager = ModelManager()

planner = PlannerAgent(manager)

state = TaskState()


print("Creating plan...")

plan = planner.create_plan(
    "Create JWT authentication for a Django application"
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

print("\nLoading Plan...")
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
print(type(loaded_plan.status))
manager.unload_model()

print("\nDone")