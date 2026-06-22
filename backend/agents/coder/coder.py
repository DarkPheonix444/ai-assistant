from .prompts import CODER_SYSTEM_PROMPT
from .schema import (
    CodeFile,
    CodeResponse
)

import json


class CoderAgent:

    def __init__(
        self,
        model_manager
    ):
        self.model_manager = model_manager

    def generate_code(
        self,
        task_description: str,
        context: str
    ) -> CodeResponse:

        prompt = (
            CODER_SYSTEM_PROMPT
            + "\n\nTask:\n"
            + task_description
            + "\n\nRelevant Code:\n"
            + context
        )

        response = self.model_manager.generate(
            "coder",
            prompt
        )

        data = json.loads(
            response
        )

        files = []

        for item in data["files"]:

            files.append(
                CodeFile(
                    path=item["path"],
                    content=item["content"]
                )
            )

        return CodeResponse(
            files=files
        )