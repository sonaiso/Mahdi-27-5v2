"""
Tadmini (embedding) relation builder — النسبة التضمينية.

Builds embedding/containment relations such as حال and تمييز.
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus
from arabic_engine.core.enums_domain import RelationKind, RoleTag
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_weight import WeightedUnit
from arabic_engine.core.types_composition import CompositionRelation, RoleAssignment

from .roles import CompositionEligibilityGate


class TadminiRelationBuilder:
    """Builds a تضمينية (embedding) composition relation."""

    @staticmethod
    def build(
        container: WeightedUnit,
        contained: WeightedUnit,
        contained_role: RoleTag = RoleTag.HAL,
    ) -> tuple[CompositionRelation | None, list[GateResult]]:
        """Attempt to build an embedding relation.

        *contained_role* defaults to HAL (حال) but may be TAMYIZ (تمييز).
        """
        results: list[GateResult] = []

        for unit in (container, contained):
            r = CompositionEligibilityGate.evaluate(unit)
            results.append(r)
            if not r.passed:
                return None, results

        relation = CompositionRelation(
            kind=RelationKind.TADMINI,
            roles=[
                RoleAssignment(unit=container, role=RoleTag.FA3IL),
                RoleAssignment(unit=contained, role=contained_role),
            ],
            closure=ClosureStatus.CLOSED,
            semantics=f"نسبة تضمينية: حامل ← {contained_role.name}",
        )
        return relation, results
