import shutil
from uuid import uuid4


class TransactionManager:

    def __init__(
        self,
        backup_manager,
        rollback_manager
    ):

        self.backup_manager = (
            backup_manager
        )

        self.rollback_manager = (
            rollback_manager
        )

    def start(
        self,
        files: list[str]
    ):

        task_id = str(
            uuid4()
        )

        backup_dir = (
            self.backup_manager
            .create_backup(
                task_id,
                files
            )
        )

        return {
            "task_id": task_id,
            "backup_dir": backup_dir
        }

    def accept(
        self,
        backup_dir: str
    ):

        shutil.rmtree(
            backup_dir,
            ignore_errors=True
        )

    def reject(
        self,
        backup_dir: str
    ):

        self.rollback_manager.rollback(
            backup_dir
        )

        shutil.rmtree(
            backup_dir,
            ignore_errors=True
        )