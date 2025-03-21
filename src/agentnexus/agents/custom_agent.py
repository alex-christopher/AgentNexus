from agentnexus.agents.base_agent import BaseAgent
from agentnexus.core.llm_handler import LLMHandler
from agentnexus.core.execution_engine import ExecutionEngine
from agentnexus.core.validation import CodeValidator
import json

class UserCustomAgent(BaseAgent):
    """
    User-defined agent allowing LLM to decide content_type (code/content).
    Handles validation and execution ONLY for code.
    """

    def __init__(self, name, system_prompt, user_prompt,
                 temperature=None, model_name=None):
        super().__init__(name)
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.llm_handler = LLMHandler.get_instance()
        self.execution_engine = ExecutionEngine()
        self.temperature = temperature
        self.model_name = model_name

    def execute(self, task: str) -> dict:
        self.logger.info(f"[UserCustomAgent] Executing Task: {task}")
        try:
            llm_raw_response = self.llm_handler.generate_code(
                system_prompt=self.system_prompt,
                prompt=self.user_prompt or task,
                temperature=self.temperature,
                model_name=self.model_name
            )

            # Expect LLM to return JSON with 'content_type' and 'response'
            import json
            llm_json = json.loads(llm_raw_response)

            content_type = llm_json.get("content_type", "content")
            response_text = llm_json.get("response", "")

            result_payload = {
                "content_type": content_type,
                "response": response_text
            }

            # Only run validation & execution if LLM marks this as 'code'
            if content_type == "code":
                validation_result = CodeValidator.validate_python(response_text)
                result_payload["validation"] = validation_result

                if validation_result.get("is_valid", False):
                    execution_result = self.execution_engine.execute_python(response_text)
                    result_payload["execution"] = execution_result

            output = {"status": "success", "result": result_payload}

            if not self.validate_output(output):
                return {"status": "error", "result": "Agent output validation failed."}

            self.log_task(task, output)
            return output

        except Exception as e:
            self.logger.error(f"[UserCustomAgent] Error: {e}", exc_info=True)
            return {"status": "error", "result": str(e)}
