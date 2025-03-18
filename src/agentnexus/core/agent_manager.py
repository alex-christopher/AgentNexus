class AgentManager:
    def __init__(self):
        self.agents = {}
        self.task_history = []

    def register_agent(self, agent_name: str, agent_instance):
        self.agents[agent_name] = agent_instance

    def dynamic_spawn(self, agent_name, agent_class):
        if agent_name not in self.agents:
            if hasattr(agent_class, 'get_instance'):
                self.agents[agent_name] = agent_class.get_instance()
            else:
                self.agents[agent_name] = agent_class(agent_name)
            print(f"[AgentManager] Dynamically spawned agent: {agent_name}")

    def run_task(self, agent_name: str, task: str):
        if agent_name not in self.agents:
            raise ValueError(f"Agent {agent_name} not found")
        
        agent = self.agents[agent_name]
        output = agent.execute(task)

        if not agent.validate_output(output):
            print(f"[AgentManager] Validation failed for {agent_name}")
            return {"status": "error", "result": output}
        
        agent.log_task(task, output)
        self.task_history.append({"agent": agent_name, "task": task, "output": output})
        return output

    def run_pipeline(self, agent_sequence: list, task: str):
        context = {}
        for agent_name in agent_sequence:
            result = self.run_task(agent_name, task)
            context[agent_name] = result
            if result['status'] == 'error':
                break
        return context
