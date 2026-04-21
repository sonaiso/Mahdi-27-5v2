# Semantic Kernel Contract v1

Document Type: Contract  
Status: Approved  
Owner: Architecture  
Version: v1  
Last Reviewed: 2026-04-21  
Source of Authority: ADR-0003  
Related Tests: tests/test_semantic_kernel.py, tests/test_semantic_phases.py  
Related Risks: R12  
Related Decisions: ADR-0003

## Contract Surface
- Root kernel, pattern transform, form profile, transfer, compatibility, closure.

## Invariants
- Transfer equation consistency and compatibility gating.

## Preconditions
- Valid root/pattern/form representations.

## Postconditions
- Transfer output with closure and compatibility status.

## Forbidden Transitions
- Transfer execution with incompatible root-pattern pair.

## Failure Semantics
- Compatibility rejection with explicit reason and threshold context.

## Trace Events
- compatibility_checked, transfer_applied, closure_state.

## Verification Mapping
- Unit: `tests/test_semantic_kernel.py`
- Integration: `tests/test_semantic_integration.py`
- Risk-driven: `tests/test_semantic_phases.py`
- CI gates: `r4-r12-gate`

## Code Surface
- Module paths: `arabic_engine/semantic_kernel/*.py`
- Public interface: transfer and compatibility APIs
- Guarded transitions: compatibility/closure checks
- Feature flags: none
- Tracer hooks: `arabic_engine.trace.unified`
