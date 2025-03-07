from abc import ABC, abstractmethod
from agentnexus.core.logger_manager import LoggerManager

class BaseAgent(ABC):
    """Abstract base class for all agents with automatic logging control."""

    def __init__(self, name: str):
        self.name = name
        self.logger = LoggerManager.get_logger(self.name)  

    @abstractmethod
    def execute(self, task: str) -> dict:
        """Each agent must implement its own execution logic."""
        pass
