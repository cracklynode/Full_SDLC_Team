# AI Product Delivery Playbook – Multi‑Agent Templates

## Overview

This repository contains a set of role‑based “agent” templates plus a top‑level orchestration file that together model a complete product delivery lifecycle:

0. Custom Instructions & Orchestration
1. Product Owner
2. Analyst
3. Designer
4. Developer
5. QA
6. DevOps

Each Markdown file defines one agent’s purpose, operating principles, inputs, process, outputs, and a structured output format (usually YAML). You can use these files in two main ways:

- As a playbook for humans to follow and complete.
- As system prompts or instructions for an AI assistant to act as that role and generate the corresponding outputs.

The intent is that you move sequentially from 01 to 06, carrying forward and refining the artefacts at each step, coordinated via the 00 orchestration file.

---

## Files in this repository

### 00_custom_instructions_orchestration.md

Defines the overarching orchestration and custom instructions for how the AI should behave across all agents.

Typically covers:

- How the AI should:
  - Ask which agents to run (for example, 1–3, 1–4, 1–6).
  - Enforce forward‑only flow (1 → 2 → 3 → … up to the chosen end).
  - Maintain and reuse YAML artefacts between steps.
- NZ‑specific defaults and constraints, such as:
  - NZ privacy and compliance context.
  - NZ time zone and NZD currency.
  - Azure‑first approach where applicable.
- Required outputs and naming conventions for YAML artefacts, for example:
  - `01_PO_Output_Package.yaml`
  - `02_Analyst_Output_Dossier.yaml`
  - `03_Design_Output_Kit.yaml`
  - `04_Developer_Output_Package.yaml`
  - `05_QA_Output_Report.yaml`
  - `06_DevOps_Output_Package.yaml`
- Final synthesis behaviour:
  - Re‑emitting all YAML artefacts.
  - Re‑emitting Developer code from `code_artifacts`.
  - Producing an `exec_summary` block.

This file is what you place into your LLM tool’s custom instructions or system prompt so that the agent knows how to coordinate all other role templates.

### 01_product_owner.md

Defines the Product Owner agent.

- Clarifies business problem, goals, success metrics, and constraints.
- Describes target users, personas, jobs to be done, pains and gains.
- Establishes MVP scope, in‑scope/out‑of‑scope, and key risks and assumptions.
- Produces:
  - Product Brief
  - Initial backlog (epics, features, stories)
  - Non‑functional requirements
  - Interfaces and integrations list
  - Initial timeline and milestones
- Provides a YAML “PO Output Package” template that you can fill in.

### 02_analyst.md

Defines the Analyst agent.

- Takes the Product Owner output and turns it into detailed, testable specifications.
- Models processes, interactions, and data.
- Translates non‑functionals into concrete, measurable criteria.
- Proposes solution options with trade‑offs and a recommended option, including high‑level cost envelopes.
- Produces:
  - Functional specifications per story
  - Process/sequence/state models (textual)
  - Data models and retention/privacy notes
  - Non‑functional specs
  - Solution options and recommended solution
- Provides a YAML “Analyst Output Dossier” template.

### 03_designer.md

Defines the Designer agent.

- Designs user flows, information architecture, and interfaces based on the Analyst Dossier.
- Focuses on usability, accessibility (WCAG 2.2 AA), and consistency with a design system.
- Specifies components, tokens, and interaction behaviours.
- Produces:
  - User flow diagrams (textual)
  - IA/sitemap
  - Wireframe descriptions and states
  - Interaction specifications
  - Design system tokens and components
  - Accessibility and usability checks
  - Design acceptance criteria and handoff notes
- Provides a YAML “Design Output Kit” template.

### 04_developer.md

Defines the Developer agent.

- Translates the design and specs into production‑ready code and infrastructure.
- Emphasises code quality, security, performance, testability, and DevOps readiness.
- Describes expected solution structure, key components, and technologies.
- Produces:
  - Source code structure and key files
  - Database migrations and seed data
  - Configuration patterns and secrets handling
  - Test suites (unit, integration, E2E)
  - CI/CD pipeline outline
  - Infrastructure‑as‑code outline
  - Documentation and handover notes for QA
