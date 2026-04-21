# Judgement Contract v1

Document Type: Contract  
Status: Approved  
Owner: Architecture  
Version: v1  
Last Reviewed: 2026-04-21  
Source of Authority: ADR-0003  
Related Tests: tests/test_semantic_integration.py, tests/test_chain.py  
Related Risks: R12  
Related Decisions: ADR-0003

## Contract Surface
- Judgement model, transition engine, closure engine.

## Invariants
- Judgement carries direction, criterion, proposition, rank, reason.

## Preconditions
- Valid proposition closure and admissible upstream outputs.

## Postconditions
- Consistent judgement state and closure trace.

## Forbidden Transitions
- Transition without proposition or trace context.

## Failure Semantics
- Explicit reject/suspend with governance reason fields.

## Trace Events
- transition_start, transition_reject, closure_result.

## Verification Mapping
- Unit: `tests/test_semantic_integration.py`
- Integration: `tests/test_chain.py`
- Risk-driven: `tests/test_contracts.py`
- CI gates: `r4-r12-gate`

## Code Surface
- Module paths: `arabic_engine/judgement/*.py`
- Public interface: judgement model + transition APIs
- Guarded transitions: judgement transition gates
- Feature flags: none
- Tracer hooks: `arabic_engine.trace.unified`
