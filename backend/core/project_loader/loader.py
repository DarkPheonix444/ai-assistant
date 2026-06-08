from pathlib import Path

from .scanner import ProjectScanner
from .tree_builder import TreeBuilder
from .schemas import ProjectMetadata


class ProjectLoader:

    def __init__(self):
        self.scanner = ProjectScanner()
        self.tree_builder = TreeBuilder()

    def load(self, root_path: str) -> ProjectMetadata:

        root = Path(root_path)

        files = self.scanner.scan(root_path)

        tree = self.tree_builder.build(files)

        return ProjectMetadata(
            root=root,
            files=files,
            total_files=len(files),
            tree=tree
        )