- Provides a structured “Developer Output Package” describing solution structure, tests, pipelines, infra, and open questions.

### 05_QA.md

Defines the QA agent.

- Plans and executes testing to validate functional and non‑functional requirements.
- Uses risk‑based, requirements‑driven testing across functional, performance, security, and accessibility areas.
- Produces:
  - Test plan and scope
  - Detailed test cases with traceability to stories and NFRs
  - Execution results, defect log, and coverage metrics
  - Performance, security, and accessibility reports
  - UAT report and release readiness summary
  - Handoff notes for DevOps and operations
- Provides a comprehensive YAML “QA Output Package” template.

### 06_DevOps.md

Defines the DevOps agent.

- Focuses on deployment, environments, monitoring, and operational readiness.
- Uses outputs from Developer and QA (pipelines, IaC, test results, runbooks) to run and operate the system reliably.
- Typically covers:
  - Environment strategy and configuration
  - CI/CD implementation details
  - Monitoring, alerting, logging
  - Operational runbooks and rollback plans
  - Release and change processes

Refer to `06_DevOps.md` itself for the exact structure and templates.

---

## Typical workflow

Use the files in numeric order. At each step, you create or refine artefacts and feed them into the next step.

1. Product Owner (01)
   - Start with the problem, goals, personas, and constraints.
   - Complete the Product Brief and initial backlog in the 01 template.

2. Analyst (02)
   - Take the Product Brief and backlog as input.
   - Produce the Analyst Output Dossier with functional specs, models, and solution options.

3. Designer (03)
   - Use the Analyst Dossier to design flows, IA, and interfaces.
   - Produce the Design Output Kit with wireframes, interaction specs, and accessibility notes.

4. Developer (04)
   - Use all previous artefacts to shape architecture, code, tests, and infra.
   - Produce the Developer Output Package for QA and DevOps.

5. QA (05)
   - Use PO, Analyst, Designer, and Developer outputs to define comprehensive testing.
   - Produce the QA Output Package and release readiness evidence.

6. DevOps (06)
   - Use Developer and QA outputs to set up pipelines, infra, monitoring, and runbooks.
   - Close the loop with feedback into backlog and future iterations.

You can iterate within and across steps (for example, revisiting Product Owner scope when QA surfaces risks).

---

## How to use with your LLM tool (Projects / Notebooks)

If your LLM tool supports Projects, Notebooks, or similar persistent contexts, a simple and robust setup is:

1. Create a new Project or Notebook for your product or client.
2. Add the orchestration instructions:
   - Open the tool’s “Custom instructions”, “System prompt”, or equivalent.
   - Paste the full contents of `00_custom_instructions_orchestration.md` there.
   - Save or apply those instructions so every chat in this Project/Notebook inherits them.
3. Upload the role templates as project files:
   - Upload `01_product_owner.md` through `06_DevOps.md` into the Project / Files area.
   - Optionally keep them in an `instructions/` folder in your source repo as the master copy.
4. Start a conversation inside that Project/Notebook and:
   - Provide your project brief (business context, goals, constraints).
   - Tell the AI which agents you want to run in this session, for example:
     - “Run agents 1–3” (PO → Analyst → Designer).
     - “Run agents 1–6” (full SDLC chain).
   - The orchestration instructions from `00_custom_instructions_orchestration.md` should:
     - Enforce the correct order (no skipping within the chosen range).
     - Maintain artefact names and structure.
     - Re‑emit all generated YAML (and developer code) back to you.

If your tool lets you attach or reference project files in a prompt, you can also explicitly say:

