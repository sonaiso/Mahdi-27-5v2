"""
Composition closure engine — orchestrates Layer 5.

Validates that all relations in a composition are properly closed.
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_composition import CompositionRelation


class CompositionClosureEngine:
    """Orchestrates composition closure for a list of relations."""

    @staticmethod
    def close(relations: list[CompositionRelation]) -> list[GateResult]:
        """Validate that every relation in the list is closed.

        Returns a GateResult per relation.
        """
        results: list[GateResult] = []

        for rel in relations:
            if rel.closure is ClosureStatus.CLOSED:
                results.append(GateResult(
                    verdict=GateVerdict.PASS,
                    layer=Layer.COMPOSITIONAL_ROLES,
                ))
            else:
                results.append(GateResult(
                    verdict=GateVerdict.REJECT,
                    layer=Layer.COMPOSITIONAL_ROLES,
                    reason=f"العلاقة {rel.kind.name} غير مقفلة",
                    missing_condition="relation_closure",
                ))

        return results
