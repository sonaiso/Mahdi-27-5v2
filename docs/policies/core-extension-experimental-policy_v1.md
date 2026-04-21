# Core Extension Experimental Policy v1

Document Type: Policy  
Status: Approved  
Owner: Architecture  
Version: v1  
Last Reviewed: 2026-04-21  
Source of Authority: ADR-0003  
Related Tests: tests/test_semantic_kernel.py, tests/test_chain.py  
Related Risks: R12  
Related Decisions: ADR-0003

## Classification Rules
- Core: mandatory system nucleus with stable governance.
- Extension: production feature not in critical nucleus.
- Experimental: controlled scope, explicit exit criteria, no implicit promotion.

## Promotion Rule
- No module may be promoted without:
  1. contract completeness,
  2. failure semantics defined,
  3. test/risk/CI linkage,
  4. documented decision under `docs/decisions/`.
