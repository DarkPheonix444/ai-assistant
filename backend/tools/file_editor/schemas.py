from dataclasses import dataclass

@dataclass
class FileChange:

    file_path: str

    old_content: str

    new_content: str