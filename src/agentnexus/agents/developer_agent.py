import re
import black
import isort
from agentnexus.agents.base_agent import BaseAgent
from agentnexus.core.llm_handler import LLMHandler
from agentnexus.core.validation import CodeValidator
from agentnexus.core.execution_engine import ExecutionEngine
from agentnexus.prompts.developer_prompt import DEVELOPER_PROMPT

class DeveloperAgent(BaseAgent):
    """Agent that uses LLM to generate, validate, and execute code."""

    def __init__(self):
        super().__init__("DeveloperAgent")
        self.llm_handler = LLMHandler()
        self.execution_engine = ExecutionEngine()

    def execute(self, task: str) -> dict:
        """Runs the agent to generate, validate, and execute code."""
        self.logger.info(f"Starting task: {task}")
        try:
            result = self._build(task)
            self.logger.info(f"Task completed successfully: {task}")
            return result
        except Exception as e:
            self.logger.error(f"Error in DeveloperAgent execution: {e}", exc_info=True)
            return {"error": str(e)}

    @classmethod
    def build(cls, task: str) -> dict:
        instance = cls()
        return instance._build(task)

    @classmethod
    def execute_code(cls, code: str) -> dict:
        instance = cls()
        return instance._execute_code(code)

    def _build(self, task: str) -> dict:
        """Runs the agent to generate, validate, and execute code."""
        self.logger.debug(f"Generating code for task: {task}")
        generated_code = self.llm_handler.generate_code(DEVELOPER_PROMPT, task)
        clean_code = self._clean_python_code(generated_code)
        formatted_code = self._format_python_code(clean_code)
        validation = CodeValidator.validate_python(formatted_code)

        return {
            "task": task,
            "generated_code": formatted_code,
            "validation": validation
        }

    @staticmethod
    def _clean_python_code(code: str) -> str:
        """Cleans the code by removing Markdown formatting."""
        code = code.strip()
        code = re.sub(r"^```[a-zA-Z]*\n", "", code)
        code = re.sub(r"```$", "", code)
        return code.strip()

    @staticmethod
    def _format_python_code(code: str) -> str:
        """Formats code using Black and sorts imports using isort."""
        try:
            formatted_code = black.format_str(code, mode=black.FileMode())
            formatted_code = isort.code(formatted_code)
            return formatted_code
        except Exception as e:
            return code  # Return original if formatting fails

    def _execute_code(self, code: str) -> dict:
        """Executes the Python code using the framework's execution engine."""
        result = self.execution_engine.execute_python(code)
        return result
