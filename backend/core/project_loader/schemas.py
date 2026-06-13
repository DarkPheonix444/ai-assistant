from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectFile:
    path: Path
    extension: str
    size: int


@dataclass
class ProjectMetadata:
    root: Path
    files: list[ProjectFile]
    total_files: int
    tree:dict
    tree_text: str 