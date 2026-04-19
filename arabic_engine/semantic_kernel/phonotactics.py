"""
Phonological compatibility checker — validates root consonants
against pattern template constraints.

Arabic has phonotactic rules that restrict which root-pattern combinations
are possible. For example:
  - Certain gutturals may block specific patterns
  - Geminated roots (doubled consonants) interact with Form II (فَعَّلَ)
  - Weak roots (roots containing و or ي) have special pattern behaviors

This module provides a phonological compatibility check that supplements
the semantic compatibility check in `compatibility.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class RootType(Enum):
    """Classification of Arabic root types by phonological structure."""

    SOUND = auto()             # صحيح — all consonants are "strong"
    HOLLOW = auto()            # أجوف — middle radical is weak (و/ي)
    DEFECTIVE = auto()         # ناقص — final radical is weak (و/ي)
    ASSIMILATED = auto()       # مثال — first radical is weak (و/ي)
    DOUBLED = auto()           # مضعّف — second and third radicals identical
    HAMZATED = auto()          # مهموز — root contains hamza (ء)
    QUADRILITERAL = auto()     # رباعي — four-consonant root


# Weak consonants in Arabic
_WEAK_CONSONANTS = frozenset("ويوىءأإآؤئ")
_WAW = frozenset("وؤ")
_YA = frozenset("يئى")
_HAMZA = frozenset("ءأإآؤئ")


def classify_root_type(root_text: str) -> RootType:
    """Classify a root by its phonological structure.

    Args:
        root_text: Root letters, optionally space-separated (e.g. "ك ت ب" or "كتب").

    Returns:
        RootType classification.
    """
    consonants = [c for c in root_text if c.strip() and c != " "]

    if len(consonants) >= 4:
        return RootType.QUADRILITERAL

    if len(consonants) < 3:
        # Fallback — treat as sound
        return RootType.SOUND

    c1, c2, c3 = consonants[0], consonants[1], consonants[2]

    # Doubled: R2 == R3
    if c2 == c3:
        return RootType.DOUBLED

    # Hamzated: any radical is hamza
    if any(c in _HAMZA for c in (c1, c2, c3)):
        return RootType.HAMZATED

    # Assimilated: first radical is weak
    if c1 in _WEAK_CONSONANTS:
        return RootType.ASSIMILATED

    # Hollow: middle radical is weak
    if c2 in _WEAK_CONSONANTS:
        return RootType.HOLLOW

    # Defective: final radical is weak
    if c3 in _WEAK_CONSONANTS:
        return RootType.DEFECTIVE

    return RootType.SOUND


@dataclass(frozen=True)
class PhonotacticResult:
    """Result of a phonotactic compatibility check."""

    compatible: bool
    root_type: RootType
    notes: str = ""


# Patterns that are phonologically restricted with certain root types.
# Key: pattern code, Value: set of incompatible root types.
_PATTERN_RESTRICTIONS: dict[str, set[RootType]] = {
    # No strict incompatibilities defined yet — Arabic phonology allows
    # most combinations with morphophonemic adjustments.  This table
    # records *dispreferred* combinations that carry extra cost.
}

# Patterns that carry extra morphological cost for certain root types.
_EXTRA_COST_MAP: dict[str, dict[RootType, float]] = {
    "فَعَّلَ": {RootType.DOUBLED: 0.15},  # Doubled root + intensive = doubled-doubled
    "اِنْفَعَلَ": {RootType.HAMZATED: 0.10},  # Hamzated root + reflexive = awkward cluster
    "اِسْتَفْعَلَ": {RootType.HOLLOW: 0.10},  # Hollow root + long prefix = weak-vowel issues
}


class PhonotacticChecker:
    """Checks phonological compatibility between root and pattern.

    Supplements semantic compatibility with phonotactic constraints.
    """

    @staticmethod
    def check(root_text: str, pattern_code: str) -> PhonotacticResult:
        """Check phonological compatibility.

        Args:
            root_text: Root letters (e.g. "ك ت ب").
            pattern_code: Pattern code (e.g. "فَعَلَ").

        Returns:
            PhonotacticResult with compatibility status and notes.
        """
        root_type = classify_root_type(root_text)

        # Check strict restrictions
        restrictions = _PATTERN_RESTRICTIONS.get(pattern_code, set())
        if root_type in restrictions:
            return PhonotacticResult(
                compatible=False,
                root_type=root_type,
                notes=f"Root type {root_type.name} is incompatible with pattern {pattern_code}",
            )

        # Check extra cost (dispreferred but not impossible)
        extra_costs = _EXTRA_COST_MAP.get(pattern_code, {})
        if root_type in extra_costs:
            cost = extra_costs[root_type]
            return PhonotacticResult(
                compatible=True,
                root_type=root_type,
                notes=(
                    f"Root type {root_type.name} with pattern {pattern_code} "
                    f"carries extra phonological cost ({cost:.2f})"
                ),
            )

        return PhonotacticResult(
            compatible=True,
            root_type=root_type,
        )

    @staticmethod
    def extra_phonological_cost(root_text: str, pattern_code: str) -> float:
        """Return extra phonological cost for the root-pattern combination.

        Returns 0.0 if no extra cost, or a positive value for dispreferred
        combinations.
        """
        root_type = classify_root_type(root_text)
        extra_costs = _EXTRA_COST_MAP.get(pattern_code, {})
        return extra_costs.get(root_type, 0.0)
