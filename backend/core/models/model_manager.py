from sentence_transformers import SentenceTransformer

from .registry import MODELS


class ModelManager:

    def __init__(self):

        self.loaded_models = {}

    def load_model(
        self,
        model_name: str
    ):

        if model_name in self.loaded_models:
            return self.loaded_models[model_name]

        config = MODELS[model_name]

        if config.model_type == "sentence_transformer":

            model = SentenceTransformer(
                config.model_path
            )

        else:

            raise ValueError(
                f"Unsupported model type: "
                f"{config.model_type}"
            )

        self.loaded_models[
            model_name
        ] = model

        return model

    def get_model(
        self,
        model_name: str
    ):

        return self.loaded_models.get(
            model_name
        )

    def unload_model(
        self,
        model_name: str
    ):

        if model_name in self.loaded_models:

            del self.loaded_models[
                model_name
            ]

    def is_loaded(
        self,
        model_name: str
    ) -> bool:

        return (
            model_name
            in self.loaded_models
        )