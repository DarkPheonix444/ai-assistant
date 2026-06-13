from pathlib import Path
from .schemas import ProjectFile


class ProjectScanner:

    ignore_dirs = {'.git', 'node_modules', '__pycache__','venv','.vscode','.idea'}

    def scan(self, root_path: Path) -> list[ProjectFile]:

        root=Path(root_path)

        files=[]

        for path in root.rglob('*'):
            if not path.is_file():
                continue

            if any(part in self.ignore_dirs for part in path.parts):
                continue

            files.append(
                ProjectFile(
                    path=path,
                    extension=path.suffix,
                    size=path.stat().st_size    

            
                )
            )
        return files
    

    