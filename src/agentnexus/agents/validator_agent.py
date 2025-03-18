from agentnexus.agents.base_agent import BaseAgent

class ValidatorAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, task):
        # Dummy validation logic
        return {"status": "success", "result": "Validation passed"}
