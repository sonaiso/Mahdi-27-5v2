"""Tests for Layer 8: Qiyas (analogical reasoning)."""

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_judgement import (
    JudgementDirection,
    JudgementRank,
    QiyasKind,
    QiyasValidity,
)
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.types_judgement import Judgement, Proposition, Qiyas

from arabic_engine.qiyas.model import QiyasModel
from arabic_engine.qiyas.transition import QiyasTransitionEngine
from arabic_engine.qiyas.closure import QiyasClosureEngine


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_closed_judgement() -> Judgement:
    """Create a closed judgement for qiyas tests."""
    prop = Proposition(relations=[], closure=ClosureStatus.CLOSED)
    return Judgement(
        proposition=prop,
        verdict=GateVerdict.PASS,
        direction=JudgementDirection.AFFIRMATION,
        rank=JudgementRank.CERTAIN,
        subject="الكاتب",
        criterion="الإسناد",
        reason="إسناد صحيح",
        closure=ClosureStatus.CLOSED,
    )


# ---------------------------------------------------------------------------
# QiyasModel tests
# ---------------------------------------------------------------------------


def test_qiyas_builds_from_closed_judgement():
    judgement = _make_closed_judgement()
    qiyas, result = QiyasModel.build(
        judgement=judgement,
        asl="الخمر",
        far3="النبيذ",
        illa="الإسكار",
        kind=QiyasKind.QIYAS_ILLA,
    )
    assert result.passed
    assert qiyas is not None
    assert qiyas.closure is ClosureStatus.CLOSED
    assert qiyas.kind is QiyasKind.QIYAS_ILLA
    assert qiyas.validity is QiyasValidity.VALID
    assert qiyas.asl == "الخمر"
    assert qiyas.far3 == "النبيذ"
    assert qiyas.illa == "الإسكار"
    assert qiyas.hukm_transferred != ""


def test_qiyas_rejects_unclosed_judgement():
    judgement = Judgement(closure=ClosureStatus.OPEN)
    qiyas, result = QiyasModel.build(
        judgement=judgement,
        asl="الخمر",
        far3="النبيذ",
        illa="الإسكار",
        kind=QiyasKind.QIYAS_ILLA,
    )
    assert result.verdict is GateVerdict.REJECT
    assert qiyas is None


def test_qiyas_rejects_no_asl():
    judgement = _make_closed_judgement()
    qiyas, result = QiyasModel.build(
        judgement=judgement,
        asl="",
        far3="النبيذ",
        illa="الإسكار",
        kind=QiyasKind.QIYAS_ILLA,
    )
    assert result.verdict is GateVerdict.REJECT
    assert qiyas is None


def test_qiyas_rejects_no_far3():
    judgement = _make_closed_judgement()
    qiyas, result = QiyasModel.build(
        judgement=judgement,
        asl="الخمر",
        far3="",
        illa="الإسكار",
        kind=QiyasKind.QIYAS_ILLA,
    )
    assert result.verdict is GateVerdict.REJECT
    assert qiyas is None


def test_qiyas_rejects_no_illa():
    judgement = _make_closed_judgement()
    qiyas, result = QiyasModel.build(
        judgement=judgement,
        asl="الخمر",
        far3="النبيذ",
        illa="",
        kind=QiyasKind.QIYAS_ILLA,
    )
    assert result.verdict is GateVerdict.REJECT
    assert qiyas is None


def test_qiyas_with_explicit_hukm():
    judgement = _make_closed_judgement()
    qiyas, result = QiyasModel.build(
        judgement=judgement,
        asl="الخمر",
        far3="النبيذ",
        illa="الإسكار",
        kind=QiyasKind.QIYAS_DALALA,
        hukm_transferred="التحريم",
    )
    assert result.passed
    assert qiyas is not None
    assert qiyas.hukm_transferred == "التحريم"
    assert qiyas.kind is QiyasKind.QIYAS_DALALA


