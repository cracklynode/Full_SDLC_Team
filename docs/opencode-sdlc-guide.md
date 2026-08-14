# Running an SDLC Team with opencode Subagents

A practical guide for turning an idea into runnable code using the subagents that ship with opencode — and for salvaging the good parts of the `FullSDLCTeam` experiment (committed as the initial commit of this repo).

---

## TL;DR

You don't need a bespoke Python orchestrator. opencode already ships a team of subagents that cover the whole SDLC. You drive them with the **Task tool**, and the "handoff contract" between them is **files on disk** (not YAML stuffed into a prompt). Chain them roughly like this:

```
idea → StoryMapper → ArchitectureAnalyzer → CoderAgent → TestEngineer → BuildAgent → OpenDevopsSpecialist
```

Each stage writes real artifacts into your workspace (`docs/`, `src/`, `infra/`, `tests/`), so the next agent can just read them.

---

## What your experiment got right

Your `FullSDLCTeam` project proved the correct mental model:

- **SDLC is a sequential pipeline** — PO → Analyst → Designer → Developer → QA → DevOps is the right order.
- **Each stage consumes the previous stage's output.** Your `context_builder.py` did this by loading prior YAML; opencode does it better by pointing agents at files.
- **Your agent prompts were genuinely good.** The `01`–`03` markdown files (Product Owner, Analyst, Designer) define rich, traceable, NZ/Azure-aware outputs (story IDs, acceptance criteria, NFRs, cost envelopes). These are reusable as *handoff contracts* (see below).

The broken bits (unparsed `04`–`06`, missing YAML fences, docs-not-code outputs) are exactly the parts a real agent framework solves for you: subagents write real files with real tools instead of emitting a YAML *description* of files.

---

## Team map: your agents → built-in subagents

| Your agent (from `agents/`) | Built-in opencode subagent | What it produces |
|---|---|---|
| Orchestrator | `StageOrchestrator` | Runs stages with gating rules, validation, rollback |
| Product Owner | `StoryMapper` (+ `PrioritizationEngine`) | Epics, stories, vertical slices; prioritised backlog (RICE/WSJF) |
| Analyst | `ArchitectureAnalyzer` (+ `ContractManager`) | Bounded contexts, module boundaries, API contracts (OpenAPI) |
| Designer | `OpenFrontendSpecialist` | Design system, theme, UI component guidance |
| Developer | `CoderAgent` | Real source files, in order, to spec |
| QA | `TestEngineer` | Tests (TDD), test cases mapped to acceptance criteria |
| Build/CI check | `BuildAgent` | Type-check and build validation |
| (Review gate) | `CodeReviewer` | Code review, security, quality pass |
| DevOps | `OpenDevopsSpecialist` | CI/CD pipelines, infrastructure as code, deployment |
| (Docs) | `DocWriter`, `ADRManager` | README/docs, architecture decision records |

Supporting subagents: `explore` (understand an existing codebase fast), `Context Retriever` / `ContextScout` (load project context/standards), `ExternalScout` (fetch current library docs), `BatchExecutor` (run independent stages in parallel).

---

## Core mechanics

### 1. Launching a subagent (the Task tool)

```
Task tool
  subagent_type: "StoryMapper"      ← which role
  description:   "Map user story"    ← short label
  prompt:        "…detailed task…"   ← the brief + what to hand back
```

- Each call starts a **fresh agent with fresh context**. It does NOT remember the previous agent.
- The only thing that persists is **files on disk** and **your chat**. Treat the prompt as the complete brief.

### 2. Passing work between agents

Two reliable patterns:

- **Write-then-read (preferred for real work).** Tell agent A to write artifacts to `docs/01-prd.md`, `docs/02-functional-spec.md`, etc. Then tell agent B: "Read `docs/01-prd.md` and `docs/02-functional-spec.md`, then …".
- **Result-in-prompt (fine for small briefs).** The completed agent returns a message; paste the key facts into the next agent's prompt.

### 3. Resuming a long agent (the `task_id` trick)

If a stage is large, you can resume the same subagent session instead of starting fresh by passing its `task_id` back into the Task tool. Use this for long multi-step coding work (e.g. `CoderAgent` building a whole feature) so it keeps its working memory.

### 4. Parallel stages

`QA`, `CodeReviewer`, and `OpenDevopsSpecialist` all depend on the developer's output — but once code exists, `QA` (tests) and `OpenDevopsSpecialist` (pipeline/infra scaffolding) can run in parallel via `BatchExecutor`, then both feed `BuildAgent`.

---

## The handoff contract (reuse your good work)

Your agent markdown files defined excellent output shapes. Turn those into **files** instead of in-prompt YAML. Suggested layout in any project:

```
docs/
├── 01-prd.md                 ← from StoryMapper (product brief + backlog)
├── 02-functional-spec.md     ← from ArchitectureAnalyzer (flows, data, NFRs)
├── 03-design.md              ← from OpenFrontendSpecialist (UI/UX notes)
├── 04-api-contracts.yaml     ← from ContractManager (OpenAPI)
src/                          ← from CoderAgent (real code)
tests/                        ← from TestEngineer
infra/                        ← from OpenDevopsSpecialist (bicep/terraform, pipelines)
```

Steal these from your existing agent files — they're already well-formed:

