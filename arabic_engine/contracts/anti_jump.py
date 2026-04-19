"""
Anti-jump contract — prevents skipping layers in the pipeline.
"""

from __future__ import annotations

from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.enums_gate import GateVerdict
from arabic_engine.core.types_gate import GateResult


class AntiJumpContract:
    """Prevents jumping from layer N to layer N+k where k > 1."""

    @staticmethod
    def check_transition(from_layer: Layer, to_layer: Layer) -> GateResult:
        """Validate that a transition does not skip layers."""
        if to_layer.value > from_layer.value + 1:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=to_layer,
                reason=f"قفز من {from_layer.name} إلى {to_layer.name} — ممنوع",
                missing_condition="anti_jump",
            )

        if to_layer.value <= from_layer.value:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=to_layer,
                reason=f"انتقال عكسي من {from_layer.name} إلى {to_layer.name} — ممنوع",
                missing_condition="forward_only",
            )

        return GateResult(
            verdict=GateVerdict.PASS,
            layer=to_layer,
        )