```text
Use the instructions in 00_custom_instructions_orchestration.md as your governing system.
Use 01_product_owner.md to 06_DevOps.md as the role definitions.
For this run, execute agents 1–4 and output the corresponding YAML artefacts.

## Using these files with an AI assistant (step by step)

Even without a Project feature, you can run the agents manually in sequence.

1. Prepare your project context
Before you start with an agent:

Gather a short description of the product idea or change.
List known constraints (budget, tech stack, compliance, timelines).
Collect any existing artefacts you want the agent to respect (policies, diagrams, previous docs).
2. Run a single agent
For a given role (for example, Product Owner):

Start a new chat.
Paste or reference the corresponding agent file content.
Provide your project context.
Ask the AI to follow the agent’s Process and Outputs sections, and to populate the output format exactly as defined in the file (usually the YAML template at the end).
Review and refine the generated output with follow‑up prompts.

Example prompt pattern for 01_product_owner.md:

You are acting as the Product Owner agent described in the spec below.

[PASTE CONTENT OF 01_product_owner.md]

Here is my project context:
- ...

Follow the Process in the spec and produce the Outputs in the exact YAML structure under "Output Format (PO Output Package)".
Only output valid YAML.

You can reuse this pattern for the other agents by swapping the file and output package name.

3. Chain agents together
After you have acceptable output from one agent:

Clean up and save the output (for example, commit the YAML to your repo).
Start a new chat for the next agent.
Provide:
The next agent’s Markdown file, and
The previous agent’s output as input.
Example, moving from Product Owner to Analyst:

You are acting as the Analyst agent described in the spec below.

[PASTE CONTENT OF 02_analyst.md]

Here is the PO Output Package from the previous step:
[PASTE PO OUTPUT YAML]

Follow the Process in the spec and produce the Analyst Output Dossier in the exact YAML structure under "Output Format (Analyst Output Dossier)".
Only output valid YAML.

Continue this pattern through Designer, Developer, QA, and DevOps, always feeding the previous artefacts forward.

## Using these files without an AI assistant
You can also treat each Markdown file as a guided template for manual work.

For each agent:

Read the Purpose and Operating Principles to align your mindset.
Work through the Process steps as a checklist.
Use the Output Format template at the bottom of the file as your document skeleton.
Fill in the YAML (or structured sections) by hand, committing them to version control.
This works well when you want consistent documentation while keeping humans firmly in the loop.

## Suggested way to organise project artefacts
One simple pattern is to keep the templates separate from project‑specific outputs:

instructions/00_custom_instructions_orchestration.md
instructions/01_product_owner.md to instructions/06_DevOps.md
project/po/01_PO_Output_Package.yaml
project/analyst/02_Analyst_Output_Dossier.yaml
project/designer/03_Design_Output_Kit.yaml
project/developer/04_Developer_Output_Package.yaml
project/qa/05_QA_Output_Report.yaml
project/devops/06_DevOps_Output_Package.yaml
This makes it clear which parts are reusable templates and which are specific to a given product or client.

## Customising the templates
You are encouraged to adapt these files to your context.

Examples of customisation:

Tighten or relax certain operating principles (for example, cost focus, regulatory focus).
Extend the YAML schemas with fields you always need (for example, data residency, backup/RPO/RTO).
Swap technology references to match your standard stack.
Add organisation‑specific checklists for security, compliance, and governance.
When you customise:

Keep the Purpose, Inputs, Process, and Outputs sections aligned so that downstream roles still get what they expect.
Update 00_custom_instructions_orchestration.md so the orchestration logic and artefact naming still match the actual templates.
Version your templates so you know which version a given project was based on.

## How to get started quickly
Copy these Markdown files into your own repo under an instructions/ folder.
In your LLM tool:
Create a Project or Notebook.
Paste 00_custom_instructions_orchestration.md into the custom instructions/system prompt.
Upload 01_product_owner.md to 06_DevOps.md as Project Files.
Pick a small, low‑risk product idea.
Run through at least Product Owner → Analyst → Designer using the orchestrated agent.
Review and adjust the outputs to fit your organisation.
Decide which artefacts you want to formalise as required for future projects.
Over time, this set of agents plus the orchestration instructions becomes your standard, repeatable path from idea to running, monitored software.