def test_qiyas_preserves_confidence():
    judgement = _make_closed_judgement()
    judgement.semantic_confidence = 0.85
    qiyas, result = QiyasModel.build(
        judgement=judgement,
        asl="الأصل",
        far3="الفرع",
        illa="العلة",
        kind=QiyasKind.QIYAS_SHABAH,
    )
    assert result.passed
    assert qiyas is not None
    assert qiyas.confidence == 0.85


# ---------------------------------------------------------------------------
# QiyasTransitionEngine tests
# ---------------------------------------------------------------------------


def test_transition_rejects_no_judgement():
    qiyas = Qiyas()
    result = QiyasTransitionEngine.validate_transition(qiyas)
    assert result.verdict is GateVerdict.REJECT
    assert result.missing_condition == "judgement"


def test_transition_rejects_unclosed_judgement():
    qiyas = Qiyas(judgement=Judgement(closure=ClosureStatus.OPEN))
    result = QiyasTransitionEngine.validate_transition(qiyas)
    assert result.verdict is GateVerdict.REJECT
    assert result.missing_condition == "judgement_closed"


def test_transition_rejects_no_asl():
    judgement = _make_closed_judgement()
    qiyas = Qiyas(judgement=judgement, far3="فرع", illa="علة", kind=QiyasKind.QIYAS_ILLA)
    result = QiyasTransitionEngine.validate_transition(qiyas)
    assert result.verdict is GateVerdict.REJECT
    assert result.missing_condition == "asl"


def test_transition_rejects_no_far3():
    judgement = _make_closed_judgement()
    qiyas = Qiyas(judgement=judgement, asl="أصل", illa="علة", kind=QiyasKind.QIYAS_ILLA)
    result = QiyasTransitionEngine.validate_transition(qiyas)
    assert result.verdict is GateVerdict.REJECT
    assert result.missing_condition == "far3"


def test_transition_suspends_no_illa():
    judgement = _make_closed_judgement()
    qiyas = Qiyas(judgement=judgement, asl="أصل", far3="فرع", kind=QiyasKind.QIYAS_ILLA)
    result = QiyasTransitionEngine.validate_transition(qiyas)
    assert result.verdict is GateVerdict.SUSPEND
    assert result.missing_condition == "illa"


def test_transition_suspends_no_kind():
    judgement = _make_closed_judgement()
    qiyas = Qiyas(judgement=judgement, asl="أصل", far3="فرع", illa="علة")
    result = QiyasTransitionEngine.validate_transition(qiyas)
    assert result.verdict is GateVerdict.SUSPEND
    assert result.missing_condition == "qiyas_kind"


def test_transition_passes_complete():
    judgement = _make_closed_judgement()
    qiyas = Qiyas(
        judgement=judgement,
        asl="الخمر",
        far3="النبيذ",
        illa="الإسكار",
        kind=QiyasKind.QIYAS_ILLA,
    )
    result = QiyasTransitionEngine.validate_transition(qiyas)
    assert result.passed


# ---------------------------------------------------------------------------
# QiyasClosureEngine tests
# ---------------------------------------------------------------------------


def test_closure_closes_valid():
    judgement = _make_closed_judgement()
    qiyas = Qiyas(
        judgement=judgement,
        asl="الخمر",
        far3="النبيذ",
        illa="الإسكار",
        kind=QiyasKind.QIYAS_ILLA,
    )
    result = QiyasClosureEngine.close(qiyas)
    assert result.passed
    assert qiyas.closure is ClosureStatus.CLOSED


def test_closure_blocks_invalid():
    qiyas = Qiyas()
    result = QiyasClosureEngine.close(qiyas)
    assert result.verdict is GateVerdict.REJECT
    assert qiyas.closure is ClosureStatus.BLOCKED


def test_closure_suspends_incomplete():
    judgement = _make_closed_judgement()
    qiyas = Qiyas(
        judgement=judgement,
        asl="أصل",
        far3="فرع",
    )  # missing illa and kind
    result = QiyasClosureEngine.close(qiyas)
    assert result.verdict is GateVerdict.SUSPEND
    assert qiyas.closure is ClosureStatus.SUSPENDED
