import subprocess, os
from enum import Enum
from alfred.api.loggers import get_logger

logger = get_logger()

class shell_type(Enum):
    bash = ["/bin/bash", "-c"],
    powershell = ["powershell", "-Command"],
    cmd = ["cmd", "/c"]

class Shell():
    @staticmethod
    def process(env, command):
        try:
            result = subprocess.run(env + [command], text=True, capture_output=True)
            if result.returncode != 0:
                logger.error(f"Command failed with error: {result.stderr.strip()}")
                raise RuntimeError(f"Command failed with error: {result.stderr.strip()}")
        except Exception as e:
            logger.exception("Error while executing shell command:")
            raise e
        return result.stdout.strip()

    @staticmethod
    def run(command: str, shell_type = shell_type.bash, output=True):
        if output: logger.info(f"Executing shell command: {command}")  
        result = Shell.process(shell_type.value[0], command)
        if output: logger.info(f"Command output:\n{result}")
        return result

        
    @staticmethod
    def run_script(script: str, shell_type = shell_type.bash, output=True):
        if not os.path.exists(script):
            logger.error(f"Invalid script path: file {script} does not exist")
            raise ValueError("Invalid script path")
        return Shell.run(script, shell_type, output)
