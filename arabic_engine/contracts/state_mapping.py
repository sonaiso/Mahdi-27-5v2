"""
State mapping — unified state model for all closure statuses.

Maps between different status representations to prevent taxonomy conflicts (R11).
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict


class StateMapper:
    """Maps between gate verdicts and closure statuses.

    Provides a single source of truth for status transitions,
    preventing the taxonomy conflicts identified in R11.
    """

    _VERDICT_TO_CLOSURE = {
        GateVerdict.PASS: ClosureStatus.CLOSED,
        GateVerdict.REJECT: ClosureStatus.BLOCKED,
        GateVerdict.SUSPEND: ClosureStatus.SUSPENDED,
    }

    _CLOSURE_TO_VERDICT = {
        ClosureStatus.CLOSED: GateVerdict.PASS,
        ClosureStatus.BLOCKED: GateVerdict.REJECT,
        ClosureStatus.SUSPENDED: GateVerdict.SUSPEND,
        ClosureStatus.OPEN: GateVerdict.SUSPEND,  # OPEN implies not yet decided
    }

    @staticmethod
    def verdict_to_closure(verdict: GateVerdict) -> ClosureStatus:
        """Convert a GateVerdict to the corresponding ClosureStatus."""
        return StateMapper._VERDICT_TO_CLOSURE[verdict]

    @staticmethod
    def closure_to_verdict(status: ClosureStatus) -> GateVerdict:
        """Convert a ClosureStatus to the most appropriate GateVerdict."""
        return StateMapper._CLOSURE_TO_VERDICT[status]
