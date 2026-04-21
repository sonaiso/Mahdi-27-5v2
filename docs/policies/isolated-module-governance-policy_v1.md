# Isolated Module Governance Policy v1

Document Type: Policy  
Status: Approved  
Owner: Architecture  
Version: v1  
Last Reviewed: 2026-04-21  
Source of Authority: ADR-0001  
Related Tests: tests/test_reference_predication_interface.py, tests/test_sigma2.py  
Related Risks: R4, R12  
Related Decisions: ADR-0001, DL-2026-04-r4-r12-governance-status

## Policy
- `reference_predication` remains isolated by policy in current phase.
- Isolation is controlled, not open-ended.

## Mandatory Checkpoint
- Formal review at end of Phase B.
- Outcome must be one of:
  1. merge candidate,
  2. remain isolated with revised conditions,
  3. de-scope/redesign.

**Principle:** Isolated by policy, not by drift.
