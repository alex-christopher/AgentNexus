from agentnexus.agents.base_agent import BaseAgent

class TaskManager(BaseAgent):

    def __init__(self):
        self.agents = {}
    
    def register_agent(self, agent_name: str, agent_class: type):
        if not issubclass(agent_class, BaseAgent):
            raise ValueError("Agent must be a subclass of BaseAgent")
        self.agents[agent_name] = agent_class

    def execute_task(self, agent_name: str, task: str):
        if agent_name not in self.agents:
            raise ValueError(f"Agent {agent_name} not found")
        
        agent_instance = self.agents[agent_name]()
        return agent_instance.execute(task)