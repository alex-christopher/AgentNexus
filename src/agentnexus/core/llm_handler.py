from agentnexus.core.config_manager import ConfigManager
from agentnexus.core.logger_manager import LoggerManager
import openai
import json

class LLMHandler:
    """
    Singleton LLM Handler - Pure Transport Layer
    Accepts any system_prompt, user_prompt, temperature, model
    """

    _instance = None

    def __init__(self):
        config = ConfigManager.get_config()
        self.api_key = config["api_key"]
        self.endpoint = config["endpoint"]
        self.model_name = config["model_name"]
        self.temperature = config["temperature"]
        self.logger = LoggerManager.get_logger("LLMHandler")

        # OpenAI client initialized ONCE (Singleton)
        self.client = openai.OpenAI(
            base_url=self.endpoint,
            api_key=self.api_key
        )

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def generate(self, system_prompt: str, prompt: str,
                      temperature: float = None, model_name: str = None) -> str:
       
        try:
            response = self.client.chat.completions.create(
                model=model_name if model_name else self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature if temperature else self.temperature,
                response_format={ "type": "json_object" }
            )

            result = response.choices[0].message.content
            self.logger.info("[LLMHandler] LLM response received successfully")
            print("RESS : ", result)
            return result

        except openai.APIConnectionError as e:
            self.logger.error(f"API Connection Error: {e}")
            raise Exception(f"API Connection Error: {e}")

        except openai.APIError as e:
            self.logger.error(f"OpenAI API Error: {e}")
            raise Exception(f"OpenAI API Error: {e}")
