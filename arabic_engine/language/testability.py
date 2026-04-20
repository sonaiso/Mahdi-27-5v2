"""
Testability interface — makes judgements testable for truth/falsity.

Implements the testability subsystem of Lang_tr:

    TestabilityInterface ⊂ Lang_tr

Determines whether a judgement formed from categories in the container
can be evaluated for truth or falsity (خبر) or is purely performative
(إنشاء).
"""

from __future__ import annotations

from arabic_engine.core.enums_language import CognitiveCategory
from arabic_engine.core.types_language import (
    CategorySlot,
    PredicationRule,
    TestabilityResult,
)


# Categories that, when involved in predication, yield testable judgements
_TESTABLE_PREDICATE_CATEGORIES: frozenset[CognitiveCategory] = frozenset({
    CognitiveCategory.QUALITY,
    CognitiveCategory.EVENT,
    CognitiveCategory.RELATION,
    CognitiveCategory.ENTITY,
    CognitiveCategory.TEMPORALITY,
    CognitiveCategory.SPATIALITY,
})

# Categories that mark performative (إنشاء) rather than informative (خبر) usage
_PERFORMATIVE_INDICATORS: frozenset[CognitiveCategory] = frozenset({
    CognitiveCategory.CONDITION,  # conditional constructions can be non-truth-evaluable
})


class TestabilityInterface:
    """Evaluates whether a judgement is testable for truth/falsity.

    A judgement is testable (خبر) when:
    - Its predicate comes from a testable category
    - Its subject is well-formed
    - No purely performative category overrides

    A judgement is performative-only (إنشاء) when it cannot be true or false.
    """

    @staticmethod
    def evaluate_predication(rule: PredicationRule) -> TestabilityResult:
        """Evaluate testability of a predication rule.

        Returns a TestabilityResult indicating whether the judgement
        resulting from this predication can be tested for truth/falsity.
        """
        if not rule.is_permitted:
            return TestabilityResult(
                is_testable=False,
                testability_reason="الإسناد غير مسموح — لا يمكن اختباره",
                truth_evaluable=False,
                performative_only=False,
            )

        if rule.predicate_category in _PERFORMATIVE_INDICATORS:
            return TestabilityResult(
                is_testable=False,
                testability_reason=(
                    f"{rule.predicate_category.name} "
                    "مقولة إنشائية — لا يُختبر بالصدق والكذب"
                ),
                truth_evaluable=False,
                performative_only=True,
            )

        if rule.predicate_category in _TESTABLE_PREDICATE_CATEGORIES:
            return TestabilityResult(
                is_testable=True,
                testability_reason="الحكم قابل للاختبار بالصدق والكذب",
                truth_evaluable=True,
                performative_only=False,
            )

        return TestabilityResult(
            is_testable=False,
            testability_reason=(
                f"{rule.predicate_category.name} "
                "لا يصلح لتقييم الصدق والكذب"
            ),
            truth_evaluable=False,
            performative_only=False,
        )

    @staticmethod
    def evaluate_slots(
        slots: list[CategorySlot],
    ) -> TestabilityResult:
        """Evaluate testability of a set of category slots.

        A container is testable if it contains at least one entity-like
        subject and one testable predicate category.
        """
        has_subject = any(
            s.category in {CognitiveCategory.ENTITY, CognitiveCategory.REFERENCE}
            for s in slots
        )
        has_testable_pred = any(
            s.category in _TESTABLE_PREDICATE_CATEGORIES
            for s in slots
        )

        if has_subject and has_testable_pred:
            return TestabilityResult(
                is_testable=True,
                testability_reason="الوعاء يحتوي مسندًا إليه ومسندًا قابلاً للاختبار",
                truth_evaluable=True,
                performative_only=False,
            )

        reason_parts: list[str] = []
        if not has_subject:
            reason_parts.append("لا يوجد مسند إليه")
        if not has_testable_pred:
            reason_parts.append("لا يوجد مسند قابل للاختبار")

        return TestabilityResult(
            is_testable=False,
            testability_reason=" — ".join(reason_parts),
            truth_evaluable=False,
            performative_only=False,
        )
