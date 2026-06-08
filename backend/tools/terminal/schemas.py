from dataclasses import dataclass


@dataclass
class CommandResult:

    success: bool

    stdout: str

    stderr: str

    exit_code: int

    execution_time: float

    command: str