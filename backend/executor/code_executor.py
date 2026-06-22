from tools.file_editor.editor import FileEditor
from tools.file_editor.diff import DiffGenerator


class CodeExecutor:

    def __init__(
        self,
        transaction_manager,
        file_editor: FileEditor,
        diff_generator: DiffGenerator
    ):

        self.transaction_manager = (
            transaction_manager
        )

        self.file_editor = (
            file_editor
        )

        self.diff_generator = (
            diff_generator
        )

    def execute(
        self,
        files
    ):

        existing_files = []

        for file in files:

            if self.file_editor.exists(
                file.path
            ):

                existing_files.append(
                    file.path
                )

        transaction = (
            self.transaction_manager.start(
                existing_files
            )
        )

        changes = []

        for file in files:

            if self.file_editor.exists(
                file.path
            ):

                old_content = (
                    self.file_editor.read(
                        file.path
                    )
                )

            else:

                old_content = ""

            self.file_editor.write(
                file.path,
                file.content
            )

            diff = (
                self.diff_generator.generate(
                    old_content,
                    file.content
                )
            )

            changes.append(
                {
                    "path": file.path,
                    "diff": diff
                }
            )

        return {
            "task_id":
            transaction["task_id"],

            "backup_dir":
            transaction["backup_dir"],

            "changes":
            changes
        }

    def accept(
        self,
        backup_dir: str
    ):

        self.transaction_manager.accept(
            backup_dir
        )

    def reject(
        self,
        backup_dir: str
    ):

        self.transaction_manager.reject(
            backup_dir
        )