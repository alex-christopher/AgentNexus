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

    _instance = None  # Singleton instance

    def __init__(self):
        super().__init__("DeveloperAgent")
        self.llm_handler = LLMHandler()
        self.execution_engine = ExecutionEngine()

    @classmethod
    def get_instance(cls):
        """Get or create a singleton instance of DeveloperAgent."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def build(cls, task: str) -> dict:
        """Use an instance to build code instead of creating a new one each time."""
        return cls.get_instance()._build(task)

    @classmethod
    def execute_code(cls, code: str) -> dict:
        """Use the same instance to execute code."""
        return cls.get_instance()._execute_code(code)

    def execute(self, task: str) -> dict:
        """Implements the abstract method from BaseAgent."""
        return self._build(task)

    def _build(self, task: str) -> dict:
        """Runs the agent to generate, validate, and execute code."""
        self.logger.info(f"Generating code for task: {task}")
        
        try:
            generated_code = self.llm_handler.generate_code(DEVELOPER_PROMPT, task)
            clean_code = self._clean_python_code(generated_code)
            formatted_code = self._format_python_code(clean_code)
            validation = CodeValidator.validate_python(formatted_code)

            output = {
                "status": "success",
                "result" : {
                    "task": task,
                    "generated_code": formatted_code,
                    "validation": validation
                }
            }

            if not self.validate_output(output):
                return {"status": "error", 
                        "result": {
                            "task": task, 
                            "error": "Output validation failed."
                    }
                }
            self.log_task(task, output)
            return output

        except Exception as e:
            self.logger.error(f"Error in DeveloperAgent execution: {e}", exc_info=True)
            return {"status": "error", "result": str(e)}

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
        except Exception:
            return code  

    def _execute_code(self, code: str) -> dict:
        """Executes the Python code using the framework's execution engine."""
        return self.execution_engine.execute_python(code)
