from .schema import ModelConfig


MODEL_REGISTRY = {

    "qwen_instruct": ModelConfig(

        name="qwen_instruct",

        model_type="planner",

        model_path=None,

        max_tokens=2048,

        temperature=0.2,

        is_available=False
    ),

    "qwen_coder": ModelConfig(

        name="qwen_coder",

        model_type="coder",

        model_path=None,

        max_tokens=4096,

        temperature=0.1,

        is_available=False
    ),

    "deepseek_coder": ModelConfig(

        name="deepseek_coder",

        model_type="coder",

        model_path=None,

        max_tokens=4096,

        temperature=0.1,

        is_available=False
    )
}