"""
Concept gate — Layer 3: Singular Conceptual Closure.

Validates that word category, definiteness, gender, and derivation
have been resolved, and that weight-system eligibility is declared.
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_singular import SingularConceptual


class ConceptGate:
    """Gate that evaluates Layer 3 (Singular Conceptual) closure."""

    LAYER = Layer.SINGULAR_CONCEPTUAL

    @staticmethod
    def evaluate(concept: SingularConceptual) -> GateResult:
        """Check whether the conceptual layer is ready to close."""
        if concept.word_category is None:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=ConceptGate.LAYER,
                reason="لم يُحدَّد صنف الكلمة (اسم/فعل/حرف)",
                missing_condition="word_category",
            )

        if concept.definiteness is None:
            return GateResult(
                verdict=GateVerdict.SUSPEND,
                layer=ConceptGate.LAYER,
                reason="لم يُحدَّد التعريف/التنكير",
                missing_condition="definiteness",
            )

        if concept.gender is None:
            return GateResult(
                verdict=GateVerdict.SUSPEND,
                layer=ConceptGate.LAYER,
                reason="لم يُحدَّد التذكير/التأنيث",
                missing_condition="gender",
            )

        if concept.derivation is None:
            return GateResult(
                verdict=GateVerdict.SUSPEND,
                layer=ConceptGate.LAYER,
                reason="لم يُحدَّد الجمود/الاشتقاق",
                missing_condition="derivation",
            )

        return GateResult(
            verdict=GateVerdict.PASS,
            layer=ConceptGate.LAYER,
        )

    @staticmethod
    def close(concept: SingularConceptual) -> SingularConceptual:
        """Attempt to close the conceptual layer. Mutates in place."""
        result = ConceptGate.evaluate(concept)
        if result.passed:
            concept.closure = ClosureStatus.CLOSED
        elif result.verdict is GateVerdict.SUSPEND:
            concept.closure = ClosureStatus.SUSPENDED
        else:
            concept.closure = ClosureStatus.BLOCKED
        return concept
