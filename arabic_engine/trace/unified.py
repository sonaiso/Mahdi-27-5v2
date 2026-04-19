"""
Unified tracer — records trace events across all layers.
"""

from __future__ import annotations

from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.enums_gate import GateVerdict
from arabic_engine.core.enums_trace import TraceEventKind, TraceSeverity
from arabic_engine.core.types_trace import TraceEvent, TraceLog
from arabic_engine.core.types_gate import GateResult


class UnifiedTracer:
    """Records and manages trace events for a processing pipeline."""

    def __init__(self) -> None:
        self._log = TraceLog()

    @property
    def log(self) -> TraceLog:
        return self._log

    def record_gate(self, result: GateResult) -> None:
        """Record a gate check result as a trace event."""
        if result.passed:
            severity = TraceSeverity.INFO
            kind = TraceEventKind.GATE_CHECK
        elif result.verdict is GateVerdict.SUSPEND:
            severity = TraceSeverity.WARNING
            kind = TraceEventKind.SUSPENSION
        else:
            severity = TraceSeverity.ERROR
            kind = TraceEventKind.REJECTION

        event = TraceEvent(
            kind=kind,
            layer=result.layer,
            severity=severity,
            verdict=result.verdict,
            reason=result.reason,
            details=result.missing_condition,
        )
        self._log.append(event)

    def record_transition(self, from_layer: Layer, to_layer: Layer) -> None:
        """Record a layer transition."""
        event = TraceEvent(
            kind=TraceEventKind.LAYER_TRANSITION,
            layer=to_layer,
            severity=TraceSeverity.INFO,
            reason=f"الانتقال من {from_layer.name} إلى {to_layer.name}",
        )
        self._log.append(event)

    def record_closure(self, layer: Layer, reason: str = "") -> None:
        """Record a closure event."""
        event = TraceEvent(
            kind=TraceEventKind.CLOSURE_CHANGE,
            layer=layer,
            severity=TraceSeverity.INFO,
            reason=reason or f"إغلاق {layer.name}",
        )
        self._log.append(event)
