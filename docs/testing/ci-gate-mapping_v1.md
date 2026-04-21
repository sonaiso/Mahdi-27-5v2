# CI Gate Mapping v1

Document Type: Testing Governance  
Status: Approved  
Owner: Architecture  
Version: v1  
Last Reviewed: 2026-04-21  
Source of Authority: DL-2026-04-r4-r12-governance-status  
Related Tests: tests/test_sigma2.py, tests/test_contracts.py, tests/test_reference_predication_interface.py  
Related Risks: R4, R12  
Related Decisions: DL-2026-04-r4-r12-governance-status

## Gate Mapping
- Gate: `r4-r12-gate`
- Risks: R4, R12
- Required tests:
  - `tests/test_sigma2.py`
  - `tests/test_reference_predication_interface.py`
  - `tests/test_contracts.py`

## Rule
PRs touching `arabic_engine/reference_predication/**` or mapped risk surfaces must pass `r4-r12-gate`.
