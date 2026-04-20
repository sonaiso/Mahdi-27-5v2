"""
Qiyas model — defines the full qiyas structure.

القياس هو إلحاق فرع بأصل في حكم لعلّة جامعة بينهما.

A qiyas requires:
  - judgement (الحكم الأصلي) — a closed judgement
  - asl (الأصل) — the original case
  - far3 (الفرع) — the new case
  - illa (العلة) — the effective cause linking both
  - kind (نوع القياس) — type of analogical reasoning
"""

from __future__ import annotations

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.enums_judgement import QiyasKind, QiyasValidity
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_judgement import Judgement, Qiyas


class QiyasModel:
    """Builds and validates a qiyas."""

    @staticmethod
    def build(
        judgement: Judgement,
        asl: str,
        far3: str,
        illa: str,
        kind: QiyasKind,
        hukm_transferred: str = "",
    ) -> tuple[Qiyas | None, GateResult]:
        """Build a qiyas from a closed judgement.

        Returns (qiyas, gate_result).
        """
        if judgement.closure is not ClosureStatus.CLOSED:
            return None, GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.QIYAS,
                reason="الحكم غير مقفل — لا يجوز بناء قياس",
                missing_condition="judgement_closed",
            )

        if not asl:
            return None, GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.QIYAS,
                reason="لا يوجد أصل للقياس",
                missing_condition="asl",
            )

        if not far3:
            return None, GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.QIYAS,
                reason="لا يوجد فرع للقياس",
                missing_condition="far3",
            )

        if not illa:
            return None, GateResult(
                verdict=GateVerdict.REJECT,
                layer=Layer.QIYAS,
                reason="لا توجد علة جامعة للقياس",
                missing_condition="illa",
            )

        # Derive the transferred ruling from the judgement if not explicit
        effective_hukm = hukm_transferred or (
            f"{judgement.direction.name}: {judgement.subject}"
            if judgement.direction
            else judgement.subject
        )

        qiyas = Qiyas(
            judgement=judgement,
            asl=asl,
            far3=far3,
            illa=illa,
            hukm_transferred=effective_hukm,
            kind=kind,
            validity=QiyasValidity.VALID,
            confidence=judgement.semantic_confidence,
            closure=ClosureStatus.CLOSED,
        )
        return qiyas, GateResult(
            verdict=GateVerdict.PASS,
            layer=Layer.QIYAS,
        )
