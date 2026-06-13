from pathlib import Path

from .scanner import ProjectScanner
from .tree_builder import TreeBuilder
from .schemas import ProjectMetadata
from .formatter import TreeFormatter


class ProjectLoader:

    def __init__(self):
        self.scanner = ProjectScanner()
        self.tree_builder = TreeBuilder()
        self.formatter = TreeFormatter()

    def load(self, root_path: str) -> ProjectMetadata:

        root = Path(root_path)

        files = self.scanner.scan(root_path)

        tree = self.tree_builder.build(files, root)
        tree_text = self.formatter.format(tree)
        
        return ProjectMetadata(
            root=root,
            files=files,
            total_files=len(files),
            tree=tree,
            tree_text=tree_text
        )