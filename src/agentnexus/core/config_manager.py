class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.api_key = None
            cls._instance.endpoint = None
            cls._instance.model_name = None
            cls._instance.temperature = 0.7
            cls._instance.model_provider = "groq"
            cls._instance.enable_logging = True
        return cls._instance
    
    @classmethod
    def set_config(cls, api_key: str, endpoint: str, model_name: str, temperature: float=0.7, model_provider: str="groq", enable_logging: bool=True):
        instance = cls()
        instance.api_key = api_key
        instance.endpoint = endpoint
        instance.model_name = model_name
        instance.temperature = 0.7
        instance.model_provider = "groq"
        instance.enable_logging = enable_logging

    @classmethod
    def get_config(cls):
        instance = cls()
        return{
            "api_key": instance.api_key,
            "endpoint": instance.endpoint,
            "model_name": instance.model_name,
            "temperature": instance.temperature,
            "model_provider": instance.model_provider,
            "enable_logging": instance.enable_logging
        }