import json
import shutil

from pathlib import Path


class BackupManager:

    def __init__(
        self,
        backup_root: str = "temp_backups"
    ):

        self.backup_root = Path(
            backup_root
        )

        self.backup_root.mkdir(
            parents=True,
            exist_ok=True
        )

    def create_backup(
        self,
        task_id: str,
        files: list[str]
    ) -> str:

        backup_dir = (
            self.backup_root /
            f"backup_{task_id}"
        )

        backup_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        manifest = {
            "task_id": task_id,
            "files": []
        }

        for file_path in files:

            source = Path(file_path)

            if not source.exists():
                continue
            try:

                relative_path = source.relative_to(
                    source.anchor
                )

            except ValueError:

                relative_path = source

            destination = (
                backup_dir /
                relative_path
            )

            destination.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            shutil.copy2(
                source,
                destination
            )

            manifest["files"].append(
                {
                    "original": str(source),
                    "backup": str(relative_path)
                }
            )

        with open(
            backup_dir / "manifest.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                manifest,
                file,
                indent=4
            )

        return str(
            backup_dir
        )