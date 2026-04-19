"""
Gate and closure enumerations for the Arabic Cognitive Fractal Engine.

Defines gate verdicts and closure status used across all layers.
"""

from enum import Enum, auto


class ClosureStatus(Enum):
    """Status of a closure gate at any layer."""

    OPEN = auto()        # Not yet evaluated
    CLOSED = auto()      # Successfully closed — all conditions met
    BLOCKED = auto()     # A blocker prevents closure
    SUSPENDED = auto()   # Temporarily suspended pending further information


class GateVerdict(Enum):
    """Verdict returned by a gate check."""

    PASS = auto()
    REJECT = auto()
    SUSPEND = auto()
