"""
Communicative closure engine — orchestrates communicative and stylistic closure.
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import GateVerdict
from arabic_engine.core.enums_domain import CommunicativeMode
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_judgement import Proposition

from .khabar_insha import KhabarInshaClassifier, CommunicativeResult
from .stylistic import StylisticGate


class CommunicativeClosureEngine:
    """Orchestrates communicative and stylistic closure."""

    @staticmethod
    def close(
        prop: Proposition,
        mode: CommunicativeMode,
    ) -> tuple[CommunicativeResult, list[GateResult]]:
        """Run the communicative closure pipeline.

        Returns (CommunicativeResult, list of GateResults).
        """
        results: list[GateResult] = []

        comm_result = KhabarInshaClassifier.classify(prop, mode)

        stylistic_result = StylisticGate.evaluate(comm_result)
        results.append(stylistic_result)

        return comm_result, results
