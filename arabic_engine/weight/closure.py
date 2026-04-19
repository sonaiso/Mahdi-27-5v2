"""
Weight closure engine — orchestrates Layer 4 in strict order.

Requires that the singular unit is fully closed before weight processing.
Includes an optional semantic kernel closure gate when semantic data is present.
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_weight import WeightedUnit

from .legality import WeightLegalityGate
from .derivation import DerivationEligibilityGate


class WeightClosureEngine:
    """Orchestrates the weight/mizan closure pipeline (Layer 4)."""

    @staticmethod
    def close(weighted: WeightedUnit) -> list[GateResult]:
        """Run the weight closure pipeline.

        Pre-condition: singular must be fully closed.
        Returns a list of GateResults for each sub-gate attempted.
        """
        results: list[GateResult] = []

        # Anti-jump: singular must be closed first
        if not weighted.singular.singular_closed:
            r = GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.WEIGHT_MIZAN,
                reason="المفرد غير مقفل — لا يجوز فتح الوزن",
                missing_condition="singular_closed",
            )
            results.append(r)
            return results

        # Legality sub-gate
        r_legality = WeightLegalityGate.evaluate(weighted.weight)
        results.append(r_legality)
        if not r_legality.passed:
            weighted.weight.closure = (
                ClosureStatus.SUSPENDED
                if r_legality.verdict is GateVerdict.SUSPEND
                else ClosureStatus.BLOCKED
            )
            return results

        # Derivation sub-gate
        r_derivation = DerivationEligibilityGate.evaluate(weighted.weight)
        results.append(r_derivation)
        if not r_derivation.passed:
            weighted.weight.closure = (
                ClosureStatus.SUSPENDED
                if r_derivation.verdict is GateVerdict.SUSPEND
                else ClosureStatus.BLOCKED
            )
            return results

        # Optional: Semantic kernel closure gate
        # Only runs if a semantic_transfer result is attached to the weight record.
        # If no semantic data is present, the gate is skipped (backward compatible).
        if weighted.weight.semantic_transfer is not None:
            from arabic_engine.semantic_kernel.closure import (
                SemanticKernelClosureEngine,
            )
            sem_results = SemanticKernelClosureEngine.close(
                weighted.weight.semantic_transfer
            )
            results.extend(sem_results)
            if not all(r.passed for r in sem_results):
                weighted.weight.closure = (
                    ClosureStatus.SUSPENDED
                    if any(
                        r.verdict is GateVerdict.SUSPEND for r in sem_results
                    )
                    else ClosureStatus.BLOCKED
                )
                return results

        weighted.weight.closure = ClosureStatus.CLOSED
        return results
