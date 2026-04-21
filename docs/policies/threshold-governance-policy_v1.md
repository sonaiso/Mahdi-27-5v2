# Threshold Governance Policy v1

Document Type: Policy  
Status: Approved  
Owner: Architecture  
Version: v1  
Last Reviewed: 2026-04-21  
Source of Authority: ADR-0002  
Related Tests: tests/test_sigma2.py, tests/test_reference_predication_interface.py  
Related Risks: R4  
Related Decisions: ADR-0002, DL-2026-04-r4-r12-governance-status

## Policy
- Threshold bundles are versioned and locked per cycle.
- Mid-cycle threshold changes are prohibited unless authorized by a new ADR.
- Any threshold update must include risk impact and CI gate mapping updates.

## Current Baseline
- Active bundle: `arabic_engine/reference_predication/thresholds.py`
- State: v1 locked for current cycle.
