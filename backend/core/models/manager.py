import gc

from llama_cpp import Llama

from .registry import MODEL_REGISTRY


class ModelManager:

    def __init__(self):

        self.active_model = None

        self.active_model_name = None

    def load_model(
        self,
        model_name: str
    ) -> bool:

        if (
            self.active_model is not None
            and
            self.active_model_name == model_name
        ):
            return True

        self.unload_model()

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

        self.active_model = Llama(
            model_path=config.model_path,
            n_ctx=config.context_window,
            verbose=False
        )

        self.active_model_name = model_name

        config.loaded = True

        return True

    def unload_model(
        self
    ) -> bool:

        if self.active_model is None:
            return False

        config = MODEL_REGISTRY.get(
            self.active_model_name
        )

        if config:
            config.loaded = False

        self.active_model = None

        self.active_model_name = None

        gc.collect()

        return True

    def is_loaded(
        self,
        model_name: str
    ) -> bool:

        return (
            self.active_model_name == model_name
        )

    def get_model(self):

        return self.active_model

    def get_active_model_name(self):

        return self.active_model_name

    def generate(
        self,
        model_name: str,
        prompt: str
    ) -> str:

        self.load_model(
            model_name
        )

        config = MODEL_REGISTRY[
            model_name
        ]

        response = self.active_model.create_chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=config.temperature,
            max_tokens=config.max_tokens
        )

        return response["choices"][0]["message"]["content"]