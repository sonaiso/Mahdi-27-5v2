"""Tests for the Communicative module and its MasterChain integration."""

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import CommunicativeMode, Layer
from arabic_engine.core.enums_singular import (
    Definiteness,
    DerivationKind,
    Gender,
    StabilityKind,
    WordCategory,
)
from arabic_engine.core.enums_weight import InflectionKind, WeightEligibility
from arabic_engine.core.enums_judgement import (
    JudgementDirection,
    JudgementRank,
    QiyasKind,
)
from arabic_engine.core.types_singular import (
    PreU0,
    SingularConceptual,
    SingularInformational,
    SingularPerceptual,
    SingularUnit,
)
from arabic_engine.core.types_weight import WeightRecord, WeightedUnit
from arabic_engine.core.types_judgement import Proposition

from arabic_engine.singular.closure import SingularClosureEngine
from arabic_engine.weight.closure import WeightClosureEngine
from arabic_engine.composition.asnadi import AsnadiRelationBuilder
from arabic_engine.communicative.khabar_insha import KhabarInshaClassifier
from arabic_engine.communicative.closure import CommunicativeClosureEngine
from arabic_engine.communicative.stylistic import StylisticGate
from arabic_engine.runtime.master_chain import MasterChain
from arabic_engine.runtime.runtime_view import RuntimeView


# ---------------------------------------------------------------------------
# KhabarInshaClassifier tests
# ---------------------------------------------------------------------------


def test_classify_khabar():
    prop = Proposition(closure=ClosureStatus.CLOSED)
    result = KhabarInshaClassifier.classify(prop, CommunicativeMode.KHABAR)
    assert result.mode is CommunicativeMode.KHABAR
    assert result.reason != ""


def test_classify_insha():
    prop = Proposition(closure=ClosureStatus.CLOSED)
    result = KhabarInshaClassifier.classify(prop, CommunicativeMode.INSHA)
    assert result.mode is CommunicativeMode.INSHA


# ---------------------------------------------------------------------------
# StylisticGate tests
# ---------------------------------------------------------------------------


def test_stylistic_passes_with_mode():
    from arabic_engine.communicative.khabar_insha import CommunicativeResult
    result = StylisticGate.evaluate(CommunicativeResult(mode=CommunicativeMode.KHABAR))
    assert result.passed


def test_stylistic_suspends_without_mode():
    from arabic_engine.communicative.khabar_insha import CommunicativeResult
    result = StylisticGate.evaluate(CommunicativeResult())
    assert result.verdict is GateVerdict.SUSPEND


# ---------------------------------------------------------------------------
# CommunicativeClosureEngine tests
# ---------------------------------------------------------------------------


def test_communicative_closure():
    prop = Proposition(closure=ClosureStatus.CLOSED)
    comm_result, results = CommunicativeClosureEngine.close(prop, CommunicativeMode.KHABAR)
    assert comm_result.mode is CommunicativeMode.KHABAR
    assert all(r.passed for r in results)


# ---------------------------------------------------------------------------
# MasterChain integration — communicative
# ---------------------------------------------------------------------------


def _make_closed_weighted(
    word_cat: WordCategory = WordCategory.FI3L,
    pattern: str = "فَعَلَ",
    root: str = "ك ت ب",
) -> WeightedUnit:
    """Create a fully closed weighted unit."""
    unit = SingularUnit(
        pre_u0=PreU0(
            codepoint=0x0643, char="ك",
            is_present=True, is_distinguishable=True, is_admissible=True,
        ),
        perceptual=SingularPerceptual(
            sensory_trace="كتب", stability=StabilityKind.TRANSFORMING,
        ),
        informational=SingularInformational(
            prior_knowledge_bound=True, agency_potential=True,
            temporal_potential=True,
        ),
        conceptual=SingularConceptual(
            word_category=word_cat,
            definiteness=Definiteness.INDEFINITE,
            gender=Gender.MASCULINE,
            derivation=DerivationKind.MUSHTAQ,
        ),
    )
    SingularClosureEngine.close_all(unit)
    record = WeightRecord(
        eligibility=WeightEligibility.ELIGIBLE,
        pattern=pattern,
        root=root,
        inflection=InflectionKind.MU3RAB,
        derivation_legality=DerivationKind.MUSHTAQ,
        verb_eligible=(word_cat is WordCategory.FI3L),
        noun_eligible=(word_cat is WordCategory.ISM),
    )
    weighted = WeightedUnit(singular=unit, weight=record)
    WeightClosureEngine.close(weighted)
    return weighted


