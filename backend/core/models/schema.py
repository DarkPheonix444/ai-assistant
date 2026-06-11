from dataclasses import dataclass


@dataclass
class ModelConfig:

    name: str

    model_type: str

    model_path: str

    context_window: int

    max_tokens: int

    temperature: float

    is_available: bool

    loaded: bool = False