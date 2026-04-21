# ADR-0004 / قرار معماري: Additive Foundational Layer First

Document Type: ADR  
Status: Accepted  
Owner: Architecture  
Version: v1  
Last Reviewed: 2026-04-21  
Source of Authority: phased-execution-plan_v1  
Supersedes: None  
Superseded by: None  
Related Tests: tests/test_foundational_symbolic.py, tests/test_foundational_ontological.py, tests/test_foundational_integration_hooks.py  
Related Risks: R4, R12  
Related Decisions: ADR-0003-core-extension-experimental-classification, DL-2026-04-contract-surface-policy

## Decision
Adopt an additive foundational implementation for v1 (letter + diacritic) before any migratory refactor of existing runtime layers.

## Rationale
- Separates model validity testing from broad operational restructuring.
- Preserves controlled contract-surface verification (invariants, failure semantics, traceability, tests).
- Prevents premature coupling with higher-order ordering/composition/judgement semantics.

## Consequences
- Layer 1 (Symbolic Encoding) and Layer 2 (Ontological Property) are implemented as independent foundational package.
- `semantic_kernel` and `language` receive hook/adapters only (no mandatory runtime wiring).
- Migration to deeper runtime layers is deferred until foundational acceptance gates are stable.

