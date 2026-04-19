"""
Trace data types for the Arabic Cognitive Fractal Engine.

Defines trace event records for audit, replay, and diagnostics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .enums_domain import Layer
from .enums_gate import GateVerdict
from .enums_trace import TraceEventKind, TraceSeverity


@dataclass(frozen=True)
class TraceEvent:
    """A single trace event recorded during processing."""

    kind: TraceEventKind
    layer: Layer
    severity: TraceSeverity = TraceSeverity.INFO
    verdict: Optional[GateVerdict] = None
    reason: str = ""
    details: str = ""


@dataclass
class TraceLog:
    """Ordered log of trace events for a processing run."""

    events: list[TraceEvent] = field(default_factory=list)

    def append(self, event: TraceEvent) -> None:
        self.events.append(event)

    def filter_by_layer(self, layer: Layer) -> list[TraceEvent]:
        return [e for e in self.events if e.layer is layer]

    def filter_by_kind(self, kind: TraceEventKind) -> list[TraceEvent]:
        return [e for e in self.events if e.kind is kind]

    @property
    def has_errors(self) -> bool:
        return any(
            e.severity in (TraceSeverity.ERROR, TraceSeverity.CRITICAL)
            for e in self.events
        )
