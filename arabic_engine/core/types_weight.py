"""
Weight / Mizan data types for the Arabic Cognitive Fractal Engine.

Defines data structures for Layer 4: Weight/Mizan Fractal.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .enums_gate import ClosureStatus
from .enums_singular import DerivationKind
from .enums_weight import (
    DescriptivePotential,
    InflectionKind,
    SpatialPotential,
    TemporalPotential,
    WeightEligibility,
)
from .types_semantic import RootSemanticKernel, SemanticTransferResult
from .types_singular import SingularUnit


# ---------------------------------------------------------------------------
# Layer 4: Weight / Mizan Fractal
# ---------------------------------------------------------------------------

@dataclass
class WeightRecord:
    """Layer 4 — weight ontology, legality, transition, trace."""

    # Weight ontology
    eligibility: WeightEligibility = WeightEligibility.NOT_ELIGIBLE
    pattern: str = ""          # e.g. "فَعَلَ", "إفعال"
    root: str = ""             # e.g. "ك ت ب"

    # Weight legality
    inflection: Optional[InflectionKind] = None
    derivation_legality: Optional[DerivationKind] = None
    accepts_conjugation: bool = False

    # Weight transition
    temporal: TemporalPotential = TemporalPotential.NONE
    spatial: SpatialPotential = SpatialPotential.NO_SPATIAL
    descriptive: DescriptivePotential = DescriptivePotential.NONE

    # Weight trace — structural eligibility after weight analysis
    noun_eligible: bool = False
    verb_eligible: bool = False
    particle_eligible: bool = False

    # Semantic kernel (optional — backward compatible)
    semantic_kernel: Optional[RootSemanticKernel] = None
    semantic_transfer: Optional[SemanticTransferResult] = None

    # Closure
    closure: ClosureStatus = ClosureStatus.OPEN

    @property
    def weight_closed(self) -> bool:
        return self.closure is ClosureStatus.CLOSED


# ---------------------------------------------------------------------------
# Weighted unit — singular + weight
# ---------------------------------------------------------------------------

@dataclass
class WeightedUnit:
    """A singular unit that has passed through weight/mizan closure."""

    singular: SingularUnit = field(default_factory=SingularUnit)
    weight: WeightRecord = field(default_factory=WeightRecord)

    @property
    def fully_closed(self) -> bool:
        """True when both singular and weight closures are satisfied."""
        return self.singular.singular_closed and self.weight.weight_closed
