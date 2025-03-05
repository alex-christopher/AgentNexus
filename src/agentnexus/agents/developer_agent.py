import uuid
import os
import ast
import flake8.api.legacy as flake8
import tempfile
import subprocess
import re
import black
import isort

from agentnexus.agents.base_agent import BaseAgent
from agentnexus.core.llm_handler import LLMHandler
from agentnexus.storage.file_manager import FileManager
from agentnexus.prompts.developer_prompt import DEVELOPER_PROMPT


class DeveloperAgent(BaseAgent):
    '''Agent that uses LLM to generate and validate code'''

    def __init__(self):
        super().__init__("DeveloperAgent")
        self.llm_handler = LLMHandler()
        self.file_manager = FileManager()

    @classmethod
    def build(cls, task: str) -> dict:
        instance = cls()
        return instance._build_code(task)
    
    @classmethod
    def execute_code(cls, code: str) -> dict:
        instance = cls()
        return instance._execute_python_code(code)

    def _build_code(self, task: str) -> dict:
        '''Runs the agent to generate, validate, and execute code'''
        generated_code = self.llm_handler.generate_code(DEVELOPER_PROMPT, task)
        clean_code = self._clean_python_code(generated_code)
        formatted_code = self._format_python_code(clean_code)
        validation = self._validate_python_code(formatted_code)

        return {
            "task": task,
            "generated_code": formatted_code,
            "validation" : validation
        }
    
    def _clean_python_code(self, code:str) -> str:
        code = code.strip()
        code = re.sub(r"^```[a-zA-Z]*\n", "", code)
        code = re.sub(r"```$", "", code)

        return code.strip()
    
    def _format_python_code(self, code: str) -> str:
        try:
            formatted_code = black.format_str(code, mode=black.FileMode())
            formatted_code = isort.code(formatted_code)
            return formatted_code
        except Exception as e:
            return code
            
    def _validate_python_code(self, code: str) -> dict:
        """Validates the generated code using syntax checking and flake8 linting."""
        temp_file_path = None  

        try:
            ast.parse(code)

            with tempfile.NamedTemporaryFile(mode='w', suffix=".py", delete=False) as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name  

            style_guide = flake8.get_style_guide()
            report = style_guide.check_files([temp_file_path])

            return {
                "is_valid": report.total_errors == 0,
                "linter_errors": report.total_errors
            }
        except SyntaxError as e:
            return {
                "is_valid": False,
                "linter_errors": f"Syntax Error: {str(e)}"
            }
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def _execute_python_code(self, code: str) -> dict:
        """Executes generated code in a safe environment."""
        temp_script_path = None  

        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
                temp_file.write(code)
                temp_script_path = temp_file.name  

            result = subprocess.run(["python", temp_script_path], capture_output=True, text=True)
            output = result.stdout.strip() if result.stdout else result.stderr.strip()

            if "ModuleNotFoundError" in output:
                missing_module = re.search(r"ModuleNotFoundError: No module named '(.+)'", output)
                if missing_module:
                    module_name = missing_module.group(1)
                    return {
                        "execution_success": False,
                        "error": f"Missing module: '{module_name}'. Please install it using:\n"
                                f"   pip install {module_name}"
                    }

            return {
                "execution_success": result.returncode == 0,
                "output": output
            }

        except Exception as e:
            return {
                "execution_success": False,
                "error": str(e)
            }
        finally:
            if temp_script_path and os.path.exists(temp_script_path):
                os.remove(temp_script_path)
