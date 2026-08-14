import os
import json
from typing import Optional, Dict, Any
from openai import OpenAI


class LLMClient:
    
    def __init__(self, provider: str = "openai", model: str = None, api_key: str = None, base_url: str = None):
        self.provider = provider.lower()
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        
        if not self.api_key:
            raise ValueError(
                "API key not provided. Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )
        
        if self.provider == "openai":
            self.model = self.model or "gpt-4o"
            self.client = OpenAI(api_key=self.api_key)
        elif self.provider == "routellm":
            self.model = self.model or "gpt-4o"
            if not self.base_url:
                raise ValueError(
                    "RouteLLM requires a base_url. Set OPENAI_BASE_URL environment variable or pass base_url parameter."
                )
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        elif self.provider == "custom":
            if not self.base_url:
                raise ValueError(
                    "Custom provider requires a base_url. Set OPENAI_BASE_URL environment variable or pass base_url parameter."
                )
            self.model = self.model or "gpt-4o"
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'openai', 'routellm', or 'custom'.")
    
    def generate(
        self,
        prompt: str,
        system_message: str = "You are a helpful AI assistant.",
        temperature: float = 0.7,
        max_tokens: int = 4000,
        response_format: Optional[Dict[str, Any]] = None
    ) -> str:
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        try:
            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            if response_format:
                kwargs["response_format"] = response_format
            
            response = self.client.chat.completions.create(**kwargs)
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise RuntimeError(f"LLM API call failed: {str(e)}")
    
    def generate_yaml(
        self,
        prompt: str,
        system_message: str = "You are a helpful AI assistant that generates YAML outputs.",
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        
        enhanced_prompt = f"{prompt}\n\nIMPORTANT: Return ONLY valid YAML. Do not include markdown code blocks, explanations, or any text outside the YAML structure."
        
        return self.generate(
            prompt=enhanced_prompt,
            system_message=system_message,
            temperature=temperature,
            max_tokens=max_tokens
        )
