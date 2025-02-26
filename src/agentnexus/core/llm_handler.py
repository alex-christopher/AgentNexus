import requests
import json
import openai

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
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content

        except openai.APIConnectionError:
            raise Exception("Authentication failed check your API key")
        except openai.APIError as e:
            raise Exception('OpenAI API Error')

    def _construct_payload(self, prompt: str) -> dict:
        '''Construct the payload for the LLM API'''
        return {
            'model': self.model_name,
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 1000,
            'temperature': 0.5,
            'top_p': 1.0,
            'n': 1,
            'stop': ['\n']
        }

    def _normalize_response(self, response: dict) -> str:

        try:
            if isinstance(response, str):
                return response.strip()

            possible_keys = ['choices', 'genreated_text', 'text', 'output']
            for key in possible_keys:
                if key in response:
                    return self._extract_from_key(response[key])

            return json.dumps(response, indent=2)
        
        except Exception as e:
            raise Exception(f'Error normalizing response: {e}')

    def _extract_from_key(self, key_value):

        if isinstance(key_value, list) and len(key_value) > 0:
            if isinstance(key_value[0], dict) and 'message' in key_value[0]:
                return key_value[0]['message'].get('content', '').strip()
            elif isinstance(key_value[0], dict):
                return key_value[0].get('text', '').strip()
        elif isinstance(key_value, str):
            return key_value.strip()

        return str(key_value)