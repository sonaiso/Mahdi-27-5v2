"""
Judgement data types for the Arabic Cognitive Fractal Engine.

Defines data structures for Layers 6-8: Proposition, Judgement, Qiyas.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .enums_gate import ClosureStatus, GateVerdict
from .enums_judgement import JudgementDirection, JudgementRank
from .types_composition import CompositionRelation


# ---------------------------------------------------------------------------
# Layer 6: Proposition
# ---------------------------------------------------------------------------

@dataclass
class Proposition:
    """Layer 6 — a proposition built from closed compositional relations."""

    relations: list[CompositionRelation] = field(default_factory=list)
    closure: ClosureStatus = ClosureStatus.OPEN


# ---------------------------------------------------------------------------
# Layer 7: Judgement
# ---------------------------------------------------------------------------

@dataclass
class Judgement:
    """Layer 7 — a judgement conditioned on a closed proposition."""

    proposition: Optional[Proposition] = None
    verdict: Optional[GateVerdict] = None
    direction: Optional[JudgementDirection] = None
    rank: Optional[JudgementRank] = None
    subject: str = ""
    criterion: str = ""
    reason: str = ""
    closure: ClosureStatus = ClosureStatus.OPEN


# ---------------------------------------------------------------------------
# Layer 8: Qiyas
# ---------------------------------------------------------------------------

@dataclass
class Qiyas:
    """Layer 8 — analogical reasoning built on a closed judgement."""

    judgement: Optional[Judgement] = None
    closure: ClosureStatus = ClosureStatus.OPEN
