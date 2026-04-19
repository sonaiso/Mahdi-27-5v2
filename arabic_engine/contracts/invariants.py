"""
Invariant checker — validates cross-cutting invariants.
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_weight import WeightedUnit


class InvariantChecker:
    """Checks structural invariants that must hold at all times."""

    @staticmethod
    def check_weighted_unit(unit: WeightedUnit) -> list[GateResult]:
        """Validate invariants on a WeightedUnit.

        Invariants:
        1. If weight is closed, singular must also be closed.
        2. If singular is not closed, weight cannot be closed.
        """
        results: list[GateResult] = []

        # Invariant 1: weight closed → singular closed
        if unit.weight.weight_closed and not unit.singular.singular_closed:
            results.append(GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.WEIGHT_MIZAN,
                reason="الوزن مقفل لكن المفرد غير مقفل — انتهاك ثابت",
                missing_condition="singular_before_weight",
            ))

        if not results:
            results.append(GateResult(
                verdict=GateVerdict.PASS,
                layer=Layer.WEIGHT_MIZAN,
            ))

        return results
