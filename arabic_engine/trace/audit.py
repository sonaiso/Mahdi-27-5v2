"""
Trace auditor — validates trace integrity and completeness.
"""

from __future__ import annotations

from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.enums_trace import TraceEventKind
from arabic_engine.core.types_trace import TraceLog


class TraceAuditor:
    """Audits a trace log for completeness and integrity."""

    REQUIRED_LAYERS = [
        Layer.PRE_U0_ADMISSIBILITY,
        Layer.SINGULAR_PERCEPTUAL,
        Layer.SINGULAR_INFORMATIONAL,
        Layer.SINGULAR_CONCEPTUAL,
        Layer.WEIGHT_MIZAN,
    ]

    @staticmethod
    def audit_layer_coverage(log: TraceLog) -> dict[Layer, bool]:
        """Check which layers have at least one trace event."""
        covered_layers = {event.layer for event in log.events}
        return {layer: layer in covered_layers for layer in TraceAuditor.REQUIRED_LAYERS}

    @staticmethod
    def audit_no_jump(log: TraceLog) -> list[str]:
        """Check for anti-jump violations in the trace.

        Returns a list of violation descriptions. Empty list means no violations.
        """
        violations: list[str] = []
        transitions = [
            e for e in log.events if e.kind is TraceEventKind.LAYER_TRANSITION
        ]

        for i in range(1, len(transitions)):
            prev = transitions[i - 1].layer
            curr = transitions[i].layer
            if curr.value > prev.value + 1:
                violations.append(
                    f"قفز من {prev.name} إلى {curr.name} — انتهاك منع القفز"
                )

        return violations

    @staticmethod
    def is_complete(log: TraceLog) -> bool:
        """Check that all required layers are covered and no jumps occurred."""
        coverage = TraceAuditor.audit_layer_coverage(log)
        return all(coverage.values()) and not TraceAuditor.audit_no_jump(log)
