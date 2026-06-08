from dataclasses import dataclass


@dataclass
class ModelConfig:

    name: str

    model_type: str

    model_path: str