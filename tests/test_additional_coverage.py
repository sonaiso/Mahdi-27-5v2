"""Additional targeted tests to improve branch coverage in low-covered modules."""

from arabic_engine.composition.tadmini import TadminiRelationBuilder
from arabic_engine.composition.taqyidi import TaqyidiRelationBuilder
from arabic_engine.judgement.transition import JudgementTransitionEngine
from arabic_engine.proposition.closure import PropositionClosureEngine
from arabic_engine.singular.concept import ConceptGate
from arabic_engine.singular.information import InformationGate

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import RelationKind, RoleTag
from arabic_engine.core.enums_judgement import JudgementDirection, JudgementRank
from arabic_engine.core.enums_singular import Definiteness, DerivationKind, Gender, WordCategory
from arabic_engine.core.types_singular import (
    PreU0,
    SingularConceptual,
    SingularInformational,
    SingularPerceptual,
    SingularUnit,
)
from arabic_engine.core.types_weight import WeightRecord, WeightedUnit
from arabic_engine.core.types_judgement import Judgement, Proposition


def _make_weighted(closed: bool = True) -> WeightedUnit:
    status = ClosureStatus.CLOSED if closed else ClosureStatus.OPEN
    singular = SingularUnit(
        pre_u0=PreU0(closure=status),
        perceptual=SingularPerceptual(closure=status),
        informational=SingularInformational(closure=status),
        conceptual=SingularConceptual(closure=status),
    )
    weight = WeightRecord(closure=status)
    return WeightedUnit(singular=singular, weight=weight)


def test_tadmini_builder_builds_closed_relation_with_default_hal_role():
    relation, results = TadminiRelationBuilder.build(_make_weighted(), _make_weighted())

    assert relation is not None
    assert all(r.passed for r in results)
    assert relation.kind is RelationKind.TADMINI
    assert relation.closure is ClosureStatus.CLOSED
    assert relation.roles[1].role is RoleTag.HAL


def test_tadmini_builder_returns_none_when_contained_unit_is_unclosed():
    relation, results = TadminiRelationBuilder.build(_make_weighted(), _make_weighted(closed=False))

    assert relation is None
    assert len(results) == 2
    assert results[-1].verdict is GateVerdict.REJECT
    assert results[-1].missing_condition in {"singular_closed", "weight_closed"}


def test_taqyidi_idafa_builder_assigns_mudaf_and_mudaf_ilayh_roles():
    relation, results = TaqyidiRelationBuilder.build_idafa(_make_weighted(), _make_weighted())

    assert relation is not None
    assert all(r.passed for r in results)
    assert relation.kind is RelationKind.TAQYIDI
    assert relation.roles[0].role is RoleTag.MUDAF
    assert relation.roles[1].role is RoleTag.MUDAF_ILAYH


def test_taqyidi_sifa_builder_assigns_mawsuf_and_sifa_roles():
    relation, results = TaqyidiRelationBuilder.build_sifa(_make_weighted(), _make_weighted())

    assert relation is not None
    assert all(r.passed for r in results)
    assert relation.kind is RelationKind.TAQYIDI
    assert relation.roles[0].role is RoleTag.MAWSUF
    assert relation.roles[1].role is RoleTag.SIFA


def test_taqyidi_sifa_builder_returns_none_if_first_unit_invalid():
    relation, results = TaqyidiRelationBuilder.build_sifa(_make_weighted(closed=False), _make_weighted())

    assert relation is None
    assert len(results) == 1
    assert results[0].verdict is GateVerdict.REJECT


def test_proposition_closure_passes_for_closed_non_empty_proposition():
    prop = Proposition(relations=[object()], closure=ClosureStatus.CLOSED)
    result = PropositionClosureEngine.evaluate(prop)
    assert result.passed


def test_proposition_closure_rejects_open_or_empty_proposition():
    open_prop = Proposition(relations=[object()], closure=ClosureStatus.OPEN)
    empty_prop = Proposition(relations=[], closure=ClosureStatus.CLOSED)

    open_result = PropositionClosureEngine.evaluate(open_prop)
    empty_result = PropositionClosureEngine.evaluate(empty_prop)

    assert open_result.verdict is GateVerdict.REJECT
    assert empty_result.verdict is GateVerdict.REJECT
    assert open_result.missing_condition == "proposition_closure"
    assert empty_result.missing_condition == "proposition_closure"


def test_judgement_transition_covers_all_failure_branches_and_pass():
    base_closed_prop = Proposition(relations=[object()], closure=ClosureStatus.CLOSED)

    no_prop = Judgement()
    open_prop = Judgement(proposition=Proposition(closure=ClosureStatus.OPEN))
    no_direction = Judgement(proposition=base_closed_prop, rank=JudgementRank.CERTAIN, subject="s", criterion="c")
    no_rank = Judgement(
        proposition=base_closed_prop,
        direction=JudgementDirection.AFFIRMATION,
        subject="s",
        criterion="c",
    )
    no_subject = Judgement(
        proposition=base_closed_prop,
        direction=JudgementDirection.AFFIRMATION,
        rank=JudgementRank.CERTAIN,
        criterion="c",
    )
    no_criterion = Judgement(
        proposition=base_closed_prop,
        direction=JudgementDirection.AFFIRMATION,
        rank=JudgementRank.CERTAIN,
        subject="s",
    )
    complete = Judgement(
        proposition=base_closed_prop,
        direction=JudgementDirection.AFFIRMATION,
        rank=JudgementRank.CERTAIN,
        subject="s",
        criterion="c",
    )

    assert JudgementTransitionEngine.validate_transition(no_prop).missing_condition == "proposition"
    assert JudgementTransitionEngine.validate_transition(open_prop).missing_condition == "proposition_closed"
    assert JudgementTransitionEngine.validate_transition(no_direction).missing_condition == "direction"
    assert JudgementTransitionEngine.validate_transition(no_rank).missing_condition == "rank"
    assert JudgementTransitionEngine.validate_transition(no_subject).missing_condition == "subject"
    assert JudgementTransitionEngine.validate_transition(no_criterion).missing_condition == "criterion"
    assert JudgementTransitionEngine.validate_transition(complete).passed


def test_information_gate_close_sets_blocked_suspended_and_closed_states():
    blocked = SingularInformational(prior_knowledge_bound=False)
    suspended = SingularInformational(prior_knowledge_bound=True)
    closed = SingularInformational(prior_knowledge_bound=True, agency_potential=True)

    InformationGate.close(blocked)
    InformationGate.close(suspended)
    InformationGate.close(closed)

    assert blocked.closure is ClosureStatus.BLOCKED
    assert suspended.closure is ClosureStatus.SUSPENDED
    assert closed.closure is ClosureStatus.CLOSED


def test_concept_gate_close_sets_blocked_suspended_and_closed_states():
    blocked = SingularConceptual()
    suspended = SingularConceptual(word_category=WordCategory.ISM)
    closed = SingularConceptual(
        word_category=WordCategory.ISM,
        definiteness=Definiteness.DEFINITE,
        gender=Gender.MASCULINE,
        derivation=DerivationKind.MUSHTAQ,
    )

    ConceptGate.close(blocked)
    ConceptGate.close(suspended)
    ConceptGate.close(closed)

    assert blocked.closure is ClosureStatus.BLOCKED
    assert suspended.closure is ClosureStatus.SUSPENDED
    assert closed.closure is ClosureStatus.CLOSED
