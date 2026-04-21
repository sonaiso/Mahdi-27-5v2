"""
Symbolic Encoding gate — foundational Layer 1.
"""

from __future__ import annotations

import unicodedata

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict

from .models import FoundationalGateResult, FoundationalLayer, SymbolicToken


class SymbolicEncodingGate:
    """Validates symbolic identity, normalization, and representation stability."""

    LAYER = FoundationalLayer.SYMBOLIC_ENCODING

    @staticmethod
    def evaluate(token: SymbolicToken) -> FoundationalGateResult:
        """Evaluate Layer 1 symbolic encoding constraints."""
        if len(token.symbol) != 1:
            return FoundationalGateResult(
                verdict=GateVerdict.REJECT,
                layer=SymbolicEncodingGate.LAYER,
                reason="الرمز يجب أن يكون وحدة Unicode واحدة",
                missing_condition="single_unicode_symbol",
                trace_id="foundational.symbolic.single-unit",
            )

        if token.codepoint <= 0 or ord(token.symbol) != token.codepoint:
            return FoundationalGateResult(
                verdict=GateVerdict.REJECT,
                layer=SymbolicEncodingGate.LAYER,
                reason="فشل invariant الهوية الرمزية بين الرمز ونقطة Unicode",
                missing_condition="symbolic_identity_invariant",
                trace_id="foundational.symbolic.identity-invariant",
            )

        if token.normalization_form not in {"NFC", "NFD", "NFKC", "NFKD"}:
            return FoundationalGateResult(
                verdict=GateVerdict.REJECT,
                layer=SymbolicEncodingGate.LAYER,
                reason="صيغة التطبيع غير مدعومة",
                missing_condition="supported_normalization_form",
                trace_id="foundational.symbolic.normalization-form",
            )

        normalized = unicodedata.normalize(token.normalization_form, token.symbol)
        if token.symbol != normalized:
            return FoundationalGateResult(
                verdict=GateVerdict.SUSPEND,
                layer=SymbolicEncodingGate.LAYER,
                reason="الرمز غير مطبّع وفق الصيغة المطلوبة",
                missing_condition="normalization_invariant",
                trace_id="foundational.symbolic.normalization-invariant",
            )

        if token.visual_glyph and len(token.visual_glyph) != 1:
            return FoundationalGateResult(
                verdict=GateVerdict.REJECT,
                layer=SymbolicEncodingGate.LAYER,
                reason="التمثيل المرئي يجب أن يكون رمزًا واحدًا",
                missing_condition="visual_symbol_arity",
                trace_id="foundational.symbolic.visual-arity",
            )

        return FoundationalGateResult(
            verdict=GateVerdict.PASS,
            layer=SymbolicEncodingGate.LAYER,
            trace_id="foundational.symbolic.pass",
        )

    @staticmethod
    def close(token: SymbolicToken) -> FoundationalGateResult:
        """Compute normalization/canonical forms and close Layer 1 token state."""
        token.normalized_symbol = unicodedata.normalize(token.normalization_form, token.symbol)
        token.canonical_form = unicodedata.normalize("NFC", token.symbol)
        token.compatibility_form = unicodedata.normalize("NFKC", token.symbol)
        token.representational_stability = (
            token.symbol == token.normalized_symbol
            and token.canonical_form == token.compatibility_form
        )

        result = SymbolicEncodingGate.evaluate(token)
        if result.passed:
            token.closure = ClosureStatus.CLOSED
        elif result.verdict is GateVerdict.SUSPEND:
            token.closure = ClosureStatus.SUSPENDED
        else:
            token.closure = ClosureStatus.BLOCKED
        return result

