"""Tests for the stable, independent reference-predication interface."""

from dataclasses import replace

import pytest

from arabic_engine.core.enums_trace import TraceEventKind
from arabic_engine.reference_predication import (
    MentalFactor,
    OntologyClass,
    PositionalPotential,
    PropositionConstraintVector,
    RatioVector,
    ReferencePredicationInterface,
    SentenceSpace,
    Sigma1ReferenceUnit,
    Sigma2Builder,
    SigmaTransitionError,
    TypePotential,
)


def _admissible_sigma1(label: str) -> Sigma1ReferenceUnit:
    return Sigma1ReferenceUnit(
        label=label,
        j_p=0.92,
        j_m=0.90,
        j_sigma=0.91,
        transition_capacity_nu=0.89,
        reference_variance=0.05,
        type_potential=TypePotential(noun=0.8, verb=0.3, particle=0.2),
        positional_potential=PositionalPotential(
            subject=0.9,
            predicate=0.8,
            qualifier=0.5,
            relator=0.4,
            transformer=0.3,
        ),
        purity_score=0.94,
        ontology=OntologyClass.ENTITY,
    )


def _cp() -> PropositionConstraintVector:
    return PropositionConstraintVector(
        khabari=1.0,
        conditional=0.0,
        insha_talabi_or_istifhami=0.0,
        naskh=0.0,
        emphatic_or_istidraki=0.0,
        proximative_or_inceptive_or_hopeful=0.0,
        connective_or_referential=0.0,
    )


def test_interface_skips_when_feature_flag_disabled():
    interface = ReferencePredicationInterface(enabled=False)
    result = interface.build_sigma2(
        _admissible_sigma1("subj"),
        _admissible_sigma1("pred"),
        sentence_space=SentenceSpace.KHABAR,
        mental_factor=MentalFactor.PRED,
        grammatical_factor="G_pred",
        ratios=RatioVector(asnadi=0.8, tadmini=0.1, taqyidi=0.1),
        proposition_constraint=_cp(),
    )
    assert result.skipped
    assert result.matrix is None
    assert "feature flag disabled" in result.skip_reason
    assert any(
        e.kind is TraceEventKind.CLOSURE_CHANGE and "skipped" in e.reason
        for e in interface.tracer.log.events
    )


def test_interface_builds_sigma2_when_enabled():
    interface = ReferencePredicationInterface(enabled=True)
    result = interface.build_sigma2(
        _admissible_sigma1("subj"),
        _admissible_sigma1("pred"),
        sentence_space=SentenceSpace.KHABAR,
        mental_factor=MentalFactor.PRED,
        grammatical_factor="G_pred",
        ratios=RatioVector(asnadi=0.8, tadmini=0.1, taqyidi=0.1),
        proposition_constraint=_cp(),
    )
    assert not result.skipped
    assert result.enabled
    assert result.matrix is not None
    assert result.matrix.sentence_space is SentenceSpace.KHABAR


def test_interface_threshold_behavior_allows_boundary_value():
    interface = ReferencePredicationInterface(enabled=True)
    # Fixed-khabar stability threshold is epsilon_rho / 2 = 0.1 by default.
    first = replace(_admissible_sigma1("u1"), reference_variance=0.1)
    second = replace(_admissible_sigma1("u2"), reference_variance=0.1)
    result = interface.build_sigma2(
        first,
        second,
        sentence_space=SentenceSpace.KHABAR,
        mental_factor=MentalFactor.PRED,
        grammatical_factor="G_pred",
        ratios=RatioVector(asnadi=0.7, tadmini=0.2, taqyidi=0.1),
        proposition_constraint=_cp(),
        subject_mark="raf",
        predicate_mark="raf",
    )
    assert result.matrix is not None


def test_interface_failure_mode_traces_and_raises():
    interface = ReferencePredicationInterface(enabled=True)
    with pytest.raises(SigmaTransitionError):
        interface.build_sigma2(
            _admissible_sigma1("u1"),
            _admissible_sigma1("u2"),
            sentence_space=SentenceSpace.KHABAR,
            mental_factor=MentalFactor.PRED,
            grammatical_factor="G_pred",
            ratios=RatioVector(asnadi=0.9, tadmini=0.2, taqyidi=0.1),
            proposition_constraint=_cp(),
        )
    assert any(e.kind is TraceEventKind.REJECTION for e in interface.tracer.log.events)


def test_interface_regression_matches_direct_builder_output():
    first = _admissible_sigma1("subj")
    second = _admissible_sigma1("pred")
    kwargs = dict(
        sentence_space=SentenceSpace.KHABAR,
        mental_factor=MentalFactor.PRED,
        grammatical_factor="G_pred",
        ratios=RatioVector(asnadi=0.8, tadmini=0.1, taqyidi=0.1),
        proposition_constraint=_cp(),
    )
    direct = Sigma2Builder.build(first, second, **kwargs)
    through_interface = ReferencePredicationInterface(enabled=True).build_sigma2(
        first, second, **kwargs
    )
    assert through_interface.matrix == direct
