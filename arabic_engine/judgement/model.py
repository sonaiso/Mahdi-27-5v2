"""
Judgement model — defines the full judgement structure.

A judgement requires:
  - subject (الموضوع)
  - direction (الجهة) — affirmation or negation
  - criterion (المعيار)
  - rank (الرتبة) — certainty level
  - reason (التعليل)
  - a closed proposition
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.enums_judgement import JudgementDirection, JudgementRank
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_judgement import Judgement, Proposition


class JudgementModel:
    """Builds and validates a judgement."""

    @staticmethod
    def build(
        proposition: Proposition,
        direction: JudgementDirection,
        rank: JudgementRank,
        subject: str,
        criterion: str,
        reason: str = "",
    ) -> tuple[Judgement | None, GateResult]:
        """Build a judgement from a closed proposition.

        Returns (judgement, gate_result).
        """
        if proposition.closure is not ClosureStatus.CLOSED:
            return None, GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.JUDGEMENT,
                reason="القضية غير مقفلة — لا يجوز إصدار حكم",
                missing_condition="proposition_closed",
            )

        if not subject:
            return None, GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.JUDGEMENT,
                reason="لا يوجد موضوع للحكم",
                missing_condition="subject",
            )

        if not criterion:
            return None, GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.JUDGEMENT,
                reason="لا يوجد معيار للحكم",
                missing_condition="criterion",
            )

        judgement = Judgement(
            proposition=proposition,
            verdict=GateVerdict.PASS,
            direction=direction,
            rank=rank,
            subject=subject,
            criterion=criterion,
            reason=reason,
            closure=ClosureStatus.CLOSED,
        )
        return judgement, GateResult(
            verdict=GateVerdict.PASS,
            layer=Layer.JUDGEMENT,
        )
