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

class DeveloperAgent(BaseAgent):
    '''Agent that uses LLM to generate and validate code'''

    def __init__(self, api_key: str, endpoint: str, model_name: str):
        super().__init__("DeveloperAgent")
        self.llm_handler = LLMHandler(api_key, endpoint, model_name)
        self.file_manager = FileManager()

    def run(self, task: str) -> dict:
        '''Runs the agent to generate, validate, and execute code'''
        generated_code = self.llm_handler.generate_code(task)
        clean_code = self._clean_code(generated_code)
        formatted_code = self._format_code(clean_code)
        validation_result = self._validate_code(formatted_code)
        execution_result = None

        if validation_result["is_valid"]:
            execution_result = self._execute_code(clean_code)

        return {
            "task": task,
            "generated_code": clean_code,
            "validation_result": validation_result,
            "execution_result": execution_result,
            "formatted_code": formatted_code
        }
    
    def _clean_code(self, code:str) -> str:
        code = code.strip()
        code = re.sub(r"^```[a-zA-Z]*\n", "", code)
        code = re.sub(r"```$", "", code)

        return code.strip()
    
    def _format_code(self, code: str) -> str:
        try:
            formatted_code = black.format_str(code, mode=black.FileMode())
            formatted_code = isort.code(formatted_code)
            return formatted_code
        except Exception as e:
            return code
            
    def _validate_code(self, code: str) -> dict:
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

    def _execute_code(self, code: str) -> dict:
        """Executes generated code in a safe environment."""
        temp_script_path = None  

        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
                temp_file.write(code)
                temp_script_path = temp_file.name  

            result = subprocess.run(["python", temp_script_path], capture_output=True, text=True)
            output = result.stdout.strip() if result.stdout else result.stderr.strip()

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