- **Traceability**: keep story IDs like `S-1.1.1` flowing from PRD → spec → tests → code. `TestEngineer` can name tests by the story they cover.
- **NZ/Azure defaults** (from `06_DevOps.md`): Entra ID identity-first, Key Vault for secrets, `Australia East` region, NZD cost envelopes, NZ Privacy Act 2020 / ISM considerations.
- **Cost envelopes** (from `02_analyst.md` and `06_DevOps.md`): ask each infra decision to include a rough monthly NZD estimate.

---

## The chaining recipe (stage by stage)

### Stage 1 — Idea → Product brief & backlog
`subagent_type: "StoryMapper"`

> **Prompt:** "Here is the idea: <paste idea>. Interview me on up to 3 clarifying questions if needed, then produce `docs/01-prd.md` containing: problem statement, target users/jobs-to-be-done, goals + success metrics, MVP scope (in/out), personas, and epics/features/user stories with IDs and acceptance criteria. Use story ID scheme S-X.Y.Z. Return a one-paragraph summary plus the file path."

Follow with `PrioritizationEngine` if you want the backlog ranked:
> "Read `docs/01-prd.md`. Score the backlog with RICE/WSJF and return a prioritised list for the MVP slice."

### Stage 2 — Analyst (spec + architecture)
`subagent_type: "ArchitectureAnalyzer"` (optionally `ContractManager` for APIs)

> **Prompt:** "Read `docs/01-prd.md`. Produce `docs/02-functional-spec.md`: for each story define functional flows, business rules, edge cases, data model, and NFRs (performance/security/availability thresholds). Define bounded contexts and module boundaries. If there are APIs, write `docs/04-api-contracts.yaml` (OpenAPI 3.0). Return: recommended architecture, key decisions, and any open questions."

### Stage 3 — Designer
`subagent_type: "OpenFrontendSpecialist"`

> **Prompt:** "Read `docs/01-prd.md` and `docs/02-functional-spec.md`. Produce `docs/03-design.md`: user flows for the primary journeys, UI layout/component guidance, design tokens, and an accessibility checklist (WCAG 2.2 AA). Keep it feasible for the recommended architecture. Return a short summary."

### Stage 4 — Developer (writes real code)
`subagent_type: "CoderAgent"`

> **Prompt:** "Implement the system described in `docs/02-functional-spec.md`, `docs/03-design.md`, and `docs/04-api-contracts.yaml` (if present). Write real code into `src/` following a clean structure (e.g. `src/app`, `src/core`, `src/infra`). Include config, auth scaffolding, and a README with run instructions. Honour the NFRs and story traceability. Return a list of files created and how to run the app."

Keep it in one `CoderAgent` session (resume with `task_id`) so it holds context across a large build.

### Stage 5 — QA
`subagent_type: "TestEngineer"`

> **Prompt:** "Read `docs/01-prd.md`, `docs/02-functional-spec.md`, and the code in `src/`. Write automated tests into `tests/` (unit for core logic, integration for APIs) mapped to the stories and acceptance criteria. Use TDD where practical. Return a test summary and any defects you found."

### Stage 6 — Verification gate
`subagent_type: "BuildAgent"`

> **Prompt:** "Type-check and build the project in `src/` with its tests in `tests/`. Fix nothing; report failures, warnings, and the exact commands that fail."

If failures: send the report back to `CoderAgent`/`TestEngineer` (resume session), then re-run `BuildAgent`.

### Stage 7 — Review gate (optional)
`subagent_type: "CodeReviewer"`

> "Review `src/` for security (secrets, injection, auth) and code quality. Return findings with severity, referencing file:line."

### Stage 8 — DevOps
`subagent_type: "OpenDevopsSpecialist"`

> "Read `docs/02-functional-spec.md` (NFRs) and the code in `src/`. Create `infra/` with IaC (Bicep/Terraform) and a CI/CD pipeline (Azure DevOps or GitHub Actions) for build → test → deploy. Include monitoring/alerting, backup/DR, and a monthly NZD cost estimate. Use Azure-first, Entra ID, Key Vault defaults."

---

## Copy-paste starter flow (one idea, end to end)

1. **StoryMapper** — prompt from Stage 1 above.
2. **ArchitectureAnalyzer** — prompt from Stage 2.
3. **OpenFrontendSpecialist** — prompt from Stage 3.
4. **CoderAgent** — prompt from Stage 4 (resume the same session if it runs long).
5. **TestEngineer** — prompt from Stage 5.
6. **BuildAgent** — prompt from Stage 6. Fix failures → back to 4/5 → re-run.
7. **CodeReviewer** (optional) — prompt from Stage 7.
8. **OpenDevopsSpecialist** — prompt from Stage 8 (can start in parallel with 5/7 once code exists).

That single sequence replaces your whole Python orchestrator, and the end state is a runnable repo, not a stack of YAML plans.

---

## Gotchas & tips

- **Fresh context per agent** — never assume an agent remembers the previous one; always tell it which files to read. This is the #1 failure mode.
- **Use `explore` first** if you're working on an existing codebase, so later agents get an accurate picture.
- **Put acceptance criteria in the prompt** for the agent that produces the artifact, and name test/code by story ID so traceability is checkable.
- **Gate on real checks**, not vibes: `BuildAgent` (compiles) and `TestEngineer` (tests pass) are the quality gates your `Orchestrator.md` described but never enforced.
- **Keep secrets out of prompts and files** — have agents reference `.env` / Key Vault placeholders (as your `06_DevOps.md` already does).
- **When in doubt, use `StageOrchestrator`** for a formal multi-stage run with explicit gates and rollback, and `BatchExecutor` for the stages that can run in parallel.