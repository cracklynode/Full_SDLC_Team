import re
from typing import Dict, List, Optional


class AgentParser:
    
    def __init__(self, agent_file_path: str):
        self.agent_file_path = agent_file_path
        self.content = self._load_content()
        self.parsed_data = self._parse()
    
    def _load_content(self) -> str:
        with open(self.agent_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _parse(self) -> Dict:
        return {
            'name': self._extract_agent_name(),
            'purpose': self._extract_section('Purpose'),
            'io_spec': self._extract_io_spec(),
            'operating_principles': self._extract_section('Operating Principles'),
            'inputs': self._extract_section('Inputs'),
            'process': self._extract_section('Process'),
            'outputs': self._extract_section('Outputs'),
            'output_format': self._extract_output_format(),
            'full_content': self.content
        }
    
    def _extract_agent_name(self) -> str:
        match = re.search(r'^#\s+Agent:\s*(.+)$', self.content, re.MULTILINE)
        return match.group(1).strip() if match else "Unknown Agent"
    
    def _extract_section(self, section_name: str) -> str:
        pattern = rf'^##\s+{re.escape(section_name)}\s*$\n(.*?)(?=^##\s|\Z)'
        match = re.search(pattern, self.content, re.MULTILINE | re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def _extract_io_spec(self) -> Dict[str, Optional[str]]:
        io_section = self._extract_section('I/O Specification')
        
        input_match = re.search(r'-\s*\*\*Input:\*\*\s*(.+?)(?=\n-|\Z)', io_section, re.DOTALL)
        output_match = re.search(r'-\s*\*\*Output:\*\*\s*`([^`]+)`', io_section)
        context_match = re.search(r'-\s*\*\*Working Context:\*\*\s*(.+?)(?=\n-|\Z)', io_section, re.DOTALL)
        
        return {
            'input': input_match.group(1).strip() if input_match else None,
            'output': output_match.group(1).strip() if output_match else None,
            'context': context_match.group(1).strip() if context_match else None
        }
    
    def _extract_output_format(self) -> str:
        pattern = r'##\s+Output Format.*?\n```yaml\n(.*?)```'
        match = re.search(pattern, self.content, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def get_input_file(self) -> Optional[str]:
        io_spec = self.parsed_data['io_spec']
        if io_spec['input']:
            file_match = re.search(r'`([^`]+\.yaml)`', io_spec['input'])
            if file_match:
                return file_match.group(1)
        
        input_handling = self._extract_section('Input Handling')
        if input_handling:
            file_match = re.search(r'\*\*File:\*\*\s*`([^`]+)`', input_handling)
            if file_match:
                return file_match.group(1)
        
        return None
    
    def get_output_file(self) -> Optional[str]:
        return self.parsed_data['io_spec']['output']
    
    def build_prompt(self, context_data: Dict = None) -> str:
        prompt_parts = [
            f"# Role: {self.parsed_data['name']}",
            "",
            f"## Your Purpose",
            self.parsed_data['purpose'],
            "",
            f"## Operating Principles",
            self.parsed_data['operating_principles'],
            "",
            f"## Your Process",
            self.parsed_data['process'],
            "",
            f"## Expected Outputs",
            self.parsed_data['outputs'],
            "",
            f"## Output Format",
            "You MUST generate your response in the following YAML format:",
            "```yaml",
            self.parsed_data['output_format'],
            "```",
            ""
        ]
        
        if context_data:
            prompt_parts.extend([
                "## Input Context",
                "Below is the input data you need to work with:",
                "```yaml",
                context_data.get('yaml_content', ''),
                "```",
                ""
            ])
        
        prompt_parts.extend([
            "## Instructions",
            f"Based on the above context and your role as {self.parsed_data['name']}, generate a complete YAML output following the specified format.",
            "Return ONLY the YAML content without any markdown code blocks, explanations, or additional text.",
            "Ensure all required fields are populated with meaningful, detailed content."
        ])
        
        return "\n".join(prompt_parts)
    
    def get_name(self) -> str:
        return self.parsed_data['name']
    
    def get_purpose(self) -> str:
        return self.parsed_data['purpose']
