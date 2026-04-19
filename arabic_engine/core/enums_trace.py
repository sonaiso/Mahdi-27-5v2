"""
Trace enumerations for the Arabic Cognitive Fractal Engine.

Defines trace-related distinctions for audit, replay, and diagnostics.
"""

from enum import Enum, auto


class TraceEventKind(Enum):
    """Kind of event recorded in a trace."""

    GATE_CHECK = auto()       # A gate was evaluated
    CLOSURE_CHANGE = auto()   # A closure status changed
    LAYER_TRANSITION = auto() # Transition from one layer to the next
    REJECTION = auto()        # A rejection occurred
    SUSPENSION = auto()       # A suspension occurred
    REPLAY = auto()           # A replay was performed


class TraceSeverity(Enum):
    """Severity level for trace events."""

    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()
