"""
Language closure engine — gate and closure for the language layer.

Follows the Gate-Closure-Trace pattern used by every other layer:

    Gate.evaluate() → GateResult → ClosureEngine.close() → TraceEvent

The language layer closes when:
  1. The container is comprehensive (جامع) — all 12 categories present
  2. The container is preventive (مانع) — no rank confusion
  3. All five container functions are active
  4. At least one testability result is positive
  5. The feedback loop has been applied
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_language import TranscendentalContainer
from arabic_engine.core.enums_language import CognitiveCategory, ContainerFunction


class LanguageGate:
    """Gate check for the language layer."""

    @staticmethod
    def evaluate(container: TranscendentalContainer) -> GateResult:
        """Evaluate whether the transcendental container can be closed.

        Checks:
        1. Comprehensive — all 12 categories present
        2. Preventive — no constraint violations
        3. All five functions active
        4. Testability — at least one positive testability result
        5. Feedback — the feedback loop has been applied
        """
        # Check 1: comprehensive
        if not container.is_comprehensive:
            present = {s.category for s in container.category_slots}
            missing = len(CognitiveCategory) - len(present)
            return GateResult(
                verdict=GateVerdict.SUSPEND,
                layer=Layer.LANGUAGE,
                reason=f"الوعاء غير جامع — ينقصه {missing} مقولة",
                missing_condition="is_comprehensive",
            )

        # Check 2: preventive
        if not container.is_preventive:
            violations = container.constraint_violation_count
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.LANGUAGE,
                reason=f"خلط في الرتب — {violations} انتهاك",
                missing_condition="is_preventive",
            )

        # Check 3: all five functions
        if len(container.active_functions) < len(ContainerFunction):
            missing_fns = set(ContainerFunction) - container.active_functions
            names = ", ".join(f.name for f in missing_fns)
            return GateResult(
                verdict=GateVerdict.SUSPEND,
                layer=Layer.LANGUAGE,
                reason=f"وظائف الوعاء ناقصة — ينقص: {names}",
                missing_condition="all_functions_active",
            )

        # Check 4: testability
        if not any(t.is_testable for t in container.testability_results):
            return GateResult(
                verdict=GateVerdict.SUSPEND,
                layer=Layer.LANGUAGE,
                reason="لا يوجد حكم قابل للاختبار في الوعاء",
                missing_condition="testability",
            )

        # Check 5: feedback
        if container.feedback is None:
            return GateResult(
                verdict=GateVerdict.SUSPEND,
                layer=Layer.LANGUAGE,
                reason="لم يُطبَّق الارتجاع اللغوي",
                missing_condition="feedback_applied",
            )

        return GateResult(
            verdict=GateVerdict.PASS,
            layer=Layer.LANGUAGE,
        )


class LanguageClosureEngine:
    """Closure engine for the language layer.

    Evaluates the gate and sets the container's closure status.
    """

    @staticmethod
    def close(container: TranscendentalContainer) -> list[GateResult]:
        """Attempt to close the language layer.

        Returns a list of GateResult instances (one from the gate check).
        Sets the container's closure status based on the verdict.
        """
        result = LanguageGate.evaluate(container)

        if result.verdict is GateVerdict.PASS:
            container.closure = ClosureStatus.CLOSED
        elif result.verdict is GateVerdict.REJECT:
            container.closure = ClosureStatus.BLOCKED
        else:
            container.closure = ClosureStatus.SUSPENDED

        return [result]
