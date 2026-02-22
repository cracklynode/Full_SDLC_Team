# AGENTS.md - Full SDLC Team

## Project Overview

This repository contains role-based AI agent templates for a complete product delivery lifecycle. It's a documentation/template project - no executable code.

---

## File Structure

- `00_custom_instructions_orchestration.md` - Orchestration rules
- `01_product_owner.md` - Product Owner agent
- `02_analyst.md` - Analyst agent
- `03_designer.md` - Designer agent
- `04_developer.md` - Developer agent
- `05_QA.md` - QA agent
- `06_DevOps.md` - DevOps agent

---

## Build/Lint/Test Commands

**None** - This is a documentation-only project. No build, lint, or test commands exist.

### YAML Artifact Naming

| Agent | YAML Artifact |
|-------|---------------|
| Product Owner | `01_PO_Output_Package.yaml` |
| Analyst | `02_Analyst_Output_Dossier.yaml` |
| Designer | `03_Design_Output_Kit.yaml` |
| Developer | `04_Developer_Output_Package.yaml` |
| QA | `05_QA_Output_Report.yaml` |
| DevOps | `06_DevOps_Output_Package.yaml` |

---

## Code Style Guidelines

### Markdown Formatting

- Use ATX headers (`#`, `##`, `###`) for hierarchy
- Use fenced code blocks with language identifiers
- Use tables for structured data
- Keep lines to 100 characters max
- Use `---` for section separation

### YAML Output Conventions

- Valid, parseable YAML only
- 2-space indentation
- Consistent key ordering
- Full descriptive key names

### YAML Block Format

```yaml
# 01_PO_Output_Package.yaml
<full YAML content>
```

### Code Artifact Blocks

```csharp
// <filename>
<code>
```

```typescript
// <filename>
<code>
```

```python
# <filename>
<code>
```

```bicep
// <filename>
<code>
```

---

## Naming Conventions

- Use kebab-case: `01_product_owner.md`, `01_PO_Output_Package.yaml`
- Prefix YAML with sequential numbers (01-06)
- Agent numbers: 01=PO, 02=Analyst, 03=Designer, 04=Developer, 05=QA, 06=DevOps

---

## Agent Execution Flow

### Agent Range

Specify range (e.g., `1-3`, `1-6`). Always start at 1, end at 1-6. Forward-only.

### Required Inputs

| Agent | Required |
|-------|----------|
| 01 - PO | Initial brief |
| 02 - Analyst | 01_PO_Output_Package.yaml |
| 03 - Designer | 02_Analyst_Output_Dossier.yaml |
| 04 - Developer | 02 + 03 artifacts |
| 05 - QA | 04 + all prior |
| 06 - DevOps | 04, 02 artifacts |

### Synthesis & Delivery

After agents run:
1. Output all YAML artifacts in order
2. Re-emit Developer code with language fences
3. Produce exec summary: project, objectives, key decisions, risks, mitigations, open questions, next steps, artifacts

---

## NZ-Specific Defaults

- **Privacy**: NZ Privacy Act
- **Time zone**: NZST/NZDT
- **Currency**: NZD
- **Cloud**: Azure-first
- **Compliance**: NZ regulatory context

---

## Error Handling

### Missing Data
- Make smallest reasonable assumption
- Document explicitly
- Log as open question

### Validation per Agent

- **PO**: Scope/goals align, metrics present
- **Analyst**: Requirements trace to goals, costs clear
- **Designer**: Flows consistent, accessibility considered
- **Developer**: Architecture aligns, stories covered
- **QA**: Traceability, defects logged
- **DevOps**: IaC aligned, monitoring covered

---

## Traceability

Maintain: Goals → Epics → Stories → Requirements → Design → Code → Tests → DevOps

---

## Operating Rules

1. **Forward-only**: Sequential execution within range
2. **Minimal assumptions**: Document all assumptions
3. **Consistency**: Avoid contradictions
4. **Security-first**: Consider security at every stage
5. **Cost-aware**: Include NZD costs
6. **Traceability**: Clear links between artifacts
