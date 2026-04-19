"""
Khabar/Insha classifier — determines communicative mode.

Classifies a proposition as خبر (informative) or إنشاء (performative).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from arabic_engine.core.enums_domain import CommunicativeMode
from arabic_engine.core.types_judgement import Proposition


@dataclass
class CommunicativeResult:
    """Result of khabar/insha classification."""

    mode: Optional[CommunicativeMode] = None
    reason: str = ""


class KhabarInshaClassifier:
    """Classifies a proposition's communicative mode."""

    @staticmethod
    def classify(prop: Proposition, mode: CommunicativeMode) -> CommunicativeResult:
        """Classify the proposition with the given communicative mode.

        In a full implementation, this would analyze the proposition's
        structure to determine mode. Currently accepts an explicit mode.
        """
        return CommunicativeResult(
            mode=mode,
            reason=f"تصنيف تواصلي: {mode.name}",
        )
