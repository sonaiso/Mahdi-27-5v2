"""Tests for non-invasive foundational integration hooks/adapters."""

from arabic_engine.foundational.integration import FoundationalIntegrationBridge
from arabic_engine.foundational.models import (
    FoundationalUnit,
    OntologicalPropertyProfile,
    SymbolKind,
    SymbolicToken,
)
from arabic_engine.foundational.symbolic_encoding import SymbolicEncodingGate
from arabic_engine.language.foundational_hook import LanguageFoundationalAdapter
from arabic_engine.semantic_kernel.foundational_hook import SemanticKernelFoundationalAdapter


def _unit() -> FoundationalUnit:
    letter = SymbolicToken(symbol="ب", codepoint=0x0628, kind=SymbolKind.LETTER)
    diacritic = SymbolicToken(symbol="ِ", codepoint=0x0650, kind=SymbolKind.DIACRITIC)
    SymbolicEncodingGate.close(letter)
    SymbolicEncodingGate.close(diacritic)
    return FoundationalUnit(
        letter=letter,
        diacritic=diacritic,
        ontology=OntologicalPropertyProfile(
            letter_essential={"is_letter": True, "has_base_shape": True},
            diacritic_essential={"is_diacritic": True, "is_mark": True},
            contextual={"position_in_word": "initial"},
        ),
    )


def test_semantic_kernel_adapter_exposes_hook_payload():
    payload = SemanticKernelFoundationalAdapter.from_foundational(_unit())
    assert payload["attachment_point"] == "semantic_kernel"
    assert payload["trace_id"] == "foundational.hook.semantic-kernel"


def test_language_adapter_exposes_hook_payload():
    payload = LanguageFoundationalAdapter.from_foundational(_unit())
    assert payload["attachment_point"] == "language"
    assert payload["trace_id"] == "foundational.hook.language"


def test_traceability_mapping_exposes_future_attachment_points():
    mapping = FoundationalIntegrationBridge.traceability_mapping(_unit())
    assert "arabic_engine.semantic_kernel.foundational_hook" in mapping["future_attachment_points"]
    assert "arabic_engine.language.foundational_hook" in mapping["future_attachment_points"]
    assert "symbolic_identity_invariant" in mapping["contracts"]
    assert mapping["trace_id"] == "foundational.traceability.mapping"

