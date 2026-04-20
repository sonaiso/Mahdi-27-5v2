"""
Predication engine — enables judgement formation from categories.

Implements the predication rules subsystem of Lang_tr:

    PredicationRules ⊂ Lang_tr

Predication requires a subject (مسند إليه) from entity-like categories
and a predicate (مسند) from event/quality/relation categories.
"""

from __future__ import annotations

from arabic_engine.core.enums_language import CognitiveCategory
from arabic_engine.core.types_language import PredicationRule

# ---------------------------------------------------------------------------
# Categories eligible for subject and predicate roles
# ---------------------------------------------------------------------------

_SUBJECT_CATEGORIES: frozenset[CognitiveCategory] = frozenset({
    CognitiveCategory.ENTITY,
    CognitiveCategory.REFERENCE,  # pronouns can be subjects
})

_PREDICATE_CATEGORIES: frozenset[CognitiveCategory] = frozenset({
    CognitiveCategory.QUALITY,
    CognitiveCategory.EVENT,
    CognitiveCategory.RELATION,
    CognitiveCategory.ENTITY,      # nominal predicate (الجملة الاسمية)
    CognitiveCategory.TEMPORALITY,
    CognitiveCategory.SPATIALITY,
})


class PredicationEngine:
    """Manages predication rules for the transcendental container.

    Determines which category combinations are valid for predication
    (الإسناد) — the assignment of a predicate (مسند) to a subject
    (مسند إليه).
    """

    @staticmethod
    def is_valid_subject(category: CognitiveCategory) -> bool:
        """Check whether a category can serve as a predication subject."""
        return category in _SUBJECT_CATEGORIES

    @staticmethod
    def is_valid_predicate(category: CognitiveCategory) -> bool:
        """Check whether a category can serve as a predicate."""
        return category in _PREDICATE_CATEGORIES

    @staticmethod
    def check_predication(
        subject_category: CognitiveCategory,
        predicate_category: CognitiveCategory,
    ) -> PredicationRule:
        """Check whether a subject–predicate combination is valid.

        Returns a PredicationRule with is_permitted set accordingly.
        """
        if not PredicationEngine.is_valid_subject(subject_category):
            return PredicationRule(
                subject_category=subject_category,
                predicate_category=predicate_category,
                is_permitted=False,
                rule_description=(
                    f"{subject_category.name} لا يصلح مسندًا إليه"
                ),
            )

        if not PredicationEngine.is_valid_predicate(predicate_category):
            return PredicationRule(
                subject_category=subject_category,
                predicate_category=predicate_category,
                is_permitted=False,
                rule_description=(
                    f"{predicate_category.name} لا يصلح مسندًا"
                ),
            )

        return PredicationRule(
            subject_category=subject_category,
            predicate_category=predicate_category,
            is_permitted=True,
            rule_description=(
                f"إسناد صحيح: {subject_category.name} ← {predicate_category.name}"
            ),
        )

    @staticmethod
    def build_all_rules() -> list[PredicationRule]:
        """Generate predication rules for all valid subject–predicate pairs."""
        rules: list[PredicationRule] = []
        for subj in _SUBJECT_CATEGORIES:
            for pred in _PREDICATE_CATEGORIES:
                rules.append(PredicationEngine.check_predication(subj, pred))
        return rules
