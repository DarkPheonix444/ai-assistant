from .schema import ModelConfig


MODELS = {

    "embedding": ModelConfig(
        name="embedding",
        model_type="sentence_transformer",
        model_path="BAAI/bge-small-en-v1.5"
    )

}