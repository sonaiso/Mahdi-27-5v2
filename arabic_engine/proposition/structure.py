"""
Proposition structure — builds a proposition from closed compositional relations.
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_composition import CompositionRelation
from arabic_engine.core.types_judgement import Proposition


class PropositionBuilder:
    """Builds a proposition from a list of composition relations."""

    @staticmethod
    def build(relations: list[CompositionRelation]) -> tuple[Proposition | None, GateResult]:
        """Attempt to build a proposition.

        All relations must be closed. Returns (proposition, gate_result).
        """
        if not relations:
            return None, GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.PROPOSITION,
                reason="لا توجد علاقات تركيبية لبناء قضية",
                missing_condition="relations",
            )

        for rel in relations:
            if rel.closure is not ClosureStatus.CLOSED:
                return None, GateResult(
                    verdict=GateVerdict.REJECT,
                    layer=Layer.PROPOSITION,
                    reason=f"العلاقة {rel.kind.name} غير مقفلة",
                    missing_condition="all_relations_closed",
                )

        prop = Proposition(
            relations=list(relations),
            closure=ClosureStatus.CLOSED,
        )
        return prop, GateResult(
            verdict=GateVerdict.PASS,
            layer=Layer.PROPOSITION,
        )
