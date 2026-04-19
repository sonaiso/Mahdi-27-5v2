"""Tests for composition, proposition, judgement, and the full master chain."""

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_singular import (
    Definiteness,
    DerivationKind,
    Gender,
    StabilityKind,
    WordCategory,
)
from arabic_engine.core.enums_weight import InflectionKind, WeightEligibility
from arabic_engine.core.enums_domain import RelationKind, RoleTag, CommunicativeMode
from arabic_engine.core.enums_judgement import JudgementDirection, JudgementRank
from arabic_engine.core.types_singular import (
    PreU0,
    SingularConceptual,
    SingularInformational,
    SingularPerceptual,
    SingularUnit,
)
from arabic_engine.core.types_weight import WeightRecord, WeightedUnit
from arabic_engine.core.types_composition import CompositionRelation, RoleAssignment

from arabic_engine.singular.closure import SingularClosureEngine
from arabic_engine.weight.closure import WeightClosureEngine
from arabic_engine.composition.roles import CompositionEligibilityGate
from arabic_engine.composition.asnadi import AsnadiRelationBuilder
from arabic_engine.proposition.structure import PropositionBuilder
from arabic_engine.judgement.model import JudgementModel
from arabic_engine.runtime.master_chain import MasterChain
from arabic_engine.runtime.runtime_view import RuntimeView
from arabic_engine.runtime.proof_view import ProofView


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
    assert unit.singular_closed

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
    assert weighted.fully_closed
    return weighted


# ---------------------------------------------------------------------------
# Composition tests
# ---------------------------------------------------------------------------


def test_composition_eligibility_rejects_unclosed():
    unit = WeightedUnit()  # unclosed
    result = CompositionEligibilityGate.evaluate(unit)
    assert result.verdict is GateVerdict.REJECT


def test_composition_eligibility_passes_closed():
    unit = _make_closed_weighted()
    result = CompositionEligibilityGate.evaluate(unit)
    assert result.passed


def test_asnadi_builds_relation():
    musnad_ilayh = _make_closed_weighted(WordCategory.ISM, "فاعِل", "ك ت ب")
    musnad = _make_closed_weighted(WordCategory.FI3L, "فَعَلَ", "ك ت ب")
    rel, results = AsnadiRelationBuilder.build(musnad_ilayh, musnad)
    assert rel is not None
    assert rel.kind is RelationKind.ASNADI
    assert rel.closure is ClosureStatus.CLOSED
    assert len(rel.roles) == 2


def test_asnadi_fails_with_unclosed_unit():
    good = _make_closed_weighted()
    bad = WeightedUnit()
    rel, results = AsnadiRelationBuilder.build(bad, good)
    assert rel is None
    assert any(not r.passed for r in results)


# ---------------------------------------------------------------------------
# Proposition tests
# ---------------------------------------------------------------------------


def test_proposition_builds_from_closed_relations():
    u1 = _make_closed_weighted(WordCategory.ISM, "فاعِل", "ك ت ب")
    u2 = _make_closed_weighted(WordCategory.FI3L, "فَعَلَ", "ك ت ب")
    rel, _ = AsnadiRelationBuilder.build(u1, u2)
    assert rel is not None

    prop, result = PropositionBuilder.build([rel])
    assert result.passed
    assert prop is not None
    assert prop.closure is ClosureStatus.CLOSED


def test_proposition_rejects_empty():
    prop, result = PropositionBuilder.build([])
    assert result.verdict is GateVerdict.REJECT


# ---------------------------------------------------------------------------
# Judgement tests
# ---------------------------------------------------------------------------


