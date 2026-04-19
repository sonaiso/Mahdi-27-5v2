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

import math
from dataclasses import dataclass, field

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.enums_semantic import CompatibilityStatus
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_semantic import SemanticTransferResult

from .compatibility import CompatibilityChecker
from .economy import EconomyOptimizer


@dataclass
class ClosureTrace:
    """Trace of a closure pipeline execution, recording which gates
    passed and which failed with their reasons."""

    gate_results: list[GateResult] = field(default_factory=list)
    final_status: ClosureStatus = ClosureStatus.OPEN

    @property
    def failed_gate(self) -> GateResult | None:
        """Return the first failing gate result, or None if all passed."""
        for r in self.gate_results:
            if not r.passed:
                return r
        return None

    @property
    def suggestions(self) -> list[str]:
        """Generate human-readable correction suggestions based on failures."""
        suggestions: list[str] = []
        failed = self.failed_gate
        if failed is None:
            return suggestions

        if failed.missing_condition == "root_pattern_compatibility":
            suggestions.append(
                "جرّب وزنًا مختلفًا — الجذر والوزن الحاليان غير متوافقين دلاليًا"
                " (Try a different pattern — root and pattern are semantically incompatible)"
            )
        elif failed.missing_condition == "complete_min":
            suggestions.append(
                "أكمل الأبعاد الناقصة في نواة الجذر أو ملف الصيغة"
                " (Complete missing dimensions in root kernel or form profile)"
            )
            suggestions.append(
                "تحقق من أن رمز الوزن غير فارغ وله 12 بُعدًا"
                " (Verify pattern code is non-empty and has 12 dimensions)"
            )
        elif failed.missing_condition == "finite_cost":
            suggestions.append(
                "الكلفة غير منتهية — تحقق من قيم المتجهات"
                " (Infinite cost — check vector values for NaN or infinity)"
            )

        return suggestions


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
        if not math.isfinite(cost.total):
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

    @staticmethod
    def close_with_trace(result: SemanticTransferResult) -> ClosureTrace:
        """Run closure and return a structured trace with suggestions.

        This is a convenience method that wraps ``close()`` and packages
        the results into a ``ClosureTrace`` with correction suggestions.
        """
        gate_results = SemanticKernelClosureEngine.close(result)
        return ClosureTrace(
            gate_results=gate_results,
            final_status=result.closure,
        )
