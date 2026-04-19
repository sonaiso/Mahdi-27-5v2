"""
Composition eligibility gate — enforces the weight-closure prerequisite.

No unit may enter composition (Layer 5) unless it is fully closed
at both singular and weight levels.
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_weight import WeightedUnit


class CompositionEligibilityGate:
    """Gate that checks whether a weighted unit may participate in composition."""

    LAYER = Layer.COMPOSITIONAL_ROLES

    @staticmethod
    def evaluate(unit: WeightedUnit) -> GateResult:
        """composition_eligible(u) ⟺
            singular_membership(u) ∧ singular_completeness(u) ∧ ¬singular_blocker(u) ∧
            weight_membership(u) ∧ weight_completeness(u) ∧ ¬weight_blocker(u)
        """
        if not unit.singular.singular_closed:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=CompositionEligibilityGate.LAYER,
                reason="المفرد غير مقفل — لا يجوز الدخول في التركيب",
                missing_condition="singular_closed",
            )

        if not unit.weight.weight_closed:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=CompositionEligibilityGate.LAYER,
                reason="الوزن غير مقفل — لا تركيب بلا ميزان",
                missing_condition="weight_closed",
            )

        return GateResult(
            verdict=GateVerdict.PASS,
            layer=CompositionEligibilityGate.LAYER,
        )
