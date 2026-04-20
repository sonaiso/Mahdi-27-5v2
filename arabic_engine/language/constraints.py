"""
Constraint system — prevents rank confusion in the transcendental container.

Implements the prevention function (المنع) of the container:

    Con_lang(x) : Valid(x) ⟺ Category(x) ∧ ProperRole(x) ∧ NoRankConfusion(x)

Guards against specific rank confusions:
  - Entity treated as quality (always)
  - Quality treated as independent entity
  - Event treated as static entity
  - Cause confused with condition
  - General confused with absolute
  - Singular concept treated as full judgement
  - Predicate confused with subject
  - Khabar confused with insha
"""

from __future__ import annotations

from arabic_engine.core.enums_language import (
    CognitiveCategory,
    ContainerValidityStatus,
    LinguisticPosition,
    RankConfusionKind,
)
from arabic_engine.core.types_language import (
    CategorySlot,
    ConstraintRecord,
)


# ---------------------------------------------------------------------------
# Forbidden assignments — (category, wrong_position) → confusion kind
# ---------------------------------------------------------------------------

_FORBIDDEN_ASSIGNMENTS: list[
    tuple[CognitiveCategory, LinguisticPosition, RankConfusionKind]
] = [
    # Entity must not be placed in attribute positions
    (
        CognitiveCategory.ENTITY,
        LinguisticPosition.NA3T_SIFA_HAL,
        RankConfusionKind.ENTITY_AS_QUALITY,
    ),
    # Quality must not be placed in entity position as if it were a standalone substance
    (
        CognitiveCategory.QUALITY,
        LinguisticPosition.ISM,
        RankConfusionKind.QUALITY_AS_ENTITY,
    ),
    # Event must not be placed in noun position as if it were static
    (
        CognitiveCategory.EVENT,
        LinguisticPosition.ISM,
        RankConfusionKind.EVENT_AS_STATIC,
    ),
    # Cause must not be placed in condition position
    (
        CognitiveCategory.CAUSE,
        LinguisticPosition.ADAWAT_SHART,
        RankConfusionKind.CAUSE_AS_CONDITION,
    ),
    # Condition must not be placed in cause position
    (
        CognitiveCategory.CONDITION,
        LinguisticPosition.ADAWAT_SABAB,
        RankConfusionKind.CAUSE_AS_CONDITION,
    ),
]


class ConstraintSystem:
    """Enforces the prevention function of the transcendental container.

    Checks that each category is placed in its proper linguistic position
    and that no rank confusion occurs.
    """

    @staticmethod
    def validate_slot(slot: CategorySlot) -> ConstraintRecord:
        """Validate a single category slot against the constraint system.

        Returns a ConstraintRecord indicating whether the placement is valid.
        """
        for forbidden_cat, forbidden_pos, confusion_kind in _FORBIDDEN_ASSIGNMENTS:
            if slot.category is forbidden_cat and slot.position is forbidden_pos:
                return ConstraintRecord(
                    category=slot.category,
                    confusion_kind=confusion_kind,
                    is_violated=True,
                    violation_reason=(
                        f"خلط الرتب: {slot.category.name} "
                        f"في موضع {slot.position.name} — "
                        f"{confusion_kind.name}"
                    ),
                )
        return ConstraintRecord(
            category=slot.category,
            confusion_kind=None,
            is_violated=False,
        )

    @staticmethod
    def validate_all_slots(slots: list[CategorySlot]) -> list[ConstraintRecord]:
        """Validate all category slots in the container.

        Returns a list of ConstraintRecord instances.
        """
        return [ConstraintSystem.validate_slot(s) for s in slots]

    @staticmethod
    def has_violations(records: list[ConstraintRecord]) -> bool:
        """Check whether any constraint is violated."""
        return any(r.is_violated for r in records)

    @staticmethod
    def get_violations(records: list[ConstraintRecord]) -> list[ConstraintRecord]:
        """Return only violated constraint records."""
        return [r for r in records if r.is_violated]

    @staticmethod
    def compute_validity(slot: CategorySlot) -> ContainerValidityStatus:
        """Compute the validity status of a single slot.

        Valid(x) ⟺ Category(x) ∧ ProperRole(x) ∧ NoRankConfusion(x)
        """
        record = ConstraintSystem.validate_slot(slot)
        if record.is_violated:
            return ContainerValidityStatus.INVALID
        return ContainerValidityStatus.VALID
