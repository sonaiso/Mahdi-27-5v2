"""
Derivation eligibility gate — validates transition potentials.

Answers: What temporal, spatial, and descriptive potentials does this weight carry?
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.enums_weight import WeightEligibility
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_weight import WeightRecord


class DerivationEligibilityGate:
    """Gate that evaluates derivation/transition eligibility of a weight."""

    LAYER = Layer.WEIGHT_MIZAN

    @staticmethod
    def evaluate(record: WeightRecord) -> GateResult:
        """Check that an eligible weight has its trace fields populated."""
        if record.eligibility is WeightEligibility.NOT_ELIGIBLE:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=DerivationEligibilityGate.LAYER,
                reason="الوحدة غير قابلة للوزن — لا فحص اشتقاقي",
                missing_condition="eligibility",
            )

        # At least one structural eligibility flag must be set
        if not (record.noun_eligible or record.verb_eligible or record.particle_eligible):
            return GateResult(
                verdict=GateVerdict.SUSPEND,
                layer=DerivationEligibilityGate.LAYER,
                reason="لم تُحدَّد أي أهلية بنيوية (اسم/فعل/حرف)",
                missing_condition="structural_eligibility",
            )

        return GateResult(
            verdict=GateVerdict.PASS,
            layer=DerivationEligibilityGate.LAYER,
        )
