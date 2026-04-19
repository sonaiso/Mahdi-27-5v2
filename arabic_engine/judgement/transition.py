"""
Judgement transition engine — manages the proposition-to-judgement transition.

Enforces that no judgement may be issued without a fully closed proposition
and all necessary judgement components (subject, direction, criterion, rank).
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_judgement import Judgement


class JudgementTransitionEngine:
    """Validates the transition from proposition to judgement."""

    @staticmethod
    def validate_transition(judgement: Judgement) -> GateResult:
        """Validate that the transition to judgement is legal."""
        if judgement.proposition is None:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.JUDGEMENT,
                reason="لا توجد قضية أساس للحكم",
                missing_condition="proposition",
            )

        if judgement.proposition.closure is not ClosureStatus.CLOSED:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.JUDGEMENT,
                reason="القضية غير مقفلة — لا يجوز الانتقال إلى الحكم",
                missing_condition="proposition_closed",
            )

        if judgement.direction is None:
            return GateResult(
                verdict=GateVerdict.SUSPEND,
                layer=Layer.JUDGEMENT,
                reason="لم تُحدَّد جهة الحكم (إثبات/نفي)",
                missing_condition="direction",
            )

        if judgement.rank is None:
            return GateResult(
                verdict=GateVerdict.SUSPEND,
                layer=Layer.JUDGEMENT,
                reason="لم تُحدَّد رتبة الحكم",
                missing_condition="rank",
            )

        if not judgement.subject:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.JUDGEMENT,
                reason="لا يوجد موضوع للحكم",
                missing_condition="subject",
            )

        if not judgement.criterion:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.JUDGEMENT,
                reason="لا يوجد معيار للحكم",
                missing_condition="criterion",
            )

        return GateResult(
            verdict=GateVerdict.PASS,
            layer=Layer.JUDGEMENT,
        )
