"""
Perception gate — Layer 1: Singular Perceptual Closure.

Validates that a sensory trace exists and an initial stability/transformability
distinction has been made.
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_singular import SingularPerceptual


class PerceptionGate:
    """Gate that evaluates Layer 1 (Singular Perceptual) closure."""

    LAYER = Layer.SINGULAR_PERCEPTUAL

    @staticmethod
    def evaluate(perceptual: SingularPerceptual) -> GateResult:
        """Check whether the perceptual layer is ready to close."""
        if not perceptual.sensory_trace:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=PerceptionGate.LAYER,
                reason="لا يوجد أثر حسي",
                missing_condition="sensory_trace",
            )

        if perceptual.stability is None:
            return GateResult(
                verdict=GateVerdict.SUSPEND,
                layer=PerceptionGate.LAYER,
                reason="لم يُحدَّد الثبات/التحول",
                missing_condition="stability",
            )

        return GateResult(
            verdict=GateVerdict.PASS,
            layer=PerceptionGate.LAYER,
        )

    @staticmethod
    def close(perceptual: SingularPerceptual) -> SingularPerceptual:
        """Attempt to close the perceptual layer. Mutates in place."""
        result = PerceptionGate.evaluate(perceptual)
        if result.passed:
            perceptual.closure = ClosureStatus.CLOSED
        elif result.verdict is GateVerdict.SUSPEND:
            perceptual.closure = ClosureStatus.SUSPENDED
        else:
            perceptual.closure = ClosureStatus.BLOCKED
        return perceptual
