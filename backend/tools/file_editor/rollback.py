import json
import shutil

from pathlib import Path


class RollbackManager:

    def rollback(
        self,
        backup_dir: str
    ) -> bool:

        backup_dir = Path(
            backup_dir
        )

        manifest_file = (
            backup_dir /
            "manifest.json"
        )

        if not manifest_file.exists():
            return False

        with open(
            manifest_file,
            "r",
            encoding="utf-8"
        ) as file:

            manifest = json.load(
                file
            )

        for file_info in manifest["files"]:

            original_path = Path(
                file_info["original"]
            )

            backup_file = (
                backup_dir /
                Path(
                    file_info["backup"]
                )
            )

            if backup_file.exists():

                shutil.copy2(
                    backup_file,
                    original_path
                )

        return True