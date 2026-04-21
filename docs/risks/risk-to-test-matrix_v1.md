# Risk-to-Test Matrix v1

**Status:** v1 locked for this cycle  
**Gate:** `r4-r12-gate`

| Risk ID | Scope | Required Tests | Failure Modes Covered | Acceptance Criteria | Gate |
|---|---|---|---|---|---|
| R4 | Edge/constraint completeness for Σ1→Σ2 and reference_predication contracts | `tests/test_sigma2.py`, `tests/test_contracts.py`, `tests/test_reference_predication_interface.py` | Invalid Σ1 admissibility, invalid ratio vectors, inconsistent G_i positional validity, causal/case contradiction, unstable fixed-khabar reference, referential alignment failure, contract gate rejections | All scoped tests pass; no failing edge/failure-path case; scoped coverage floor for `arabic_engine.reference_predication` and `arabic_engine.contracts` is met | `r4-r12-gate` |
| R12 | Strategy quality: risk-driven coverage vs count-driven expansion | `tests/test_sigma2.py`, `tests/test_reference_predication_interface.py`, `tests/test_contracts.py` | Missing risk-linked assertions, regression mismatch between interface and direct builder, policy drift in transition invariants | Each required test remains explicitly risk-linked; regression parity checks pass; no PR touching scoped files merges without successful gate | `r4-r12-gate` |

## Minimum row policy (mandatory)

- Risk ID
- Explicit test files
- Covered failure-mode categories
- Acceptance criterion
- Gate name that enforces closure
