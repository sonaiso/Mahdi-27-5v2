"""Tests for Σ1 -> Σ2 reference-predication transition models."""

from dataclasses import replace

import pytest

from arabic_engine.reference_predication import (
    MentalFactor,
    PositionalPotential,
    PredicationType,
    PropositionMode,
    PropositionConstraintVector,
    RatioVector,
    SentenceSpace,
    Sigma1ReferenceUnit,
    Sigma1Thresholds,
    Sigma2Builder,
    SigmaPrerequisiteChecker,
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


def test_ratio_vector_probability_mode_validates_sum_one():
    assert RatioVector(asnadi=0.7, tadmini=0.2, taqyidi=0.1).is_valid()
    assert not RatioVector(asnadi=0.7, tadmini=0.2, taqyidi=0.2).is_valid()


def test_ratio_vector_independent_mode_skips_sum_constraint():
    assert RatioVector(
        asnadi=0.7,
        tadmini=0.2,
        taqyidi=0.2,
        independent=True,
    ).is_valid()


def test_sigma1_prerequisite_checker_reports_admissible_unit():
    report = SigmaPrerequisiteChecker.evaluate(
        _admissible_sigma1("u1"),
        Sigma1Thresholds(),
    )
    assert report.is_admissible


def test_sigma1_prerequisite_checker_detects_reference_stability_gap():
    unit = _admissible_sigma1("u1")
    unit = replace(unit, reference_variance=0.9)
    report = SigmaPrerequisiteChecker.evaluate(unit, Sigma1Thresholds())
    assert not report.passes_reference_stability
    assert not report.is_admissible


def test_sigma2_builder_builds_khabar_matrix_defaults():
    s2 = Sigma2Builder.build(
        _admissible_sigma1("subj"),
        _admissible_sigma1("pred"),
        sentence_space=SentenceSpace.KHABAR,
        mental_factor=MentalFactor.PRED,
        grammatical_factor="G_pred",
        ratios=RatioVector(asnadi=0.8, tadmini=0.1, taqyidi=0.1),
        proposition_constraint=_cp(),
    )
    assert s2.reference_predication.chi is PredicationType.PRED
    assert s2.reference_predication.zeta is PropositionMode.KHABAR


def test_sigma2_builder_builds_conditional_matrix_defaults():
    s2 = Sigma2Builder.build(
        _admissible_sigma1("protasis"),
        _admissible_sigma1("apodosis"),
        sentence_space=SentenceSpace.COND,
        mental_factor=MentalFactor.COND,
        grammatical_factor="G_cond",
        ratios=RatioVector(asnadi=0.5, tadmini=0.2, taqyidi=0.3),
        proposition_constraint=_cp(),
    )
    assert s2.reference_predication.chi is PredicationType.COND
    assert s2.reference_predication.zeta is PropositionMode.INSHA


@pytest.mark.parametrize(
    "space,chi,zeta",
    [
        (SentenceSpace.NASKH, PredicationType.NASKH, PropositionMode.KHABAR),
        (SentenceSpace.INSHA, PredicationType.INSHA, PropositionMode.INSHA),
    ],
)
def test_sigma2_builder_space_mapping(space, chi, zeta):
    s2 = Sigma2Builder.build(
        _admissible_sigma1("a"),
        _admissible_sigma1("b"),
        sentence_space=space,
        mental_factor=MentalFactor.MOD,
        grammatical_factor="G_i",
        ratios=RatioVector(asnadi=0.6, tadmini=0.2, taqyidi=0.2),
        proposition_constraint=_cp(),
    )
    assert s2.reference_predication.chi is chi
    assert s2.reference_predication.zeta is zeta


def test_sigma2_builder_rejects_non_admissible_sigma1():
    bad = Sigma1ReferenceUnit(
        label="bad",
        j_p=0.2,
        j_m=0.2,
        j_sigma=0.2,
        transition_capacity_nu=0.1,
        reference_variance=0.9,
        type_potential=TypePotential(noun=0.2, verb=0.2, particle=0.2),
        positional_potential=PositionalPotential(
            subject=0.1, predicate=0.1, qualifier=0.1, relator=0.1, transformer=0.1,
        ),
        purity_score=0.1,
    )

    with pytest.raises(SigmaTransitionError):
        Sigma2Builder.build(
            bad,
            _admissible_sigma1("good"),
            sentence_space=SentenceSpace.KHABAR,
            mental_factor=MentalFactor.PRED,
            grammatical_factor="G_pred",
            ratios=RatioVector(asnadi=0.7, tadmini=0.2, taqyidi=0.1),
            proposition_constraint=_cp(),
        )


def test_sigma2_builder_rejects_invalid_ratio_vector():
    with pytest.raises(SigmaTransitionError):
        Sigma2Builder.build(
            _admissible_sigma1("u1"),
            _admissible_sigma1("u2"),
            sentence_space=SentenceSpace.KHABAR,
            mental_factor=MentalFactor.PRED,
            grammatical_factor="G_pred",
            ratios=RatioVector(asnadi=0.9, tadmini=0.2, taqyidi=0.1),
            proposition_constraint=_cp(),
        )
