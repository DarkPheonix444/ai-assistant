from .prompts import PLANNER_SYSTEM_PROMPT
from .schema import Plan, Todo

import json
import uuid


class PlannerAgent:

    def __init__(
        self,
        model_manager
    ):
        self.model_manager = model_manager

    def create_plan(
        self,
        user_request: str
    ):

        prompt = (
            PLANNER_SYSTEM_PROMPT
            + "\n\nUser Request:\n"
            + user_request
        )

        response = self.model_manager.generate(
            "planner",
            prompt
        )

        data = json.loads(response)

        todos = []

        for index, item in enumerate(
            data["todos"],
            start=1
        ):

            todos.append(
                Todo(
                    id=index,
                    title=item["title"],
                    description=item["description"]
                )
            )

        plan = Plan(
            task_id=str(uuid.uuid4()),
            user_request=user_request,
            todos=todos
        )

        return plan