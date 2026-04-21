"""
Ontological Property gate — foundational Layer 2.
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict

from .contracts import FoundationalInvariantContract
from .models import FoundationalGateResult, FoundationalLayer, FoundationalUnit


class OntologicalPropertyGate:
    """Validates essential/contextual ontological property contracts."""

    LAYER = FoundationalLayer.ONTOLOGICAL_PROPERTY

    @staticmethod
    def evaluate(unit: FoundationalUnit) -> FoundationalGateResult:
        """Evaluate Layer 2 ontological contracts."""
        if unit.letter is None and unit.diacritic is None:
            return FoundationalGateResult(
                verdict=GateVerdict.REJECT,
                layer=OntologicalPropertyGate.LAYER,
                reason="الوحدة التأسيسية فارغة (لا حرف ولا حركة)",
                missing_condition="foundational_scope_v1",
                trace_id="foundational.ontology.scope-v1",
            )

        if not FoundationalInvariantContract.ontological_property_completeness_invariant(unit):
            return FoundationalGateResult(
                verdict=GateVerdict.SUSPEND,
                layer=OntologicalPropertyGate.LAYER,
                reason="نقص في ملف الخواص الجوهرية للحرف/الحركة",
                missing_condition="ontological_property_completeness_invariant",
                trace_id="foundational.ontology.completeness-invariant",
            )

        if not FoundationalInvariantContract.essential_contextual_separation_invariant(unit):
            return FoundationalGateResult(
                verdict=GateVerdict.REJECT,
                layer=OntologicalPropertyGate.LAYER,
                reason="خلط بين الخواص الجوهرية والسياقية",
                missing_condition="essential_contextual_separation_invariant",
                trace_id="foundational.ontology.essential-contextual-separation",
            )

        return FoundationalGateResult(
            verdict=GateVerdict.PASS,
            layer=OntologicalPropertyGate.LAYER,
            trace_id="foundational.ontology.pass",
        )

    @staticmethod
    def close(unit: FoundationalUnit) -> FoundationalGateResult:
        """Attempt to close Layer 2 state."""
        result = OntologicalPropertyGate.evaluate(unit)
        if result.passed:
            unit.ontology.closure = ClosureStatus.CLOSED
        elif result.verdict is GateVerdict.SUSPEND:
            unit.ontology.closure = ClosureStatus.SUSPENDED
        else:
            unit.ontology.closure = ClosureStatus.BLOCKED
        return result

