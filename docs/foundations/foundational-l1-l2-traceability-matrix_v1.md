# Foundational L1/L2 Traceability Matrix v1

Document Type: Traceability Matrix  
Status: Approved  
Owner: Architecture  
Version: v1  
Last Reviewed: 2026-04-21  
Source of Authority: symbolic-ontological-foundation_v1  
Supersedes: None  
Superseded by: None  
Related Tests: tests/test_foundational_symbolic.py, tests/test_foundational_ontological.py, tests/test_foundational_integration_hooks.py, tests/test_foundational_contracts.py  
Related Risks: R4, R12  
Related Decisions: ADR-0004-additive-foundational-layer-first

| Layer | Model | Contract / Invariant | Tests | Hook / Attachment |
|---|---|---|---|---|
| Layer 1: Symbolic Encoding | `SymbolicToken` | `symbolic_identity_invariant` | `tests/test_foundational_symbolic.py` | `semantic_kernel/foundational_hook.py` |
| Layer 1: Symbolic Encoding | `SymbolicToken` | `normalization_invariant` | `tests/test_foundational_symbolic.py`, `tests/test_foundational_contracts.py` | `semantic_kernel/foundational_hook.py` |
| Layer 2: Ontological Property | `OntologicalPropertyProfile` | `ontological_property_completeness_invariant` | `tests/test_foundational_ontological.py`, `tests/test_foundational_contracts.py` | `language/foundational_hook.py` |
| Layer 2: Ontological Property | `OntologicalPropertyProfile` | `essential_contextual_separation_invariant` | `tests/test_foundational_ontological.py`, `tests/test_foundational_contracts.py` | `language/foundational_hook.py` |

