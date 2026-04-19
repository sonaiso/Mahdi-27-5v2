"""
Judgement closure engine — orchestrates Layer 7 closure.
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_judgement import Judgement

from .transition import JudgementTransitionEngine


class JudgementClosureEngine:
    """Orchestrates judgement closure."""

    @staticmethod
    def close(judgement: Judgement) -> GateResult:
        """Attempt to close the judgement layer."""
        result = JudgementTransitionEngine.validate_transition(judgement)

        if result.passed:
            judgement.closure = ClosureStatus.CLOSED
        elif result.verdict is GateVerdict.SUSPEND:
            judgement.closure = ClosureStatus.SUSPENDED
        else:
            judgement.closure = ClosureStatus.BLOCKED

        return result
