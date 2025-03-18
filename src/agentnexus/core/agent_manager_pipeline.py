import asyncio
from concurrent.futures import ThreadPoolExecutor
from agentnexus.core.agent_manager import AgentManager
from agentnexus.core.logger_manager import LoggerManager

class AgentManagerPipeline(AgentManager):
    def __init__(self):
        super().__init__()
        self.executer = ThreadPoolExecutor(max_workers=5)
        self.active_tasks = set()
        self.logger = LoggerManager.get_logger("AgentManagerPipeline")

    async def run_task_async(self, agent_name: str, task: str):
        if agent_name not in self.agents:
            self.logger.error(f"Agent {agent_name} not found")
            raise ValueError(f"Agent {agent_name} not found")
        
        agent = self.agents[agent_name]
        output = await asyncio.get_event_loop().run_in_executor(self.executer, agent.execute, task)

        if not agent.validate_output(output):
            print(f"[AgentManager] Validation failed for {agent_name}")
            self.logger.error(f"Validation failed for {agent_name}")
            return {"status": "error", "result": output}
        
        agent.log_task(task, output)
        self.task_history.append({"agent": agent_name, "task": task, "output": output})
        self.logger.info(f"[AgentManagerPipeline] Agent {agent_name} completed execution")
        return output
    
    async def run_pipeline_async(self, agent_sequence: list, task: str):
        context = {}
        tasks = []

        for agent_name in agent_sequence:
            if self.logger.warning(f"[AgentManagerPipeline] Skipping duplicate agent-task: {agent_name}"):
                continue
            self.active_tasks.add((agent_name, task))
            tasks.append(asyncio.create_task(self.run_task_async(agent_name, task)))

        self.logger.info(f"[AgentManagerPipeline] Running pipeline for task: {task}")
        results = await asyncio.gather(*tasks)

        for agent_name, result in zip(agent_sequence, results):
            context[agent_name] = result

        self.logger.info(f"[AgentManagerPipeline] Pipeline completed for task: {task}")
        return context

    def shutdown(self):
        self.logger.info("[AgentManagerPipeline] Executor shutdown")
        self.executer.shutdown()
        
