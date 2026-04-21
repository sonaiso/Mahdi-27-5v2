"""Tests for foundational contract invariants."""

from arabic_engine.foundational.contracts import FoundationalInvariantContract
from arabic_engine.foundational.models import (
    FoundationalUnit,
    OntologicalPropertyProfile,
    SymbolKind,
    SymbolicToken,
)
from arabic_engine.foundational.symbolic_encoding import SymbolicEncodingGate


def _complete_unit() -> FoundationalUnit:
    letter = SymbolicToken(symbol="ك", codepoint=0x0643, kind=SymbolKind.LETTER)
    diacritic = SymbolicToken(symbol="َ", codepoint=0x064E, kind=SymbolKind.DIACRITIC)
    SymbolicEncodingGate.close(letter)
    SymbolicEncodingGate.close(diacritic)
    return FoundationalUnit(
        letter=letter,
        diacritic=diacritic,
        ontology=OntologicalPropertyProfile(
            letter_essential={"is_letter": True, "has_base_shape": True},
            diacritic_essential={"is_diacritic": True, "is_mark": True},
            contextual={"phonetic_context": "open-syllable"},
        ),
    )


def test_symbolic_identity_invariant_passes():
    unit = _complete_unit()
    assert FoundationalInvariantContract.symbolic_identity_invariant(unit)


def test_normalization_invariant_passes():
    unit = _complete_unit()
    assert FoundationalInvariantContract.normalization_invariant(unit)


def test_ontological_completeness_invariant_passes():
    unit = _complete_unit()
    assert FoundationalInvariantContract.ontological_property_completeness_invariant(unit)


def test_essential_contextual_separation_invariant_fails_on_overlap():
    unit = _complete_unit()
    unit.ontology.contextual["is_mark"] = "invalid-overlap"
    assert not FoundationalInvariantContract.essential_contextual_separation_invariant(unit)

