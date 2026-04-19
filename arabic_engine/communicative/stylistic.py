"""
Stylistic gate — evaluates stylistic closure conditions.
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import GateVerdict
from arabic_engine.core.enums_domain import Layer, CommunicativeMode
from arabic_engine.core.types_gate import GateResult

from .khabar_insha import CommunicativeResult


class StylisticGate:
    """Gate that checks whether stylistic closure conditions are met."""

    @staticmethod
    def evaluate(result: CommunicativeResult) -> GateResult:
        """Check that a communicative mode has been determined."""
        if result.mode is None:
            return GateResult(
                verdict=GateVerdict.SUSPEND,
                layer=Layer.PROPOSITION,
                reason="لم يُحدَّد النمط التواصلي (خبر/إنشاء)",
                missing_condition="communicative_mode",
            )
        return GateResult(
            verdict=GateVerdict.PASS,
            layer=Layer.PROPOSITION,
        )
