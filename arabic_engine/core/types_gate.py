"""
Gate data types for the Arabic Cognitive Fractal Engine.

Defines the GateResult structure returned by every gate check.
"""

from __future__ import annotations

from dataclasses import dataclass

from .enums_gate import GateVerdict
from .enums_domain import Layer


@dataclass(frozen=True)
class GateResult:
    """Result of a gate check at any layer."""

    verdict: GateVerdict
    layer: Layer
    reason: str = ""
    missing_condition: str = ""

    @property
    def passed(self) -> bool:
        return self.verdict is GateVerdict.PASS
