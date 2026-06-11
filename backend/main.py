from core.models.manager import ModelManager

from agents.planner.planner import PlannerAgent
import time 

start_time=time.perf_counter()
manager = ModelManager()

planner = PlannerAgent(manager)

plan = planner.create_plan(
    "Create JWT authentication for a Django application"
)
End_time = time.perf_counter()

execution = End_time-start_time

print(plan)
print(f"Execution time: {execution} seconds")