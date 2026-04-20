"""
Category registry — maps cognitive categories to linguistic positions.

The twelve categories (𝒦) are housed in their canonical Arabic grammatical
positions.  This module provides the authoritative mapping and validates
that every category has exactly one proper home.

    𝒦 = {Entity, Quality, Event, Relation, Cause, Condition,
          Negation, Quantity, Limitation, Reference, Temporality, Spatiality}
"""

from __future__ import annotations

from arabic_engine.core.enums_language import (
    CognitiveCategory,
    ContainerValidityStatus,
    LinguisticPosition,
)
from arabic_engine.core.types_language import CategorySlot


# ---------------------------------------------------------------------------
# Canonical category → position map
# ---------------------------------------------------------------------------

_CANONICAL_MAP: dict[CognitiveCategory, tuple[LinguisticPosition, str, str]] = {
    CognitiveCategory.ENTITY: (
        LinguisticPosition.ISM,
        "الذات",
        "Entity",
    ),
    CognitiveCategory.QUALITY: (
        LinguisticPosition.NA3T_SIFA_HAL,
        "الصفة",
        "Quality",
    ),
    CognitiveCategory.EVENT: (
        LinguisticPosition.FI3L_MASDAR,
        "الحدث",
        "Event",
    ),
    CognitiveCategory.RELATION: (
        LinguisticPosition.HARF_ADAWAT_NISAB,
        "العلاقة",
        "Relation",
    ),
    CognitiveCategory.CAUSE: (
        LinguisticPosition.ADAWAT_SABAB,
        "السببية",
        "Cause",
    ),
    CognitiveCategory.CONDITION: (
        LinguisticPosition.ADAWAT_SHART,
        "الشرطية",
        "Condition",
    ),
    CognitiveCategory.NEGATION: (
        LinguisticPosition.ADAWAT_NAFY,
        "النفي",
        "Negation",
    ),
    CognitiveCategory.QUANTITY: (
        LinguisticPosition.ADAWAT_ADAD,
        "العدد/الكم",
        "Quantity",
    ),
    CognitiveCategory.LIMITATION: (
        LinguisticPosition.ADAWAT_TAQYID,
        "التقييد",
        "Limitation",
    ),
    CognitiveCategory.REFERENCE: (
        LinguisticPosition.DAMIR_ISHARA_MAWSUL,
        "الإحالة",
        "Reference",
    ),
    CognitiveCategory.TEMPORALITY: (
        LinguisticPosition.ADAWAT_ZAMAN,
        "الزمان",
        "Temporality",
    ),
    CognitiveCategory.SPATIALITY: (
        LinguisticPosition.ADAWAT_MAKAN,
        "المكان",
        "Spatiality",
    ),
}


class CategoryRegistry:
    """Authoritative registry mapping cognitive categories to linguistic positions.

    Provides:
    - Full slot generation for all 12 categories
    - Lookup by category or position
    - Validation that the mapping is comprehensive (جامع)
    """

    @staticmethod
    def build_all_slots() -> list[CategorySlot]:
        """Build all 12 canonical category slots.

        Returns a list of CategorySlot instances, one per cognitive category,
        each mapped to its proper linguistic position.
        """
        slots: list[CategorySlot] = []
        for cat, (pos, label_ar, label_en) in _CANONICAL_MAP.items():
            slots.append(CategorySlot(
                category=cat,
                position=pos,
                validity=ContainerValidityStatus.VALID,
                label_ar=label_ar,
                label_en=label_en,
            ))
        return slots

    @staticmethod
    def get_position(category: CognitiveCategory) -> LinguisticPosition:
        """Return the canonical linguistic position for a category."""
        return _CANONICAL_MAP[category][0]

    @staticmethod
    def get_category_for_position(
        position: LinguisticPosition,
    ) -> CognitiveCategory | None:
        """Return the cognitive category housed at a linguistic position, or None."""
        for cat, (pos, _, _) in _CANONICAL_MAP.items():
            if pos is position:
                return cat
        return None

    @staticmethod
    def is_comprehensive(slots: list[CategorySlot]) -> bool:
        """Check whether a list of slots covers all 12 categories (جامع)."""
        present = {s.category for s in slots}
        return present == set(CognitiveCategory)

    @staticmethod
    def missing_categories(slots: list[CategorySlot]) -> set[CognitiveCategory]:
        """Return the set of categories missing from the given slots."""
        present = {s.category for s in slots}
        return set(CognitiveCategory) - present

    @staticmethod
    def canonical_map_size() -> int:
        """Return the number of entries in the canonical map (should be 12)."""
        return len(_CANONICAL_MAP)
