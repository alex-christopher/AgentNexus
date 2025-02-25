import uuid
import os
from agentnexus.agents.base_agent import BaseAgent
from agentnexus.core.llm_handler import LLMHandler
from agentnexus.storage.file_manager import FileManager

class DeveloperAgent(BaseAgent):
    '''Agent that uses LLM to generate code'''

    def __init__(self, api_key: str, endpoint: str, model_name:str):
        super().__init__("DeveloperAgent")
        self.llm_handler = LLMHandler(api_key, endpoint, model_name)
        self.file_manager = FileManager()

    def run(self, task: str) -> str:
        '''Run the agent to generate code'''
        generated_code = self.llm_handler.generate_code(task)
        
        file_path = self.file_manager.save_code(generated_code)

        return {"task" : task, "generated_code" : generated_code, "file_path" : file_path}