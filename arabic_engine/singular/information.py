"""
Information gate — Layer 2: Singular Informational Closure.

Validates that prior-knowledge binding and at least one potentiality
dimension have been resolved.
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_singular import SingularInformational


class InformationGate:
    """Gate that evaluates Layer 2 (Singular Informational) closure."""

    LAYER = Layer.SINGULAR_INFORMATIONAL

    @staticmethod
    def evaluate(info: SingularInformational) -> GateResult:
        """Check whether the informational layer is ready to close."""
        if not info.prior_knowledge_bound:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=InformationGate.LAYER,
                reason="لم تُربط المعلومات السابقة",
                missing_condition="prior_knowledge_bound",
            )

        # At least one potentiality dimension must be set
        potentials = [
            info.causality_potential,
            info.effect_potential,
            info.agency_potential,
            info.temporal_potential,
            info.spatial_potential,
            info.countability_potential,
        ]
        if not any(potentials):
            return GateResult(
                verdict=GateVerdict.SUSPEND,
                layer=InformationGate.LAYER,
                reason="لا توجد أي إمكانية معلوماتية محددة",
                missing_condition="at_least_one_potential",
            )

        return GateResult(
            verdict=GateVerdict.PASS,
            layer=InformationGate.LAYER,
        )

    @staticmethod
    def close(info: SingularInformational) -> SingularInformational:
        """Attempt to close the informational layer. Mutates in place."""
        result = InformationGate.evaluate(info)
        if result.passed:
            info.closure = ClosureStatus.CLOSED
        elif result.verdict is GateVerdict.SUSPEND:
            info.closure = ClosureStatus.SUSPENDED
        else:
            info.closure = ClosureStatus.BLOCKED
        return info
