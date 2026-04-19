"""
Weight legality gate — validates built/inflected and derivation legality.

Answers: Is the weight legally formed?
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.enums_weight import WeightEligibility
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_weight import WeightRecord


class WeightLegalityGate:
    """Gate that evaluates weight legality conditions."""

    LAYER = Layer.WEIGHT_MIZAN

    @staticmethod
    def evaluate(record: WeightRecord) -> GateResult:
        """Check weight legality (inflection + derivation_legality)."""
        if record.eligibility is WeightEligibility.NOT_ELIGIBLE:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=WeightLegalityGate.LAYER,
                reason="الوحدة غير قابلة للوزن",
                missing_condition="eligibility",
            )

        if record.inflection is None:
            return GateResult(
                verdict=GateVerdict.SUSPEND,
                layer=WeightLegalityGate.LAYER,
                reason="لم يُحدَّد المبني/المعرب",
                missing_condition="inflection",
            )

        if record.derivation_legality is None:
            return GateResult(
                verdict=GateVerdict.SUSPEND,
                layer=WeightLegalityGate.LAYER,
                reason="لم تُحدَّد شرعية الاشتقاق",
                missing_condition="derivation_legality",
            )

        return GateResult(
            verdict=GateVerdict.PASS,
            layer=WeightLegalityGate.LAYER,
        )
