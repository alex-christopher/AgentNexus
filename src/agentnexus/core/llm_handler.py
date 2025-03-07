import requests
import json
import openai

from agentnexus.core.config_manager import ConfigManager
from agentnexus.core.logger_manager import LoggerManager

class LLMHandler:
    '''Handler for LLM APIs and supporting dynamic responses'''

    def __init__(self):
        config = ConfigManager.get_config()
        self.api_key = config["api_key"]
        self.endpoint = config["endpoint"]
        self.model_name = config["model_name"]
        self.temperature = config["temperature"]
        self.logger = LoggerManager.get_logger("LLMHandler")
        
    def generate_code(self, system_prompt:str, prompt: str) -> str:
        '''Generate code using the LLM API'''

        try:
            client = openai.OpenAI(
                base_url=self.endpoint,
                api_key=self.api_key
            )
            
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}],
                temperature=self.temperature
            )

            result = response.choices[0].message.content
            self.logger.info("Code generated successfully")
            return result

        except openai.APIConnectionError as e:
            raise Exception("API Connection Error: {e}")
        except openai.APIError as e:
            raise Exception('OpenAI API Error : {e}')
