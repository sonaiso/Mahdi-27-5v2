# Foundational L1/L2 Glossary v1

Document Type: Foundation  
Status: Approved  
Owner: Architecture  
Version: v1  
Last Reviewed: 2026-04-21  
Source of Authority: symbolic-ontological-foundation_v1  
Supersedes: None  
Superseded by: None  
Related Tests: tests/test_foundational_symbolic.py, tests/test_foundational_ontological.py  
Related Risks: R4  
Related Decisions: ADR-0004-additive-foundational-layer-first

## Canonical Terms
- symbolic identity invariant: equality constraint between Unicode symbol and declared codepoint.
- normalization invariant: token remains normalized under configured Unicode normalization form.
- representational stability: canonical/compatibility stability record for symbolic persistence.
- visual glyph: rendering form used for display, not the symbolic identity source.
- ontological property completeness invariant: required essential property keys are present for active scope.
- essential/contextual separation invariant: essential keys do not appear in contextual scope.
- attachment point: future integration location without forced runtime wiring.
- traceability mapping: explicit map from layer/model/contract to tests and hooks.

