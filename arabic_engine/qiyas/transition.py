"""
Qiyas transition engine — manages the judgement-to-qiyas transition.

Enforces that no qiyas may be issued without a fully closed judgement
and all four pillars of qiyas (الأصل، الفرع، العلة، الحكم).
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_judgement import Qiyas


class QiyasTransitionEngine:
    """Validates the transition from judgement to qiyas."""

    @staticmethod
    def validate_transition(qiyas: Qiyas) -> GateResult:
        """Validate that the transition to qiyas is legal.

        Checks the four pillars: الأصل (asl), الفرع (far3),
        العلة (illa), and الحكم المنقول (hukm_transferred).
        """
        if qiyas.judgement is None:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.QIYAS,
                reason="لا يوجد حكم أساس للقياس",
                missing_condition="judgement",
            )

        if qiyas.judgement.closure is not ClosureStatus.CLOSED:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.QIYAS,
                reason="الحكم غير مقفل — لا يجوز الانتقال إلى القياس",
                missing_condition="judgement_closed",
            )

        if not qiyas.asl:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.QIYAS,
                reason="لا يوجد أصل للقياس — الركن الأول مفقود",
                missing_condition="asl",
            )

        if not qiyas.far3:
            return GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.QIYAS,
                reason="لا يوجد فرع للقياس — الركن الثاني مفقود",
                missing_condition="far3",
            )

        if not qiyas.illa:
            return GateResult(
                verdict=GateVerdict.SUSPEND,
                layer=Layer.QIYAS,
                reason="لم تُحدَّد العلة الجامعة — الركن الثالث غير مكتمل",
                missing_condition="illa",
            )

        if qiyas.kind is None:
            return GateResult(
                verdict=GateVerdict.SUSPEND,
                layer=Layer.QIYAS,
                reason="لم يُحدَّد نوع القياس (علة/دلالة/شبه)",
                missing_condition="qiyas_kind",
            )

        return GateResult(
            verdict=GateVerdict.PASS,
            layer=Layer.QIYAS,
        )
