import tempfile
import subprocess
import os
import re

from agentnexus.core.logger_manager import LoggerManager

class ExecutionEngine:

    def __init__(self):
        self.logger = LoggerManager.get_logger("ExecutionEngine")

    def execute_python(self, code: str) -> dict:
        '''Executes python code'''
        temp_script_path = None

        try:
            self.logger.info(f"Executing code: {code}")
            with tempfile.NamedTemporaryFile(mode='w', suffix=".py", delete=False) as temp_file:
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
            self.logger.info(f"Execution completed successfully")
            return {
                "execution_success": result.returncode == 0,
                "output": output
            }
        except Exception as e:
            self.logger.error(f"Error executing code: {e}", exc_info=True)
            return {
                "execution_success": False,
                "error": str(e)
            }
        finally:
            if temp_script_path and os.path.exists(temp_script_path):
                os.remove(temp_script_path)