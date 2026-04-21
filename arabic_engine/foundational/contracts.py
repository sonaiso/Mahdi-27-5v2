"""
Foundational invariant contracts for additive Layer 1/2.
"""

from __future__ import annotations

from .models import FoundationalUnit


class FoundationalInvariantContract:
    """Contract-level checks for foundational v1."""

    LETTER_REQUIRED_ESSENTIAL = {"is_letter", "has_base_shape"}
    DIACRITIC_REQUIRED_ESSENTIAL = {"is_diacritic", "is_mark"}

    @staticmethod
    def symbolic_identity_invariant(unit: FoundationalUnit) -> bool:
        """Each available token must satisfy symbol/codepoint identity."""
        tokens = [t for t in (unit.letter, unit.diacritic) if t is not None]
        return all(len(t.symbol) == 1 and ord(t.symbol) == t.codepoint for t in tokens)

    @staticmethod
    def normalization_invariant(unit: FoundationalUnit) -> bool:
        """Each available token must remain normalized in its configured form."""
        tokens = [t for t in (unit.letter, unit.diacritic) if t is not None]
        return all(t.symbol == t.normalized_symbol for t in tokens)

    @staticmethod
    def ontological_property_completeness_invariant(unit: FoundationalUnit) -> bool:
        """Required essential keys must exist for provided token kinds."""
        profile = unit.ontology
        if unit.letter is not None and not FoundationalInvariantContract.LETTER_REQUIRED_ESSENTIAL.issubset(
            set(profile.letter_essential.keys())
        ):
            return False
        if unit.diacritic is not None and not FoundationalInvariantContract.DIACRITIC_REQUIRED_ESSENTIAL.issubset(
            set(profile.diacritic_essential.keys())
        ):
            return False
        return True

    @staticmethod
    def essential_contextual_separation_invariant(unit: FoundationalUnit) -> bool:
        """No essential key may appear in contextual scope."""
        profile = unit.ontology
        essential_keys = set(profile.letter_essential) | set(profile.diacritic_essential)
        return essential_keys.isdisjoint(set(profile.contextual))

