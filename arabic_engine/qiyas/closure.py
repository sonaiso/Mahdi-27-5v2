"""
Qiyas closure engine — orchestrates Layer 8 closure.
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_judgement import Qiyas

from .transition import QiyasTransitionEngine


class QiyasClosureEngine:
    """Orchestrates qiyas closure."""

    @staticmethod
    def close(qiyas: Qiyas) -> GateResult:
        """Attempt to close the qiyas layer."""
        result = QiyasTransitionEngine.validate_transition(qiyas)

        if result.passed:
            qiyas.closure = ClosureStatus.CLOSED
        elif result.verdict is GateVerdict.SUSPEND:
            qiyas.closure = ClosureStatus.SUSPENDED
        else:
            qiyas.closure = ClosureStatus.BLOCKED

        return result
