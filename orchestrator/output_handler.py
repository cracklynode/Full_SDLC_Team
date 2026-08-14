import os
import yaml
import re
from typing import Dict, Any, Optional
from datetime import datetime


class OutputHandler:
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def parse_llm_response(self, response: str) -> str:
        response = response.strip()
        
        yaml_block_pattern = r'```(?:yaml|yml)?\s*\n(.*?)\n```'
        match = re.search(yaml_block_pattern, response, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        if response.startswith('---') or ':' in response:
            return response
        
        raise ValueError("Could not extract valid YAML from LLM response")
    
    def validate_yaml(self, yaml_content: str) -> Dict[str, Any]:
        try:
            parsed = yaml.safe_load(yaml_content)
            if not isinstance(parsed, dict):
                raise ValueError("YAML content must be a dictionary/object")
            return parsed
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format: {str(e)}")
    
    def save_output(
        self,
        yaml_content: str,
        output_filename: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        
        try:
            parsed_yaml = self.validate_yaml(yaml_content)
        except ValueError as e:
            raise ValueError(f"Cannot save invalid YAML: {str(e)}")
        
        if metadata:
            parsed_yaml['_metadata'] = {
                'generated_at': datetime.now().isoformat(),
                'agent': metadata.get('agent_name', 'unknown'),
                'model': metadata.get('model', 'unknown'),
                **metadata
            }
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(parsed_yaml, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        return output_path
    
    def process_and_save(
        self,
        llm_response: str,
        output_filename: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> tuple[str, Dict[str, Any]]:
        
        yaml_content = self.parse_llm_response(llm_response)
        
        parsed_data = self.validate_yaml(yaml_content)
        
        output_path = self.save_output(yaml_content, output_filename, metadata)
        
        return output_path, parsed_data
    
    def load_output(self, filename: str) -> Dict[str, Any]:
        file_path = os.path.join(self.output_dir, filename)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Output file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def output_exists(self, filename: str) -> bool:
        file_path = os.path.join(self.output_dir, filename)
        return os.path.exists(file_path)
