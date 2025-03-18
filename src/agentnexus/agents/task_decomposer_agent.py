from agentnexus.agents.base_agent import BaseAgent

class TaskDecomposerAgent(BaseAgent):
    """Decomposes a user task into required agent sequence."""

    def execute(self, task: str) -> dict:
        self.logger.info(f"Decomposing Task: {task}")

        # Simple rule-based decomposition for now (MVP logic)
        agent_sequence = []

        if "build" in task.lower() or "create" in task.lower():
            agent_sequence.append("developer")
            agent_sequence.append("validator")
            agent_sequence.append("tester")
            agent_sequence.append("auditor")

        elif "test" in task.lower():
            agent_sequence.append("tester")
            agent_sequence.append("auditor")

        else:
            agent_sequence.append("developer")
            agent_sequence.append("validator")

        result = {
            "status": "success",
            "result": agent_sequence
        }

        self.logger.info(f"Decomposition Result: {result}")
        return result
