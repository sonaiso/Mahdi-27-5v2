"""
Proposition closure engine — validates Layer 6 closure.
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_judgement import Proposition


class PropositionClosureEngine:
    """Validates that a proposition is properly closed."""

    @staticmethod
    def evaluate(prop: Proposition) -> GateResult:
        if prop.closure is ClosureStatus.CLOSED and prop.relations:
            return GateResult(
                verdict=GateVerdict.PASS,
                layer=Layer.PROPOSITION,
            )
        return GateResult(
            verdict=GateVerdict.REJECT,
            layer=Layer.PROPOSITION,
            reason="القضية غير مقفلة أو فارغة",
            missing_condition="proposition_closure",
        )
