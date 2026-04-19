"""
Data types for the Arabic Cognitive Fractal Engine.

Defines the canonical data structures that flow through each layer,
from pre-U0 admissibility up through weight closure and composition.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .enums import (
    ClosureStatus,
    Definiteness,
    DerivationKind,
    DescriptivePotential,
    GateVerdict,
    Gender,
    InflectionKind,
    Layer,
    RelationKind,
    RoleTag,
    SpatialPotential,
    StabilityKind,
    TemporalPotential,
    WeightEligibility,
    WordCategory,
)
from .types_semantic import RootSemanticKernel, SemanticTransferResult

# Re-export canonical definitions from types_weight to avoid duplication
from .types_weight import WeightRecord, WeightedUnit

@dataclass(frozen=True)
class GateResult:
    """Result of a gate check at any layer."""

    verdict: GateVerdict
    layer: Layer
    reason: str = ""
    missing_condition: str = ""

    @property
    def passed(self) -> bool:
        return self.verdict is GateVerdict.PASS


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


# ---------------------------------------------------------------------------
# Layer 5: Compositional structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RoleAssignment:
    """A single role assignment within a compositional relation."""

    unit: WeightedUnit
    role: RoleTag


@dataclass
class CompositionRelation:
    """A compositional relation carrying semantics of role distribution."""

    kind: RelationKind
    roles: list[RoleAssignment] = field(default_factory=list)
    closure: ClosureStatus = ClosureStatus.OPEN
    semantics: str = ""  # human-readable role-distribution description


# ---------------------------------------------------------------------------
# Layer 6-8: Proposition, Judgement, Qiyas
# ---------------------------------------------------------------------------

@dataclass
class Proposition:
    """Layer 6 — a proposition built from closed compositional relations."""

    relations: list[CompositionRelation] = field(default_factory=list)
    closure: ClosureStatus = ClosureStatus.OPEN


@dataclass
class Judgement:
    """Layer 7 — a judgement conditioned on a closed proposition."""

    proposition: Optional[Proposition] = None
    verdict: Optional[GateVerdict] = None
    reason: str = ""
    closure: ClosureStatus = ClosureStatus.OPEN


@dataclass
class Qiyas:
    """Layer 8 — analogical reasoning built on a closed judgement."""

    judgement: Optional[Judgement] = None
    closure: ClosureStatus = ClosureStatus.OPEN
