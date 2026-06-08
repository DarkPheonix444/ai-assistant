import subprocess
import time

from .schemas import CommandResult


class TerminalRunner:

    def run(
        self,
        command: str,
        cwd: str | None = None
    ) -> CommandResult:

        start_time = time.time()

        try:

            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=60
            )

            execution_time = (
                time.time() -
                start_time
            )

            return CommandResult(

                success=(
                    result.returncode == 0
                ),

                stdout=result.stdout,

                stderr=result.stderr,

                exit_code=result.returncode,

                execution_time=execution_time,

                command=command
            )

        except subprocess.TimeoutExpired:

            execution_time = (
                time.time() -
                start_time
            )

            return CommandResult(

                success=False,

                stdout="",

                stderr="Command timed out",

                exit_code=-2,

                execution_time=execution_time,

                command=command
            )

        except Exception as error:

            execution_time = (
                time.time() -
                start_time
            )

            return CommandResult(

                success=False,

                stdout="",

                stderr=str(error),

                exit_code=-1,

                execution_time=execution_time,

                command=command
            )