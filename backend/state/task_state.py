from agents.planner.schema import (
    Plan,
    Todo,
    TodoStatus,
    PlanStatus
)

from dataclasses import asdict
import json
from pathlib import Path


class TaskState:

    def __init__(self):

        self.storage_dir = Path("state/plans")

        self.storage_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def save_plan(
        self,
        plan: Plan
    ):

        file_path = (
            self.storage_dir /
            f"{plan.task_id}.json"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                asdict(plan),
                file,
                indent=4
            )

    def load_plan(
        self,
        task_id: str
    ):

        file_path = (
            self.storage_dir /
            f"{task_id}.json"
        )

        if not file_path.exists():

            raise FileNotFoundError(
                f"Plan not found: {task_id}"
            )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        todos = []

        for item in data["todos"]:

            todos.append(
                Todo(
                    id=item["id"],
                    title=item["title"],
                    description=item["description"],
                    status=TodoStatus(
                        item["status"]
                    )
                )
            )

        return Plan(
            task_id=data["task_id"],
            user_request=data["user_request"],
            todos=todos,
            current_todo=data["current_todo"],
            status=PlanStatus(
                data["status"]
            )
        )

    def update_todo_status(
        self,
        task_id: str,
        todo_id: int,
        status: TodoStatus
    ):

        plan = self.load_plan(
            task_id
        )

        for todo in plan.todos:

            if todo.id == todo_id:

                todo.status = status

                break

        self.save_plan(plan)

    def get_current_todo(
        self,
        task_id: str
    ):

        plan = self.load_plan(
            task_id
        )

        if (
            plan.current_todo >=
            len(plan.todos)
        ):

            return None

        return plan.todos[
            plan.current_todo
        ]