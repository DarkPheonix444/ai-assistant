from .prompts import PLANNER_SYSTEM_PROMPT
from .schema import Plan, Todo

import json
import uuid


class PlannerAgent:

    def __init__(
        self,
        model_manager,
        embedding_manager
    ):
        self.model_manager = model_manager
        self.embedding_manager = embedding_manager

    def create_plan(
        self,
        user_request: str,
        project_tree: str
    ):

        results = self.embedding_manager.search(
            user_request,
            k=10
        )

        print("\n===== RETRIEVED CONTEXT =====\n")

        for result in results:

            print(
                f"\nFILE: {result.file_path}\n"
            )

            print(result.text)

            print(
                "\n" + "=" * 60 + "\n"
            )

        retrieved_context = ""

        for result in results:

            retrieved_context += (
                f"\nFile: {result.file_path}\n"
                f"{result.text}\n"
            )

        prompt = (
            PLANNER_SYSTEM_PROMPT
            + "\n\nRepository Structure:\n"
            + project_tree
            + "\n\nRelevant Code:\n"
            + retrieved_context
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