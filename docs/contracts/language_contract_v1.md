# Language Contract v1

Document Type: Contract  
Status: Approved  
Owner: Architecture  
Version: v1  
Last Reviewed: 2026-04-21  
Source of Authority: ADR-0003  
Related Tests: tests/test_language.py  
Related Risks: R12  
Related Decisions: ADR-0003

## Contract Surface
- Container build, constraints, predication, reference, testability, feedback.

## Invariants
- No rank confusion.
- Predication must preserve role validity.

## Preconditions
- Ordered cognitive categories and valid references.

## Postconditions
- Testable container output and valid closure state.

## Forbidden Transitions
- Entity/quality inversion without explicit rule.

## Failure Semantics
- Reject with explicit `reason` and `missing_condition`.

## Trace Events
- Constraint violations, predication rejection, closure verdict.

## Verification Mapping
- Unit: `tests/test_language.py`
- Integration: `tests/test_chain.py`
- Risk-driven: `tests/test_contracts.py`
- CI gates: `r4-r12-gate`

## Code Surface
- Module paths: `arabic_engine/language/*.py`
- Public interface: language container and closure interfaces
- Guarded transitions: constraint and predication gates
- Feature flags: none
- Tracer hooks: `arabic_engine.trace.unified`
