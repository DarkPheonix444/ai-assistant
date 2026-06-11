from agents.planner.schema import   Plan,Todo,TodoStatus
class TaskState:

    def save_plan(
        self,
        plan: Plan
    ):
        pass

    def load_plan(
        self,
        task_id: str
    ):
        pass

    def update_todo_status(
        self,
        task_id: str,
        todo_id: int,
        status: TodoStatus
    ):
        pass

    def get_current_todo(
        self,
        task_id: str
    ):
        pass