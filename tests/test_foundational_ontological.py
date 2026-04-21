"""Tests for foundational Layer 2 (Ontological Property)."""

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.foundational.models import (
    FoundationalUnit,
    OntologicalPropertyProfile,
    SymbolKind,
    SymbolicToken,
)
from arabic_engine.foundational.ontological_property import OntologicalPropertyGate


def _letter() -> SymbolicToken:
    return SymbolicToken(symbol="ب", codepoint=0x0628, kind=SymbolKind.LETTER)


def _diacritic() -> SymbolicToken:
    return SymbolicToken(symbol="َ", codepoint=0x064E, kind=SymbolKind.DIACRITIC)


def test_ontological_property_rejects_empty_scope():
    unit = FoundationalUnit()
    result = OntologicalPropertyGate.close(unit)
    assert result.verdict is GateVerdict.REJECT


def test_ontological_property_suspends_missing_essential_profile():
    unit = FoundationalUnit(
        letter=_letter(),
        ontology=OntologicalPropertyProfile(
            letter_essential={"is_letter": True},
        ),
    )
    result = OntologicalPropertyGate.close(unit)
    assert result.verdict is GateVerdict.SUSPEND
    assert result.missing_condition == "ontological_property_completeness_invariant"
    assert unit.ontology.closure is ClosureStatus.SUSPENDED


def test_ontological_property_rejects_essential_context_overlap():
    unit = FoundationalUnit(
        letter=_letter(),
        diacritic=_diacritic(),
        ontology=OntologicalPropertyProfile(
            letter_essential={"is_letter": True, "has_base_shape": True},
            diacritic_essential={"is_diacritic": True, "is_mark": True},
            contextual={"is_letter": "context-drift"},
        ),
    )
    result = OntologicalPropertyGate.close(unit)
    assert result.verdict is GateVerdict.REJECT
    assert result.missing_condition == "essential_contextual_separation_invariant"


def test_ontological_property_passes_complete_profile():
    unit = FoundationalUnit(
        letter=_letter(),
        diacritic=_diacritic(),
        ontology=OntologicalPropertyProfile(
            letter_essential={"is_letter": True, "has_base_shape": True},
            diacritic_essential={"is_diacritic": True, "is_mark": True},
            contextual={"position_in_word": "medial"},
        ),
    )
    result = OntologicalPropertyGate.close(unit)
    assert result.passed
    assert unit.ontology.closure is ClosureStatus.CLOSED

