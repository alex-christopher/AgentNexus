from abc import ABC, abstractmethod
import uuid

from agentnexus.core.logger_manager import LoggerManager

class BaseAgent(ABC):
    """Abstract base class for all agents with automatic logging control."""

    def __init__(self, name: str):
        self.name = name
        self.agent_id = str(uuid.uuid4())
        self.logger = LoggerManager.get_logger(self.name)  
        self.task_history = []


    @abstractmethod
    def execute(self, task:str) -> dict:
        """Each agent must implement its own execution logic."""
        pass

    def validate_output(self, output: dict) -> bool:
        if not isinstance(output, dict):
            self.logger.error("Output is not a dictionary.")
            return False
        
        if "status" not in output or "result" not in output:
            self.logger.error("Output missing required fields: 'status' and 'result'.")
            return False
        
        return True
    
    def log_task(self, task: str, output: dict):
        self.task_history.append({
            "task": task,
            "output": output
        })
        self.logger.info(f"Task executed: {task} | Output: {output}")

    def get_task_history(self):
        return self.task_history
