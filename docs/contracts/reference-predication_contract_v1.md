# Reference-Predication Contract v1

Document Type: Contract  
Status: Approved  
Owner: Architecture  
Version: v1  
Last Reviewed: 2026-04-21  
Source of Authority: ADR-0001  
Related Tests: tests/test_sigma2.py, tests/test_reference_predication_interface.py, tests/test_contracts.py  
Related Risks: R4, R12  
Related Decisions: ADR-0001, ADR-0002, DL-2026-04-r4-r12-governance-status

## Contract Surface
- Σ1→Σ2 matrix builder, stable interface, threshold governance.

## Invariants
- Referential coherence and guarded grammatical factor transitions.

## Preconditions
- Valid Σ1 admissibility and threshold bundle availability.

## Postconditions
- Stable Σ2 matrix with deterministic policy-conformant outputs.

## Forbidden Transitions
- Ungated direct integration into MasterChain during current phase.

## Failure Semantics
- Reject/suspend must include `reason`, `layer`, `missing_condition`.

## Trace Events
- threshold_validation, contradiction_detected, interface_fallback, closure_verdict.

## Verification Mapping
- Unit: `tests/test_sigma2.py`
- Integration: `tests/test_reference_predication_interface.py`
- Risk-driven: `tests/test_contracts.py`
- CI gates: `r4-r12-gate`

## Code Surface
- Module paths: `arabic_engine/reference_predication/*.py`
- Public interface: `ReferencePredicationInterface`
- Guarded transitions: Σ1 admissibility + threshold gates
- Feature flags: `ARABIC_ENGINE_ENABLE_REFERENCE_PREDICATION`
- Tracer hooks: `arabic_engine.trace.unified`