def test_master_chain_process_communicative():
    chain = MasterChain()

    # Process through proposition
    unit = SingularUnit(
        pre_u0=PreU0(
            codepoint=0x0643, char="ك",
            is_present=True, is_distinguishable=True, is_admissible=True,
        ),
        perceptual=SingularPerceptual(
            sensory_trace="كتب", stability=StabilityKind.TRANSFORMING,
        ),
        informational=SingularInformational(
            prior_knowledge_bound=True, agency_potential=True,
            temporal_potential=True,
        ),
        conceptual=SingularConceptual(
            word_category=WordCategory.FI3L,
            definiteness=Definiteness.INDEFINITE,
            gender=Gender.MASCULINE,
            derivation=DerivationKind.MUSHTAQ,
        ),
    )
    chain.process_singular(unit)

    weight = WeightRecord(
        eligibility=WeightEligibility.ELIGIBLE,
        pattern="فَعَلَ",
        root="ك ت ب",
        inflection=InflectionKind.MU3RAB,
        derivation_legality=DerivationKind.MUSHTAQ,
        verb_eligible=True,
    )
    chain.process_weight(weight)

    u2 = _make_closed_weighted(WordCategory.ISM, "فاعِل", "ك ت ب")
    rel, _ = AsnadiRelationBuilder.build(u2, chain.state.weighted)
    chain.process_composition([rel])
    chain.process_proposition()

    # Now process communicative
    results = chain.process_communicative(CommunicativeMode.KHABAR)
    assert all(r.passed for r in results)
    assert chain.state.communicative_result is not None
    assert chain.state.communicative_result.mode is CommunicativeMode.KHABAR


def test_master_chain_communicative_rejects_without_proposition():
    chain = MasterChain()
    results = chain.process_communicative(CommunicativeMode.KHABAR)
    assert results[0].verdict is GateVerdict.REJECT


def test_master_chain_full_pipeline_with_qiyas_and_language():
    """Full pipeline: singular → weight → composition → proposition →
    judgement → qiyas → language."""
    chain = MasterChain()

    # Step 1: Singular
    unit = SingularUnit(
        pre_u0=PreU0(
            codepoint=0x0643, char="ك",
            is_present=True, is_distinguishable=True, is_admissible=True,
        ),
        perceptual=SingularPerceptual(
            sensory_trace="كتب", stability=StabilityKind.TRANSFORMING,
        ),
        informational=SingularInformational(
            prior_knowledge_bound=True, agency_potential=True,
            temporal_potential=True,
        ),
        conceptual=SingularConceptual(
            word_category=WordCategory.FI3L,
            definiteness=Definiteness.INDEFINITE,
            gender=Gender.MASCULINE,
            derivation=DerivationKind.MUSHTAQ,
        ),
    )
    results = chain.process_singular(unit)
    assert all(r.passed for r in results)

    # Step 2: Weight
    weight = WeightRecord(
        eligibility=WeightEligibility.ELIGIBLE,
        pattern="فَعَلَ",
        root="ك ت ب",
        inflection=InflectionKind.MU3RAB,
        derivation_legality=DerivationKind.MUSHTAQ,
        verb_eligible=True,
    )
    results = chain.process_weight(weight)
    assert all(r.passed for r in results)

    # Step 3: Composition
    u2 = _make_closed_weighted(WordCategory.ISM, "فاعِل", "ك ت ب")
    rel, _ = AsnadiRelationBuilder.build(u2, chain.state.weighted)
    results = chain.process_composition([rel])
    assert all(r.passed for r in results)

    # Step 4: Proposition
    result = chain.process_proposition()
    assert result.passed

    # Step 5: Communicative (cross-cutting)
    results = chain.process_communicative(CommunicativeMode.KHABAR)
    assert all(r.passed for r in results)

    # Step 6: Judgement
    result = chain.process_judgement(
        direction=JudgementDirection.AFFIRMATION,
        rank=JudgementRank.CERTAIN,
        subject="الطالب",
        criterion="الإسناد",
        reason="كَتَبَ الطالبُ — إسناد صحيح",
    )
    assert result.passed

    # Step 7: Qiyas (Layer 8)
    result = chain.process_qiyas(
        asl="الكتابة بالقلم",
        far3="الكتابة بالحاسوب",
        illa="إنتاج النص المكتوب",
        kind=QiyasKind.QIYAS_ILLA,
    )
    assert result.passed
    assert chain.state.qiyas is not None
    assert chain.state.qiyas.closure is ClosureStatus.CLOSED

    # Step 8: Language (Layer 9)
    results = chain.process_language()
    assert all(r.passed for r in results)

    # Verify runtime view
    snapshot = RuntimeView.snapshot(chain)
    assert snapshot.singular_closed
    assert snapshot.weight_closed
    assert snapshot.judgement_closed
    assert snapshot.qiyas_closed
    assert snapshot.language_closed


def test_master_chain_qiyas_rejects_before_judgement():
    chain = MasterChain()
    result = chain.process_qiyas(
        asl="الأصل",
        far3="الفرع",
        illa="العلة",
        kind=QiyasKind.QIYAS_ILLA,
    )
    assert result.verdict is GateVerdict.REJECT
