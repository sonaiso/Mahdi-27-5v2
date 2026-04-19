"""
Singular closure engine — orchestrates layers 0-3 in strict order.

Enforces the anti-jump invariant: no layer may close before its predecessor.
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_singular import PreU0, SingularUnit

from .perception import PerceptionGate
from .information import InformationGate
from .concept import ConceptGate


class SingularClosureEngine:
    """Orchestrates the full singular closure pipeline (Layers 0-3)."""

    @staticmethod
    def evaluate_pre_u0(pre: PreU0) -> GateResult:
        """Evaluate Layer 0 (Pre-U0 Admissibility)."""
        if not pre.is_present:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.PRE_U0_ADMISSIBILITY,
                reason="الوحدة غير موجودة",
                missing_condition="is_present",
            )
        if not pre.is_distinguishable:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.PRE_U0_ADMISSIBILITY,
                reason="الوحدة غير قابلة للتمييز",
                missing_condition="is_distinguishable",
            )
        if not pre.is_admissible:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.PRE_U0_ADMISSIBILITY,
                reason="الوحدة غير مقبولة أوليًا",
                missing_condition="is_admissible",
            )
        return GateResult(
            verdict=GateVerdict.PASS,
            layer=Layer.PRE_U0_ADMISSIBILITY,
        )

    @staticmethod
    def close_pre_u0(pre: PreU0) -> PreU0:
        """Attempt to close Layer 0."""
        result = SingularClosureEngine.evaluate_pre_u0(pre)
        pre.closure = (
            ClosureStatus.CLOSED if result.passed else ClosureStatus.BLOCKED
        )
        return pre

    @staticmethod
    def close_all(unit: SingularUnit) -> list[GateResult]:
        """Run the full singular pipeline in strict order.

        Returns a list of GateResults, one per layer attempted.
        Stops at the first non-PASS layer.
        """
        results: list[GateResult] = []

        # Layer 0
        r0 = SingularClosureEngine.evaluate_pre_u0(unit.pre_u0)
        results.append(r0)
        if not r0.passed:
            unit.pre_u0.closure = ClosureStatus.BLOCKED
            return results
        unit.pre_u0.closure = ClosureStatus.CLOSED

        # Layer 1
        r1 = PerceptionGate.evaluate(unit.perceptual)
        results.append(r1)
        if not r1.passed:
            unit.perceptual.closure = (
                ClosureStatus.SUSPENDED
                if r1.verdict is GateVerdict.SUSPEND
                else ClosureStatus.BLOCKED
            )
            return results
        unit.perceptual.closure = ClosureStatus.CLOSED

        # Layer 2
        r2 = InformationGate.evaluate(unit.informational)
        results.append(r2)
        if not r2.passed:
            unit.informational.closure = (
                ClosureStatus.SUSPENDED
                if r2.verdict is GateVerdict.SUSPEND
                else ClosureStatus.BLOCKED
            )
            return results
        unit.informational.closure = ClosureStatus.CLOSED

        # Layer 3
        r3 = ConceptGate.evaluate(unit.conceptual)
        results.append(r3)
        if not r3.passed:
            unit.conceptual.closure = (
                ClosureStatus.SUSPENDED
                if r3.verdict is GateVerdict.SUSPEND
                else ClosureStatus.BLOCKED
            )
            return results
        unit.conceptual.closure = ClosureStatus.CLOSED

        return results
