import requests
import json
import openai

from agentnexus.prompts.developer_prompt import DEVELOPER_PROMPT

class LLMHandler:
    '''Handler for LLM APIs and supporting dynamic responses'''

    def __init__(self, api_key: str, endpoint: str, model_name: str):
        self.api_key = api_key
        self.endpoint = endpoint
        self.model_name = model_name

    def generate_code(self, prompt: str) -> str:
        '''Generate code using the LLM API'''

        try:
            client = openai.OpenAI(
                base_url=self.endpoint,
                api_key=self.api_key
            )
            
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": DEVELOPER_PROMPT},
                    {"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content

        except openai.APIConnectionError:
            raise Exception("Authentication failed check your API key")
        except openai.APIError as e:
            raise Exception('OpenAI API Error')

    