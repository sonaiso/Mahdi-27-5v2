"""
Compositional data types for the Arabic Cognitive Fractal Engine.

Defines data structures for Layer 5: Compositional Roles.

Semantic kernel integration: Role assignments can access semantic transfer
results from their underlying weighted units, enabling semantically-informed
composition decisions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .enums_gate import ClosureStatus
from .enums_domain import RelationKind, RoleTag
from .types_weight import WeightedUnit
from .types_semantic import SemanticTransferResult


# ---------------------------------------------------------------------------
# Layer 5: Compositional structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RoleAssignment:
    """A single role assignment within a compositional relation."""

    unit: WeightedUnit
    role: RoleTag

    @property
    def semantic_transfer(self) -> Optional[SemanticTransferResult]:
        """Access the semantic transfer result from the underlying weight, if present."""
        return self.unit.weight.semantic_transfer


@dataclass
class CompositionRelation:
    """A compositional relation carrying semantics of role distribution."""

    kind: RelationKind
    roles: list[RoleAssignment] = field(default_factory=list)
    closure: ClosureStatus = ClosureStatus.OPEN
    semantics: str = ""  # human-readable role-distribution description

    @property
    def semantic_compatibility_score(self) -> float:
        """Compute semantic compatibility between role units.

        If both units in a relation have semantic transfer results,
        compute the cosine similarity between their output kernels.
        Returns 1.0 if semantic data is unavailable (backward compatible).
        """
        transfers = [
            r.semantic_transfer
            for r in self.roles
            if r.semantic_transfer is not None
        ]
        if len(transfers) < 2:
            return 1.0
        # Compare first two units' output kernels
        t0 = transfers[0]
        t1 = transfers[1]
        if t0.output_kernel.dim == 0 or t1.output_kernel.dim == 0:
            return 1.0
        if t0.output_kernel.dim != t1.output_kernel.dim:
            return 0.5  # dimension mismatch → partial
        return t0.output_kernel.cosine_similarity(t1.output_kernel)
