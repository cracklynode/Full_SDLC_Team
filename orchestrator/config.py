import os
from typing import Optional
from dotenv import load_dotenv


class Config:
    
    def __init__(self, env_file: Optional[str] = None):
        if env_file and os.path.exists(env_file):
            load_dotenv(env_file)
        else:
            load_dotenv()
        
        self.provider = os.getenv('LLM_PROVIDER', 'openai')
        self.model = os.getenv('LLM_MODEL', 'gpt-4o')
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.base_url = os.getenv('OPENAI_BASE_URL')
        
        self.temperature = float(os.getenv('LLM_TEMPERATURE', '0.7'))
        self.max_tokens = int(os.getenv('LLM_MAX_TOKENS', '4000'))
        
        self.retry_attempts = int(os.getenv('RETRY_ATTEMPTS', '3'))
        self.retry_delay = int(os.getenv('RETRY_DELAY', '2'))
    
    def validate(self) -> bool:
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. "
                "Please set it in your .env file or environment."
            )
        
        if self.provider in ['routellm', 'custom'] and not self.base_url:
            raise ValueError(
                f"OPENAI_BASE_URL is required for provider '{self.provider}'. "
                "Please set it in your .env file or environment."
            )
        
        return True
    
    def get_llm_config(self) -> dict:
        return {
            'provider': self.provider,
            'model': self.model,
            'api_key': self.api_key,
            'base_url': self.base_url,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens
        }
    
    def __repr__(self) -> str:
        return (
            f"Config(provider={self.provider}, model={self.model}, "
            f"temperature={self.temperature}, max_tokens={self.max_tokens})"
        )
