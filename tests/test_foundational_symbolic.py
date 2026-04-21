"""Tests for foundational Layer 1 (Symbolic Encoding)."""

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.foundational.models import SymbolKind, SymbolicToken
from arabic_engine.foundational.symbolic_encoding import SymbolicEncodingGate


def test_symbolic_encoding_passes_for_normalized_letter():
    token = SymbolicToken(
        symbol="ك",
        codepoint=0x0643,
        kind=SymbolKind.LETTER,
        normalization_form="NFC",
    )
    result = SymbolicEncodingGate.close(token)
    assert result.passed
    assert token.closure is ClosureStatus.CLOSED


def test_symbolic_encoding_rejects_identity_mismatch():
    token = SymbolicToken(
        symbol="ك",
        codepoint=0x0628,
        kind=SymbolKind.LETTER,
    )
    result = SymbolicEncodingGate.close(token)
    assert result.verdict is GateVerdict.REJECT
    assert result.missing_condition == "symbolic_identity_invariant"


def test_symbolic_encoding_suspends_when_not_normalized():
    token = SymbolicToken(
        symbol="\uFE91",  # presentation form, not normalized under NFKC
        codepoint=0xFE91,
        kind=SymbolKind.LETTER,
        normalization_form="NFKC",
    )
    result = SymbolicEncodingGate.close(token)
    assert result.verdict is GateVerdict.SUSPEND
    assert result.missing_condition == "normalization_invariant"
    assert token.closure is ClosureStatus.SUSPENDED

