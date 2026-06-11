from core.models.manager import ModelManager

manager = ModelManager()

print("Loading planner...")

response = manager.generate(
    "planner",
    "Reply only with hello"
)

print(response)

manager.unload_model()

print("Done")