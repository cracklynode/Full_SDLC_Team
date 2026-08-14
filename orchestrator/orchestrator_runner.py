import yaml
import os
import time
from datetime import datetime

from config import Config
from llm_client import LLMClient
from agent_parser import AgentParser
from output_handler import OutputHandler
from context_builder import ContextBuilder


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "orchestrator_config.yaml")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config

def resolve_path(base_path, relative_path):
    orchestrator_dir = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(orchestrator_dir, relative_path))

def get_initial_brief():
    print("\n" + "="*60)
    print("🚀 Full SDLC Team Orchestrator")
    print("="*60 + "\n")
    print("Please provide your project idea or business goal.")
    print("This will be used as the initial brief for the Product Owner.\n")
    print("Example: 'Build a cloud cost optimizer for Azure resources'\n")
    
    brief = input("💡 Enter your project idea: ").strip()
    
    while not brief:
        print("⚠️  Project idea cannot be empty. Please try again.\n")
        brief = input("💡 Enter your project idea: ").strip()
    
    print(f"\n✓ Project idea captured: {brief}\n")
    return brief

def save_initial_brief(brief, output_dir):
    brief_file = os.path.join(output_dir, "00_initial_brief.yaml")
    
    brief_data = {
        "initial_brief": brief,
        "timestamp": datetime.now().isoformat(),
        "status": "pending"
    }
    
    with open(brief_file, "w", encoding="utf-8") as f:
        yaml.dump(brief_data, f, default_flow_style=False, sort_keys=False)
    
    print(f"📝 Initial brief saved to: {brief_file}\n")
    return brief_file

def execute_agent_with_llm(
    agent_file: str,
    agent_dir: str,
    output_dir: str,
    llm_client: LLMClient,
    context_builder: ContextBuilder,
    output_handler: OutputHandler,
    config: Config
):
    agent_path = os.path.join(agent_dir, agent_file)
    
    if not os.path.exists(agent_path):
        print(f"⚠️  Warning: {agent_file} not found at {agent_path}")
        return False
    
    print(f"🧩 Executing {agent_file}...")
    
    parser = AgentParser(agent_path)
    agent_name = parser.get_name()
    output_file = parser.get_output_file()
    
    if not output_file:
        print(f"   ⚠️  No output file specified for {agent_file}, skipping...")
        return False
    
    output_filename = os.path.basename(output_file)
    
    print(f"   📖 Agent: {agent_name}")
    print(f"   📄 Output: {output_filename}")
    
    previous_outputs = context_builder.get_previous_outputs(agent_file)
    print(f"   📥 Loading context from: {', '.join(previous_outputs)}")
    
    context = context_builder.build_context(previous_outputs)
    formatted_context = context_builder.format_context_for_prompt(context)
    
    prompt = parser.build_prompt(formatted_context)
    
    print(f"   🤖 Calling LLM ({config.model})...")
    
    for attempt in range(config.retry_attempts):
        try:
            response = llm_client.generate_yaml(
                prompt=prompt,
                system_message=f"You are an expert {agent_name} in a software development team.",
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )
            
            print(f"   ✓ LLM response received ({len(response)} chars)")
            
            output_path, parsed_data = output_handler.process_and_save(
                llm_response=response,
                output_filename=output_filename,
                metadata={
                    'agent_name': agent_name,
                    'agent_file': agent_file,
                    'model': config.model,
                    'provider': config.provider
                }
            )
            
            print(f"   💾 Output saved to: {output_path}")
            print(f"   ✓ {agent_file} completed successfully\n")
            return True
            
        except Exception as e:
            print(f"   ⚠️  Attempt {attempt + 1}/{config.retry_attempts} failed: {str(e)}")
            if attempt < config.retry_attempts - 1:
                print(f"   ⏳ Retrying in {config.retry_delay} seconds...")
                time.sleep(config.retry_delay)
            else:
                print(f"   ❌ Failed to execute {agent_file} after {config.retry_attempts} attempts\n")
                return False

def run_agents():
    try:
        print("\n🔧 Loading configuration...")
        app_config = Config()
        app_config.validate()
        print(f"   ✓ Configuration loaded: {app_config}")
        
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease create a .env file with your API credentials.")
        print("See .env.example for reference.\n")
        return
    
    orchestrator_config = load_config()
    
    agent_dir = resolve_path(__file__, orchestrator_config["agent_folder"])
    output_dir = resolve_path(__file__, orchestrator_config["output_folder"])
    src_dir = resolve_path(__file__, orchestrator_config["src_folder"])
    infra_dir = resolve_path(__file__, orchestrator_config["infra_folder"])
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(infra_dir, exist_ok=True)
    
    initial_brief = get_initial_brief()
    save_initial_brief(initial_brief, output_dir)
    
    print(f"📂 Project Root: {orchestrator_config['project_root']}")
    print(f"📂 Agent Directory: {agent_dir}")
    print(f"📂 Output Directory: {output_dir}")
    print(f"📂 Source Directory: {src_dir}")
    print(f"📂 Infrastructure Directory: {infra_dir}")
    print(f"\n{'='*60}\n")
    
    llm_config = app_config.get_llm_config()
    llm_client = LLMClient(
        provider=llm_config['provider'],
        model=llm_config['model'],
        api_key=llm_config['api_key'],
        base_url=llm_config['base_url']
    )
    
    context_builder = ContextBuilder(output_dir)
    output_handler = OutputHandler(output_dir)
    
    print("🚀 Starting agent execution pipeline...\n")
    
    success_count = 0
    failed_agents = []
    
    for agent_file in orchestrator_config["execution_order"]:
        success = execute_agent_with_llm(
            agent_file=agent_file,
            agent_dir=agent_dir,
            output_dir=output_dir,
            llm_client=llm_client,
            context_builder=context_builder,
            output_handler=output_handler,
            config=app_config
        )
        
        if success:
            success_count += 1
        else:
            failed_agents.append(agent_file)
    
    print(f"{'='*60}")
    print(f"✅ Pipeline completed: {success_count}/{len(orchestrator_config['execution_order'])} agents succeeded")
    
    if failed_agents:
        print(f"⚠️  Failed agents: {', '.join(failed_agents)}")
    
    print(f"📋 Outputs available in: {output_dir}\n")

if __name__ == "__main__":
    try:
        run_agents()
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("   Ensure orchestrator_config.yaml exists in the orchestrator directory.")
    except KeyboardInterrupt:
        print("\n\n⚠️  Orchestration cancelled by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
