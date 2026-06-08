from pathlib import Path


class FileEditor:

    def read(
        self,
        file_path: str
    ) -> str:

        return Path(
            file_path
        ).read_text(
            encoding="utf-8",
            errors="ignore"
        )

    def write(
        self,
        file_path: str,
        content: str
    ) -> None:

        Path(
            file_path
        ).write_text(
            content,
            encoding="utf-8"
        )

    def exists(
    self,
    file_path: str
    ) -> bool:

        return Path(
            file_path
        ).exists()
    
    def delete(
    self,
    file_path: str
    ) -> None:

        path = Path(file_path)

        if path.exists():
            path.unlink()