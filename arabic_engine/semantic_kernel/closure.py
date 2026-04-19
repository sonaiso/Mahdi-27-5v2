"""
Semantic kernel closure engine — orchestrates the closure pipeline
for the semantic transfer layer.

Follows the same Gate → Closure → Trace pattern used in all other layers.

Gates:
    1. Compatibility gate — root and pattern must be compatible
    2. Completeness gate — Complete_min(R,P,F) must hold
    3. Economy gate — cost must be finite
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.enums_semantic import CompatibilityStatus
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_semantic import SemanticTransferResult

from .compatibility import CompatibilityChecker
from .economy import EconomyOptimizer


class SemanticKernelClosureEngine:
    """Orchestrates closure for a SemanticTransferResult.

    Runs three sub-gates in sequence:
    1. Compatibility — root–pattern must not be INCOMPATIBLE
    2. Completeness — Complete_min(R,P,F)
    3. Economy — cost must be finite and reasonable
    """

    LAYER = Layer.WEIGHT_MIZAN  # semantic kernel is part of Layer 4

    @staticmethod
    def close(result: SemanticTransferResult) -> list[GateResult]:
        """Run the semantic kernel closure pipeline.

        Returns a list of GateResults for each sub-gate attempted.
        Sets result.closure based on the outcome.
        """
        results: list[GateResult] = []

        # Gate 1: Compatibility
        compat = CompatibilityChecker.check_root_pattern(
            result.root_kernel, result.pattern_transform
        )
        if compat is CompatibilityStatus.INCOMPATIBLE:
            r = GateResult(
                verdict=GateVerdict.REJECT,
                layer=SemanticKernelClosureEngine.LAYER,
                reason="الجذر والوزن غير متوافقين — لا يجوز نقل الحمولة",
                missing_condition="root_pattern_compatibility",
            )
            results.append(r)
            result.closure = ClosureStatus.BLOCKED
            return results

        results.append(GateResult(
            verdict=GateVerdict.PASS,
            layer=SemanticKernelClosureEngine.LAYER,
            reason="التوافق بين الجذر والوزن — ناجح",
        ))

        # Gate 2: Completeness
        complete = CompatibilityChecker.check_complete_min(
            result.root_kernel,
            result.pattern_transform,
            result.form_profile,
        )
        if not complete:
            r = GateResult(
                verdict=GateVerdict.SUSPEND,
                layer=SemanticKernelClosureEngine.LAYER,
                reason="لم يتحقق شرط الحد الأدنى المكتمل",
                missing_condition="complete_min",
            )
            results.append(r)
            result.closure = ClosureStatus.SUSPENDED
            return results

        results.append(GateResult(
            verdict=GateVerdict.PASS,
            layer=SemanticKernelClosureEngine.LAYER,
            reason="الحد الأدنى المكتمل — متحقق",
        ))

        # Gate 3: Economy
        cost = EconomyOptimizer.compute_cost(result)
        if not _is_finite(cost.total):
            r = GateResult(
                verdict=GateVerdict.REJECT,
                layer=SemanticKernelClosureEngine.LAYER,
                reason="الكلفة غير منتهية — رفض",
                missing_condition="finite_cost",
            )
            results.append(r)
            result.closure = ClosureStatus.BLOCKED
            return results

        results.append(GateResult(
            verdict=GateVerdict.PASS,
            layer=SemanticKernelClosureEngine.LAYER,
            reason="الاقتصاد — متحقق",
        ))

        # All gates passed
        result.closure = ClosureStatus.CLOSED
        return results


def _is_finite(value: float) -> bool:
    """Check that a value is finite (not NaN or infinite)."""
    import math
    return math.isfinite(value)
