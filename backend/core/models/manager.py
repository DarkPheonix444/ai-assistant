from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer
)

from .registry import MODEL_REGISTRY


class ModelManager:

    def __init__(self):

        self.loaded_models = {}

        self.loaded_tokenizers = {}

    def load_model(
        self,
        model_name: str
    ) -> bool:

        if model_name in self.loaded_models:
            return True

        config = MODEL_REGISTRY.get(
            model_name
        )

        if config is None:
            raise ValueError(
                f"Unknown model: {model_name}"
            )

        if not config.is_available:
            raise ValueError(
                f"Model not available: {model_name}"
            )

        tokenizer = AutoTokenizer.from_pretrained(
            config.model_path
        )

        model = AutoModelForCausalLM.from_pretrained(
            config.model_path
        )

        self.loaded_models[
            model_name
        ] = model

        self.loaded_tokenizers[
            model_name
        ] = tokenizer

        config.loaded = True

        return True

    def unload_model(
        self,
        model_name: str
    ) -> bool:

        if model_name not in self.loaded_models:
            return False

        del self.loaded_models[
            model_name
        ]

        del self.loaded_tokenizers[
            model_name
        ]

        config = MODEL_REGISTRY.get(
            model_name
        )

        if config:
            config.loaded = False

        return True

    def is_loaded(
        self,
        model_name: str
    ) -> bool:

        return (
            model_name
            in self.loaded_models
        )

    def get_model(
        self,
        model_name: str
    ):

        return self.loaded_models.get(
            model_name
        )

    def get_tokenizer(
        self,
        model_name: str
    ):

        return self.loaded_tokenizers.get(
            model_name
        )