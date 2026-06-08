from dataclasses import dataclass


@dataclass
class ChunkMetadata:

    chunk_id: str

    file_path: str

    text: str

    start_char: int

    end_char: int