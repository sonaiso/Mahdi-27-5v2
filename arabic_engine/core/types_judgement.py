"""
Judgement data types for the Arabic Cognitive Fractal Engine.

Defines data structures for Layers 6-8: Proposition, Judgement, Qiyas.

Semantic kernel integration: Propositions can aggregate semantic transfer
results from their composition relations, and Judgements can incorporate
semantic kernel information for semantically-informed truthiness assessments.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .enums_gate import ClosureStatus, GateVerdict
from .enums_judgement import (
    JudgementDirection,
    JudgementRank,
    QiyasKind,
    QiyasValidity,
)
from .types_composition import CompositionRelation


# ---------------------------------------------------------------------------
# Layer 6: Proposition
# ---------------------------------------------------------------------------

@dataclass
class Proposition:
    """Layer 6 — a proposition built from closed compositional relations."""

    relations: list[CompositionRelation] = field(default_factory=list)
    closure: ClosureStatus = ClosureStatus.OPEN

    @property
    def semantic_coherence_score(self) -> float:
        """Aggregate semantic compatibility across all composition relations.

        Returns 1.0 if no semantic data is available (backward compatible).
        """
        scores = [
            r.semantic_compatibility_score
            for r in self.relations
        ]
        if not scores:
            return 1.0
        return sum(scores) / len(scores)


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
    semantic_confidence: float = 1.0  # semantic kernel confidence [0.0, 1.0]
    closure: ClosureStatus = ClosureStatus.OPEN


# ---------------------------------------------------------------------------
# Layer 8: Qiyas (القياس — analogical reasoning)
# ---------------------------------------------------------------------------

@dataclass
class Qiyas:
    """Layer 8 — analogical reasoning built on a closed judgement.

    القياس هو إلحاق فرع بأصل في حكم لعلّة جامعة بينهما.
    The four pillars of qiyas:
      1. asl (الأصل) — the original case with an established judgement
      2. far3 (الفرع) — the new case to be judged
      3. hukm (الحكم) — the ruling to be transferred
      4. illa (العلة) — the effective cause that links original to new
    """

    judgement: Optional[Judgement] = None
    asl: str = ""        # الأصل — the original case
    far3: str = ""       # الفرع — the branch / new case
    illa: str = ""       # العلة — the effective cause
    hukm_transferred: str = ""  # الحكم المنقول — the transferred ruling
    kind: Optional[QiyasKind] = None
    validity: Optional[QiyasValidity] = None
    confidence: float = 1.0  # derived from judgement's semantic_confidence
    closure: ClosureStatus = ClosureStatus.OPEN
