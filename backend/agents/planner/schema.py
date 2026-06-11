from dataclasses import dataclass, field
from enum import Enum


class TodoStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class PlanStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Todo:

    id: int

    title: str

    description: str

    status: TodoStatus = TodoStatus.PENDING


@dataclass
class Plan:

    task_id: str

    user_request: str

    todos: list[Todo] = field(default_factory=list)

    current_todo: int = 0

    status: PlanStatus = PlanStatus.CREATED