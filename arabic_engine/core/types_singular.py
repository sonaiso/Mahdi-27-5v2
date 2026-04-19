"""
Singular-layer data types for the Arabic Cognitive Fractal Engine.

Defines data structures for layers 0-3: Pre-U0, Perceptual, Informational, Conceptual.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .enums_gate import ClosureStatus
from .enums_singular import (
    Definiteness,
    DerivationKind,
    Gender,
    StabilityKind,
    WordCategory,
)


# ---------------------------------------------------------------------------
# Layer 0: Pre-U0 Admissibility
# ---------------------------------------------------------------------------

@dataclass
class PreU0:
    """Layer 0 — presence, distinguishability, initial admissibility."""

    codepoint: int = 0
    char: str = ""
    is_present: bool = False
    is_distinguishable: bool = False
    is_admissible: bool = False
    closure: ClosureStatus = ClosureStatus.OPEN


# ---------------------------------------------------------------------------
# Layer 1: Singular Perceptual Closure
# ---------------------------------------------------------------------------

@dataclass
class SingularPerceptual:
    """Layer 1 — sensory trace, initial stability/transformability."""

    sensory_trace: str = ""
    stability: Optional[StabilityKind] = None
    closure: ClosureStatus = ClosureStatus.OPEN


# ---------------------------------------------------------------------------
# Layer 2: Singular Informational Closure
# ---------------------------------------------------------------------------

@dataclass
class SingularInformational:
    """Layer 2 — prior-knowledge binding, causality, temporality, countability."""

    prior_knowledge_bound: bool = False
    causality_potential: bool = False
    effect_potential: bool = False
    agency_potential: bool = False
    temporal_potential: bool = False
    spatial_potential: bool = False
    countability_potential: bool = False
    closure: ClosureStatus = ClosureStatus.OPEN


# ---------------------------------------------------------------------------
# Layer 3: Singular Conceptual Closure
# ---------------------------------------------------------------------------

@dataclass
class SingularConceptual:
    """Layer 3 — definiteness, gender, word category, derivation, etc."""

    definiteness: Optional[Definiteness] = None
    gender: Optional[Gender] = None
    word_category: Optional[WordCategory] = None
    derivation: Optional[DerivationKind] = None
    stability_conceptual: Optional[StabilityKind] = None
    weight_system_eligible: bool = False
    closure: ClosureStatus = ClosureStatus.OPEN


# ---------------------------------------------------------------------------
# Singular unit — aggregates layers 0-3
# ---------------------------------------------------------------------------

@dataclass
class SingularUnit:
    """A singular linguistic unit aggregating layers 0 through 3."""

    pre_u0: PreU0 = field(default_factory=PreU0)
    perceptual: SingularPerceptual = field(default_factory=SingularPerceptual)
    informational: SingularInformational = field(default_factory=SingularInformational)
    conceptual: SingularConceptual = field(default_factory=SingularConceptual)

    @property
    def singular_closed(self) -> bool:
        """True only when all three singular sub-layers are closed."""
        return (
            self.pre_u0.closure is ClosureStatus.CLOSED
            and self.perceptual.closure is ClosureStatus.CLOSED
            and self.informational.closure is ClosureStatus.CLOSED
            and self.conceptual.closure is ClosureStatus.CLOSED
        )
