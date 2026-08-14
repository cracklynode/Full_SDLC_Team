import os
import yaml
from typing import Dict, Any, List, Optional


class ContextBuilder:
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
    
    def load_yaml_file(self, file_path: str) -> Dict[str, Any]:
        full_path = file_path if os.path.isabs(file_path) else os.path.join(self.output_dir, file_path)
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Context file not found: {full_path}")
        
        with open(full_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def resolve_input_path(self, input_spec: str) -> Optional[str]:
        if not input_spec:
            return None
        
        if '.yaml' in input_spec or '.yml' in input_spec:
            import re
            match = re.search(r'`([^`]+\.ya?ml)`', input_spec)
            if match:
                file_path = match.group(1)
                file_path = file_path.replace('../outputs/', '')
                return file_path
        
        return None
    
    def build_context(self, input_files: List[str]) -> Dict[str, Any]:
        context = {
            'inputs': [],
            'combined_data': {}
        }
        
        for input_file in input_files:
            try:
                data = self.load_yaml_file(input_file)
                context['inputs'].append({
                    'file': input_file,
                    'data': data
                })
                context['combined_data'].update(data)
            except FileNotFoundError as e:
                print(f"⚠️  Warning: {e}")
                continue
        
        return context
    
    def format_context_for_prompt(self, context: Dict[str, Any]) -> Dict[str, str]:
        yaml_parts = []
        
        for input_item in context['inputs']:
            yaml_parts.append(f"# Source: {input_item['file']}")
            yaml_parts.append(yaml.dump(input_item['data'], default_flow_style=False, sort_keys=False))
            yaml_parts.append("")
        
        return {
            'yaml_content': "\n".join(yaml_parts),
            'raw_data': context['combined_data']
        }
    
    def get_previous_outputs(self, current_agent_file: str) -> List[str]:
        agent_number = self._extract_agent_number(current_agent_file)
        
        if agent_number is None or agent_number <= 1:
            return ['00_initial_brief.yaml']
        
        previous_outputs = []
        
        for i in range(agent_number):
            if i == 0:
                previous_outputs.append('00_initial_brief.yaml')
            else:
                pattern = f"{i:02d}_*.yaml"
                matching_files = self._find_files_matching(pattern)
                previous_outputs.extend(matching_files)
        
        return previous_outputs
    
    def _extract_agent_number(self, agent_file: str) -> Optional[int]:
        import re
        match = re.search(r'^(\d+)_', os.path.basename(agent_file))
        return int(match.group(1)) if match else None
    
    def _find_files_matching(self, pattern: str) -> List[str]:
        import glob
        search_path = os.path.join(self.output_dir, pattern)
        files = glob.glob(search_path)
        return [os.path.basename(f) for f in files]
