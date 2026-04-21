"""Tests for Σ1 -> Σ2 reference-predication transition models."""

from dataclasses import replace
import warnings

import pytest

from arabic_engine.reference_predication import (
    GrammaticalFactorGI,
    GrammaticalRole,
    LegacySigma1ReferenceUnit,
    MentalFactor,
    OntologyClass,
    PositionalPotential,
    PredicationType,
    PropositionMode,
    PropositionConstraintVector,
    RatioVector,
    SentenceSpace,
    SigmaCompatibilityAdapter,
    Sigma1ReferenceUnit,
    Sigma1Thresholds,
    Sigma2Builder,
    SigmaPrerequisiteChecker,
    SigmaTransitionError,
    THRESHOLD_BUNDLE_V1,
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
    with warnings.catch_warnings(record=True) as recorded:
        warnings.simplefilter("always")
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
    assert isinstance(s2.grammatical_factor, GrammaticalFactorGI)
    assert any(issubclass(w.category, DeprecationWarning) for w in recorded)
    assert any(
        "Passing string grammatical_factor is deprecated" in str(w.message)
        for w in recorded
    )


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
    g_i = GrammaticalFactorGI(
        code="G_i",
        ontology_anchor=OntologyClass.ENTITY,
        causality_score=0.8,
        ego_mode=_admissible_sigma1("x").ego_reference,
        generality=_admissible_sigma1("x").generality,
        role=GrammaticalRole.SUBJECT,
        positional_validity=0.9,
    )
    s2 = Sigma2Builder.build(
        _admissible_sigma1("a"),
        _admissible_sigma1("b"),
        sentence_space=space,
        mental_factor=MentalFactor.MOD,
        grammatical_factor=g_i,
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


def test_legacy_sigma1_adapter_converts_to_expanded_sigma1():
    legacy = LegacySigma1ReferenceUnit(
        label="legacy",
        j_p=0.9,
        j_m=0.9,
        j_sigma=0.9,
        transition_capacity_nu=0.9,
        reference_variance=0.05,
        type_potential=TypePotential(noun=0.8, verb=0.2, particle=0.1),
        positional_potential=PositionalPotential(
            subject=0.9,
            predicate=0.8,
            qualifier=0.4,
            relator=0.3,
            transformer=0.2,
        ),
        purity_score=0.9,
    )
    expanded = SigmaCompatibilityAdapter.legacy_sigma1_to_expanded(legacy)
    assert isinstance(expanded, Sigma1ReferenceUnit)
    assert expanded.label == "legacy"


def test_sigma2_builder_rejects_when_j_m_fails_explicit_invariant():
    first = replace(_admissible_sigma1("u1"), j_m=0.1)
    with pytest.raises(SigmaTransitionError, match="J_m"):
        Sigma2Builder.build(
            first,
            _admissible_sigma1("u2"),
            sentence_space=SentenceSpace.KHABAR,
            mental_factor=MentalFactor.PRED,
            grammatical_factor="G_pred",
            ratios=RatioVector(asnadi=0.7, tadmini=0.2, taqyidi=0.1),
            proposition_constraint=_cp(),
        )


def test_sigma2_builder_rejects_inconsistent_structured_gi():
    invalid_gi = GrammaticalFactorGI(
        code="G_bad",
        ontology_anchor=OntologyClass.ENTITY,
        causality_score=0.5,
        ego_mode=_admissible_sigma1("x").ego_reference,
        generality=_admissible_sigma1("x").generality,
        role=GrammaticalRole.SUBJECT,
        positional_validity=0.1,
    )
    with pytest.raises(SigmaTransitionError, match="positional eligibility"):
        Sigma2Builder.build(
            _admissible_sigma1("u1"),
            _admissible_sigma1("u2"),
            sentence_space=SentenceSpace.KHABAR,
            mental_factor=MentalFactor.PRED,
            grammatical_factor=invalid_gi,
            ratios=RatioVector(asnadi=0.7, tadmini=0.2, taqyidi=0.1),
            proposition_constraint=_cp(),
        )


def test_sigma2_builder_rejects_causal_case_contradiction():
    first = replace(_admissible_sigma1("u1"), causality=0.0)
    second = replace(_admissible_sigma1("u2"), causality=0.0)
    with pytest.raises(SigmaTransitionError, match="causal structure"):
        Sigma2Builder.build(
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


def test_sigma2_builder_rejects_unstable_reference_in_fixed_khabar():
    first = replace(_admissible_sigma1("u1"), reference_variance=0.12)
    second = replace(_admissible_sigma1("u2"), reference_variance=0.05)
    with pytest.raises(SigmaTransitionError, match="Unstable reference"):
        Sigma2Builder.build(
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


def test_sigma2_threshold_bundle_v1_is_locked_for_cycle():
    assert THRESHOLD_BUNDLE_V1.theta_sigma1 == 0.70
    assert THRESHOLD_BUNDLE_V1.theta_p == 0.70
    assert THRESHOLD_BUNDLE_V1.theta_m == 0.70
    assert THRESHOLD_BUNDLE_V1.theta_t == 0.55
    assert THRESHOLD_BUNDLE_V1.theta_l == 0.55
    assert THRESHOLD_BUNDLE_V1.theta_purity == 0.70
    assert THRESHOLD_BUNDLE_V1.theta_nu == 0.65
    assert THRESHOLD_BUNDLE_V1.epsilon_rho == 0.20
    assert THRESHOLD_BUNDLE_V1.theta_gi == 0.60
    assert THRESHOLD_BUNDLE_V1.theta_i2_causal_alignment == 0.50
    assert THRESHOLD_BUNDLE_V1.theta_i2_referential_alignment == 0.50


def test_sigma2_builder_rejects_referential_alignment_failure():
    first = replace(_admissible_sigma1("u1"), association=0.0)
    second = replace(_admissible_sigma1("u2"), association=1.0)
    with pytest.raises(SigmaTransitionError, match="referential alignment"):
        Sigma2Builder.build(
            first,
            second,
            sentence_space=SentenceSpace.COND,
            mental_factor=MentalFactor.COND,
            grammatical_factor="G_cond",
            ratios=RatioVector(asnadi=0.7, tadmini=0.2, taqyidi=0.1),
            proposition_constraint=_cp(),
        )
