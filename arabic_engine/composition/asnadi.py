"""
Asnadi (predicative) relation builder — النسبة الإسنادية.

Builds predicative relations between a subject (مسند إليه) and a predicate (مسند).
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer, RelationKind, RoleTag
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_weight import WeightedUnit
from arabic_engine.core.types_composition import CompositionRelation, RoleAssignment

from .roles import CompositionEligibilityGate


class AsnadiRelationBuilder:
    """Builds an إسنادية (predicative) composition relation."""

    @staticmethod
    def build(
        musnad_ilayh: WeightedUnit,
        musnad: WeightedUnit,
    ) -> tuple[CompositionRelation | None, list[GateResult]]:
        """Attempt to build a predicative relation.

        Returns (relation, gate_results). Relation is None if any gate fails.
        """
        results: list[GateResult] = []

        for unit, label in [
            (musnad_ilayh, "المسند إليه"),
            (musnad, "المسند"),
        ]:
            r = CompositionEligibilityGate.evaluate(unit)
            results.append(r)
            if not r.passed:
                return None, results

        relation = CompositionRelation(
            kind=RelationKind.ASNADI,
            roles=[
                RoleAssignment(unit=musnad_ilayh, role=RoleTag.MUSNAD_ILAYH),
                RoleAssignment(unit=musnad, role=RoleTag.MUSNAD),
            ],
            closure=ClosureStatus.CLOSED,
            semantics="نسبة إسنادية: المسند إليه ← المسند",
        )
        return relation, results
