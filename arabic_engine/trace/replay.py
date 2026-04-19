"""
Trace replayer — replays a trace log for diagnostics and verification.
"""

from __future__ import annotations

from arabic_engine.core.enums_trace import TraceEventKind, TraceSeverity
from arabic_engine.core.types_trace import TraceEvent, TraceLog


class TraceReplayer:
    """Replays a trace log and generates a human-readable summary."""

    @staticmethod
    def replay(log: TraceLog) -> list[str]:
        """Produce a list of human-readable trace lines."""
        lines: list[str] = []
        for i, event in enumerate(log.events):
            prefix = f"[{i:03d}] [{event.severity.name}] [{event.layer.name}]"
            detail = event.reason or event.kind.name
            lines.append(f"{prefix} {detail}")
        return lines

    @staticmethod
    def replay_errors(log: TraceLog) -> list[str]:
        """Replay only error and critical events."""
        lines: list[str] = []
        for i, event in enumerate(log.events):
            if event.severity in (TraceSeverity.ERROR, TraceSeverity.CRITICAL):
                prefix = f"[{i:03d}] [{event.severity.name}] [{event.layer.name}]"
                lines.append(f"{prefix} {event.reason}")
        return lines
