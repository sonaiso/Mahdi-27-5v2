"""
Compositional data types for the Arabic Cognitive Fractal Engine.

Defines data structures for Layer 5: Compositional Roles.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .enums_gate import ClosureStatus
from .enums_domain import RelationKind, RoleTag
from .types_weight import WeightedUnit


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
