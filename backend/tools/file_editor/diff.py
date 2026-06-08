import difflib

class DiffGenerator:

    def generate(
        self,
        old_content: str,
        new_content: str
    ):

        return "\n".join(
            difflib.unified_diff(
                old_content.splitlines(),
                new_content.splitlines(),
                lineterm=""
            )
        )