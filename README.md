# Full SDLC Team Orchestrator - LLM Integration

An AI-powered orchestrator that runs a complete Software Development Life Cycle (SDLC) team using Large Language Models. Each agent (Product Owner, Analyst, Designer, Developer, QA, DevOps) is defined as a markdown prompt and executed sequentially, with outputs automatically fed as context to the next agent.

## Features

- 🤖 **LLM-Powered Agents**: Each agent markdown file is treated as an AI prompt
- 🔄 **Automatic Context Chaining**: Outputs from one agent automatically feed into the next
- 📝 **YAML Output Generation**: All agent outputs are generated and saved as structured YAML
- 🔌 **Multiple LLM Providers**: Support for OpenAI, RouteLLM, and custom endpoints
- ⚙️ **Configurable**: Easy configuration via environment variables
- 🔁 **Retry Logic**: Automatic retry with exponential backoff for API failures
- 📂 **Organized Outputs**: All outputs saved to `/outputs` directory with metadata

## Architecture

### Core Modules

1. **llm_client.py** - Handles API calls to OpenAI/RouteLLM/custom endpoints
2. **agent_parser.py** - Extracts I/O specs and prompts from markdown agent files
3. **output_handler.py** - Parses LLM responses and saves YAML outputs
4. **context_builder.py** - Loads previous outputs and builds context for next agent
5. **config.py** - Manages configuration from environment variables
6. **orchestrator_runner.py** - Main orchestration logic

### Agent Pipeline

```
User Input → Product Owner → Analyst → Designer → Developer → QA → DevOps
              ↓                ↓          ↓           ↓         ↓      ↓
           01_PO_*.yaml   02_Analyst_*.yaml  ...  06_DevOps_*.yaml
```

Each agent:
1. Reads its markdown definition
2. Loads context from previous agent outputs
3. Calls LLM with structured prompt
4. Parses and validates YAML response
5. Saves output for next agent

## Setup

### Prerequisites

- Python 3.8+
- OpenAI API key (or compatible LLM endpoint)

### Installation

1. **Clone or navigate to the project directory**

```bash
cd Projects/FullSDLCTeam
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here

# Optional: Change provider and model
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o

# Optional: For RouteLLM or custom endpoints
# OPENAI_BASE_URL=https://your-routellm-endpoint.com/v1

# Optional: Adjust generation parameters
# LLM_TEMPERATURE=0.7
# LLM_MAX_TOKENS=4000
```

## Usage

### Running the Orchestrator

From the project root:

```bash
cd orchestrator
python orchestrator_runner.py
```

Or from the project root:

```bash
python orchestrator/orchestrator_runner.py
```

### Interactive Flow

1. The orchestrator will prompt you for a project idea:
   ```
   💡 Enter your project idea: Build a cloud cost optimizer for Azure resources
   ```

2. It will then execute each agent in sequence:
   - Product Owner → generates product brief and backlog
   - Analyst → creates functional specs and data models
   - Designer → produces architecture and UI/UX designs
   - Developer → generates implementation plans and code structure
   - QA → creates test plans and test cases
   - DevOps → defines infrastructure and deployment pipelines

3. All outputs are saved to `/outputs` directory

### Output Files

```
outputs/
├── 00_initial_brief.yaml
├── 01_PO_Output_Package.yaml
├── 02_Analyst_Output_Dossier.yaml
├── 03_Designer_Output_Blueprint.yaml
├── 04_Developer_Output_Codebase.yaml
├── 05_QA_Output_Test_Suite.yaml
└── 06_DevOps_Output_Infrastructure.yaml
```

Each output file includes:
- Structured YAML content as defined in agent markdown
- Metadata (timestamp, agent name, model used)

## Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | *required* | Your OpenAI API key |
| `LLM_PROVIDER` | `openai` | Provider: `openai`, `routellm`, or `custom` |
| `LLM_MODEL` | `gpt-4o` | Model to use for generation |
| `OPENAI_BASE_URL` | - | Base URL for RouteLLM or custom endpoints |
| `LLM_TEMPERATURE` | `0.7` | Temperature for generation (0.0-1.0) |
| `LLM_MAX_TOKENS` | `4000` | Maximum tokens per response |
| `RETRY_ATTEMPTS` | `3` | Number of retry attempts on failure |
| `RETRY_DELAY` | `2` | Delay between retries (seconds) |

### Using RouteLLM

To use RouteLLM or a custom endpoint:

```env
OPENAI_API_KEY=your_api_key
LLM_PROVIDER=routellm
OPENAI_BASE_URL=https://your-routellm-endpoint.com/v1
LLM_MODEL=gpt-4o
```

### Using Custom Endpoints

For any OpenAI-compatible endpoint:

```env
OPENAI_API_KEY=your_api_key
LLM_PROVIDER=custom
OPENAI_BASE_URL=https://your-custom-endpoint.com/v1
LLM_MODEL=your-model-name
```

## Agent Definitions

Agents are defined in `/agents` directory as markdown files:

- `01_product_owner.md` - Product vision and backlog
- `02_analyst.md` - Functional specifications
- `03_designer.md` - Architecture and design
- `04_developer.md` - Implementation plans
- `05_QA.md` - Test strategies
- `06_DevOps.md` - Infrastructure and deployment

Each agent markdown includes:
- **Purpose**: What the agent does
- **I/O Specification**: Input and output files
- **Operating Principles**: How the agent works
- **Process**: Step-by-step workflow
- **Output Format**: YAML structure to generate

## Customization

### Adding New Agents

1. Create a new markdown file in `/agents` (e.g., `07_security.md`)
2. Follow the existing agent structure
3. Add to `orchestrator_config.yaml` execution order:

```yaml
execution_order:
  - 01_product_owner.md
  - 02_analyst.md
  - 03_designer.md
  - 04_developer.md
  - 05_QA.md
  - 06_DevOps.md
  - 07_security.md  # New agent
```

### Modifying Agent Behavior

Edit the markdown files in `/agents` to change:
- Agent purpose and principles
- Output format structure
- Process steps
- Operating guidelines

The orchestrator will automatically use the updated definitions.

## Troubleshooting

### API Key Issues

```
❌ Configuration Error: OPENAI_API_KEY not found in environment variables
```

**Solution**: Ensure `.env` file exists with valid `OPENAI_API_KEY`

### YAML Parsing Errors

```
⚠️ Attempt 1/3 failed: Could not extract valid YAML from LLM response
```

**Solution**: The LLM sometimes includes markdown formatting. The system will automatically retry. If it persists, try:
- Increasing `LLM_TEMPERATURE` for more creative responses
- Using a more capable model (e.g., `gpt-4o` instead of `gpt-3.5-turbo`)

### Missing Context Files

```
⚠️ Warning: Context file not found: outputs/01_PO_Output_Package.yaml
```

**Solution**: Ensure previous agents completed successfully. Check `/outputs` directory for expected files.

## Development

### Project Structure

```
FullSDLCTeam/
├── agents/                 # Agent markdown definitions
│   ├── 01_product_owner.md
│   ├── 02_analyst.md
│   └── ...
├── orchestrator/          # Core orchestration code
│   ├── orchestrator_runner.py
│   ├── llm_client.py
│   ├── agent_parser.py
│   ├── output_handler.py
│   ├── context_builder.py
│   ├── config.py
│   └── orchestrator_config.yaml
├── outputs/               # Generated YAML outputs
├── src/                   # Generated source code (future)
├── infra/                 # Generated infrastructure (future)
├── requirements.txt
├── .env.example
└── README.md
```

### Running Tests

```bash
# Test individual modules
python -c "from orchestrator.config import Config; c = Config(); c.validate()"
python -c "from orchestrator.llm_client import LLMClient; print('LLM client loaded')"
```

## License

[Your License Here]

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

For issues or questions:
- Check the Troubleshooting section
- Review agent markdown files for expected formats
- Verify `.env` configuration
