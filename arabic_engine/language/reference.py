"""
Reference system — binds discourse to its referents.

Implements the reference subsystem of Lang_tr:

    ReferenceSystem ⊂ Lang_tr

Reference expressions (pronouns, demonstratives, relatives) connect
discourse back to the cognitive categories they denote.
"""

from __future__ import annotations

from arabic_engine.core.enums_language import CognitiveCategory
from arabic_engine.core.types_language import ReferenceBinding


# ---------------------------------------------------------------------------
# Reference types
# ---------------------------------------------------------------------------

REFERENCE_TYPE_PRONOUN = "ضمير"           # pronoun
REFERENCE_TYPE_DEMONSTRATIVE = "إشارة"    # demonstrative
REFERENCE_TYPE_RELATIVE = "موصول"          # relative pronoun

_VALID_REFERENT_CATEGORIES: frozenset[CognitiveCategory] = frozenset({
    CognitiveCategory.ENTITY,
    CognitiveCategory.QUALITY,
    CognitiveCategory.EVENT,
    CognitiveCategory.TEMPORALITY,
    CognitiveCategory.SPATIALITY,
    CognitiveCategory.REFERENCE,  # pronouns can refer to other references
})


class ReferenceSystem:
    """Manages reference bindings in the transcendental container.

    Ensures that every referring expression (ضمير / إشارة / موصول)
    is bound to a valid referent category.
    """

    @staticmethod
    def can_refer_to(category: CognitiveCategory) -> bool:
        """Check whether a category can be a valid referent."""
        return category in _VALID_REFERENT_CATEGORIES

    @staticmethod
    def bind(
        referent_category: CognitiveCategory,
        reference_type: str,
        referent_label: str = "",
    ) -> ReferenceBinding:
        """Create a reference binding.

        If the referent category is not valid, the binding is unresolved.
        """
        is_valid = ReferenceSystem.can_refer_to(referent_category)
        return ReferenceBinding(
            referent_category=referent_category,
            reference_type=reference_type,
            is_resolved=is_valid,
            referent_label=referent_label,
        )

    @staticmethod
    def bind_pronoun(
        referent_category: CognitiveCategory,
        referent_label: str = "",
    ) -> ReferenceBinding:
        """Create a pronoun reference binding."""
        return ReferenceSystem.bind(
            referent_category=referent_category,
            reference_type=REFERENCE_TYPE_PRONOUN,
            referent_label=referent_label,
        )

    @staticmethod
    def bind_demonstrative(
        referent_category: CognitiveCategory,
        referent_label: str = "",
    ) -> ReferenceBinding:
        """Create a demonstrative reference binding."""
        return ReferenceSystem.bind(
            referent_category=referent_category,
            reference_type=REFERENCE_TYPE_DEMONSTRATIVE,
            referent_label=referent_label,
        )

    @staticmethod
    def bind_relative(
        referent_category: CognitiveCategory,
        referent_label: str = "",
    ) -> ReferenceBinding:
        """Create a relative-pronoun reference binding."""
        return ReferenceSystem.bind(
            referent_category=referent_category,
            reference_type=REFERENCE_TYPE_RELATIVE,
            referent_label=referent_label,
        )

    @staticmethod
    def all_resolved(bindings: list[ReferenceBinding]) -> bool:
        """Check whether all reference bindings are resolved."""
        return all(b.is_resolved for b in bindings)

    @staticmethod
    def unresolved_bindings(
        bindings: list[ReferenceBinding],
    ) -> list[ReferenceBinding]:
        """Return only the unresolved reference bindings."""
        return [b for b in bindings if not b.is_resolved]