def test_judgement_builds_from_closed_proposition():
    u1 = _make_closed_weighted(WordCategory.ISM, "فاعِل", "ك ت ب")
    u2 = _make_closed_weighted(WordCategory.FI3L, "فَعَلَ", "ك ت ب")
    rel, _ = AsnadiRelationBuilder.build(u1, u2)
    prop, _ = PropositionBuilder.build([rel])

    judgement, result = JudgementModel.build(
        proposition=prop,
        direction=JudgementDirection.AFFIRMATION,
        rank=JudgementRank.CERTAIN,
        subject="الكاتب",
        criterion="الفعل والفاعل",
        reason="إسناد صحيح",
    )
    assert result.passed
    assert judgement is not None
    assert judgement.closure is ClosureStatus.CLOSED


def test_judgement_rejects_no_subject():
    u1 = _make_closed_weighted(WordCategory.ISM, "فاعِل", "ك ت ب")
    u2 = _make_closed_weighted(WordCategory.FI3L, "فَعَلَ", "ك ت ب")
    rel, _ = AsnadiRelationBuilder.build(u1, u2)
    prop, _ = PropositionBuilder.build([rel])

    judgement, result = JudgementModel.build(
        proposition=prop,
        direction=JudgementDirection.AFFIRMATION,
        rank=JudgementRank.CERTAIN,
        subject="",
        criterion="test",
    )
    assert result.verdict is GateVerdict.REJECT
    assert judgement is None


# ---------------------------------------------------------------------------
# Master chain integration tests
# ---------------------------------------------------------------------------


def test_master_chain_full_pipeline():
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

    # Step 3: Composition — need a second unit for asnadi
    unit2 = SingularUnit(
        pre_u0=PreU0(
            codepoint=0x0627, char="ا",
            is_present=True, is_distinguishable=True, is_admissible=True,
        ),
        perceptual=SingularPerceptual(
            sensory_trace="طالب", stability=StabilityKind.STABLE,
        ),
        informational=SingularInformational(
            prior_knowledge_bound=True, agency_potential=True,
        ),
        conceptual=SingularConceptual(
            word_category=WordCategory.ISM,
            definiteness=Definiteness.DEFINITE,
            gender=Gender.MASCULINE,
            derivation=DerivationKind.MUSHTAQ,
        ),
    )
    SingularClosureEngine.close_all(unit2)
    weight2 = WeightRecord(
        eligibility=WeightEligibility.ELIGIBLE,
        pattern="فاعِل",
        root="ط ل ب",
        inflection=InflectionKind.MU3RAB,
        derivation_legality=DerivationKind.MUSHTAQ,
        noun_eligible=True,
    )
    weighted2 = WeightedUnit(singular=unit2, weight=weight2)
    WeightClosureEngine.close(weighted2)
    assert weighted2.fully_closed

    # Build relation using chain's weighted unit
    rel, rel_results = AsnadiRelationBuilder.build(weighted2, chain.state.weighted)
    assert rel is not None
    assert all(r.passed for r in rel_results)

    results = chain.process_composition([rel])
    assert all(r.passed for r in results)

    # Step 4: Proposition
    result = chain.process_proposition()
    assert result.passed

    # Step 5: Judgement
    result = chain.process_judgement(
        direction=JudgementDirection.AFFIRMATION,
        rank=JudgementRank.CERTAIN,
        subject="الطالب",
        criterion="الإسناد",
        reason="كَتَبَ الطالبُ — إسناد صحيح",
    )
    assert result.passed

    # Verify runtime view
    snapshot = RuntimeView.snapshot(chain)
    assert snapshot.singular_closed
    assert snapshot.weight_closed
    assert snapshot.judgement_closed

    # Verify proof view
    proof = ProofView.generate(chain)
    assert len(proof) > 0

    trace_summary = ProofView.generate_trace_summary(chain)
    assert len(trace_summary) > 0


def test_master_chain_rejects_weight_before_singular():
    chain = MasterChain()
    weight = WeightRecord(
        eligibility=WeightEligibility.ELIGIBLE,
        inflection=InflectionKind.MU3RAB,
        derivation_legality=DerivationKind.MUSHTAQ,
        verb_eligible=True,
    )
    results = chain.process_weight(weight)
    assert results[0].verdict is GateVerdict.REJECT
