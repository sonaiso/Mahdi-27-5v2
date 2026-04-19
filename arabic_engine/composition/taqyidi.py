"""
Taqyidi (restrictive) relation builder — النسبة التقييدية.

Builds restrictive/qualifying relations such as إضافة and وصف.
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus
from arabic_engine.core.enums_domain import RelationKind, RoleTag
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_weight import WeightedUnit
from arabic_engine.core.types_composition import CompositionRelation, RoleAssignment

from .roles import CompositionEligibilityGate


class TaqyidiRelationBuilder:
    """Builds a تقييدية (restrictive) composition relation."""

    @staticmethod
    def build_idafa(
        mudaf: WeightedUnit,
        mudaf_ilayh: WeightedUnit,
    ) -> tuple[CompositionRelation | None, list[GateResult]]:
        """Build an إضافة (construct-state) relation."""
        results: list[GateResult] = []

        for unit in (mudaf, mudaf_ilayh):
            r = CompositionEligibilityGate.evaluate(unit)
            results.append(r)
            if not r.passed:
                return None, results

        relation = CompositionRelation(
            kind=RelationKind.TAQYIDI,
            roles=[
                RoleAssignment(unit=mudaf, role=RoleTag.MUDAF),
                RoleAssignment(unit=mudaf_ilayh, role=RoleTag.MUDAF_ILAYH),
            ],
            closure=ClosureStatus.CLOSED,
            semantics="نسبة تقييدية: مضاف ← مضاف إليه",
        )
        return relation, results

    @staticmethod
    def build_sifa(
        mawsuf: WeightedUnit,
        sifa: WeightedUnit,
    ) -> tuple[CompositionRelation | None, list[GateResult]]:
        """Build a وصف (qualification) relation."""
        results: list[GateResult] = []

        for unit in (mawsuf, sifa):
            r = CompositionEligibilityGate.evaluate(unit)
            results.append(r)
            if not r.passed:
                return None, results

        relation = CompositionRelation(
            kind=RelationKind.TAQYIDI,
            roles=[
                RoleAssignment(unit=mawsuf, role=RoleTag.MAWSUF),
                RoleAssignment(unit=sifa, role=RoleTag.SIFA),
            ],
            closure=ClosureStatus.CLOSED,
            semantics="نسبة تقييدية: موصوف ← صفة",
        )
        return relation, results
