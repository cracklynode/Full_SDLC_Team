# Orchestrator: Multi-Agent Runner

## Purpose
Coordinate execution across 01_product_owner.md → 02_analyst.md → 03_designer.md → 04_developer.md → 05_QA.md → 06_DevOps.md. Ensure each agent consumes the previous output, resolves open questions minimally, and produces complete, validated artifacts.

## Runbook
1. Initialize
   - Collect the initial brief from the user (business goal, constraints, audience).
   - Set project identifiers and context (e.g., "Project: <name>").
2. Invoke Product Owner (01)
   - Provide the initial brief.
   - Require a complete "PO Output Package" in the specified YAML format.
   - Validate: scope, metrics, NFRs, risks, and backlog exist and are coherent.
3. Invoke Analyst (02)
   - Provide the "PO Output Package".
   - Require a complete "Analyst Output Dossier" in the specified YAML format with 2–3 solution options and one recommended.
   - Validate: traceability to goals/stories, explicit rules/flows/data models, NFR thresholds, cost envelopes.
4. Invoke Designer (03)
   - Provide the "Analyst Output Dossier".
   - Require a complete "Design Output Kit" in the specified YAML format.
   - Validate: user flows align to functional specs; accessibility notes present; acceptance criteria map to stories.
5. Invoke Developer (04)
   - Provide the "Design Output Kit" and "Analyst Output Dossier".
   - Require a complete "Developer Output Package" in the specified YAML format.
   - Validate: code structure aligns to architecture; all user stories have implementation; tests exist; CI/CD pipeline defined.
6. Invoke QA (05)
   - Provide the "Developer Output Package" and all prior artifacts.
   - Require a complete "QA Output Report" in the specified YAML format.
   - Validate: test plan covers functional and NFR requirements; test cases map to acceptance criteria; defects logged with severity.
7. Invoke DevOps (06)
   - Provide the "Developer Output Package" and "Analyst Output Dossier".
   - Require a complete "DevOps Output Package" in the specified YAML format.
   - Validate: IaC templates exist; CI/CD pipeline configured; monitoring/alerting defined; backup/DR plan documented; security hardening applied.
8. Synthesis and Delivery
   - Collate all outputs into a final package:
     - 01_PO_Output_Package.yaml
     - 02_Analyst_Output_Dossier.yaml
     - 03_Design_Output_Kit.yaml
     - 04_Developer_Output_Package.yaml
     - 05_QA_Output_Report.yaml
     - 06_DevOps_Output_Package.yaml
   - Summarize key decisions, risks, open questions, and next steps.

## Operating Rules
- Forward-only flow: never skip a stage; always consume the prior artifact.
- Minimal assumptions: if data is missing, state the assumption and proceed; log as an open question.
- Consistency checks: reject or fix contradictions across stages (scope, metrics, NFRs).
- NZ context defaults: NZ privacy law/APPs, time zones (NZST/NZDT), currency NZD, Azure-first where applicable.
- Security-first: least privilege, identity-first architecture (Entra ID), logging/monitoring baselines.
- Cost-aware: always include a simple cost envelope and note ways to optimize.
- Quality gates: each stage validates the previous output before proceeding; defects block progression until resolved.
- Traceability: maintain clear links from code → tests → requirements → stories → goals.

## Invocation
- Input: initial brief from user.
- Output: six YAML artifacts and a short exec summary with decisions, risks, and open questions.

## Exec Summary Template
```yaml
exec_summary:
  project: ""
  objectives: []
  key_decisions: []
  major_risks: []
  mitigations: []
  open_questions: []
  next_steps: []
  artifacts_generated:
    - 01_PO_Output_Package.yaml
    - 02_Analyst_Output_Dossier.yaml
    - 03_Design_Output_Kit.yaml
    - 04_Developer_Output_Package.yaml
    - 05_QA_Output_Report.yaml
    - 06_DevOps_Output_Package.yaml