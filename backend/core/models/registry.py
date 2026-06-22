from .schema import ModelConfig


MODEL_REGISTRY = {

    "planner": ModelConfig(
        name="planner",
        model_type="planner",
        model_path="models\planner\qwen2.5-7b-instruct-q5_k_m-00001-of-00002.gguf",
        context_window=8192,
        max_tokens=1024,
        temperature=0.2,
        is_available=True
    ),

    "coder": ModelConfig(
        name="coder",
        model_type="coder",
        model_path="models\coder\qwen2.5-coder-7b-instruct-q5_k_m.gguf",
        context_window=8192,
        max_tokens=4096,
        temperature=0.1,
        is_available=True
    ),

    "reviewer": ModelConfig(
        name="reviewer",
        model_type="reviewer",
        model_path="models/qwen2.5-7b-instruct.gguf",
        context_window=8192,
        max_tokens=2048,
        temperature=0.0,
        is_available=False
    )
}