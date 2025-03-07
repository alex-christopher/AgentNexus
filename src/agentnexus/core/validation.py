import ast
import flake8.api.legacy as flake8
import tempfile
import os

from agentnexus.core.logger_manager import LoggerManager

class CodeValidator:

    
    logger = LoggerManager.get_logger("CodeValidator")
        
    @staticmethod
    def validate_python(code:str) -> dict:
        '''Validates python code'''
        temp_file = None
        CodeValidator.logger.info("Validating Python code.")

        try:
            ast.parse(code)
            CodeValidator.logger.debug("Syntax check passed.")

            with tempfile.NamedTemporaryFile(mode='w', suffix=".py", delete=False) as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name

            style_guide = flake8.get_style_guide()
            report = style_guide.check_files([temp_file_path])

            CodeValidator.logger.info(f"Linter found {report.total_errors} errors.")

            return {
                "is_valid": report.total_errors == 0,
                "linter_errors": report.total_errors
            }
    
        except SyntaxError as e:
            self.logger.error(f"Syntax Error: {e}", exc_info=True)
            return {
                "is_valid": False,
                "linter_errors": f"Syntax Error: {str(e)}"
            }
        
        finally:
            if temp_file and os.path.exists(temp_file.name):
                os.remove(temp_file.name)

    