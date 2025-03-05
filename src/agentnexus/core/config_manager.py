class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.api_key = None
            cls._instance.endpoint = None
            cls._instance.model_name = None
        return cls._instance
    
    @classmethod
    def set_config(cls, api_key: str, endpoint: str, model_name: str, temperature: float = 0.7):
        instance = cls()
        instance.api_key = api_key
        instance.endpoint = endpoint
        instance.model_name = model_name
        instance.temperature = temperature

    @classmethod
    def get_config(cls):
        instance = cls()
        return{
            "api_key": instance.api_key,
            "endpoint": instance.endpoint,
            "model_name": instance.model_name,
            "temperature": instance.temperature
        }