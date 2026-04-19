"""Tests for all new semantic kernel functionality (Phases 1-5).

Covers:
- Phase 1: Correctness fixes (conditional persistence, consistency checks,
  graceful degradation, constant cleanup)
- Phase 2: Architecture improvements (cosine-similarity, alignment,
  context delta, weight scheduler)
- Phase 3: Data expansion (expanded seeds, phonotactics)
- Phase 4: Robustness (ClosureTrace, metrics, Pareto-optimal)
- Phase 5: Integration (auto-chain, composition, judgement propagation)
"""

import pytest

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_singular import (
    Definiteness,
    DerivationKind,
    Gender,
    StabilityKind,
    WordCategory,
)
from arabic_engine.core.enums_weight import InflectionKind, WeightEligibility
from arabic_engine.core.enums_domain import RelationKind, RoleTag
from arabic_engine.core.enums_judgement import JudgementDirection, JudgementRank
from arabic_engine.core.types_singular import (
    PreU0,
    SingularConceptual,
    SingularInformational,
    SingularPerceptual,
    SingularUnit,
)
from arabic_engine.core.types_weight import WeightRecord, WeightedUnit
from arabic_engine.core.types_semantic import SemanticVector
from arabic_engine.core.types_composition import CompositionRelation, RoleAssignment
from arabic_engine.core.types_judgement import Proposition, Judgement

from arabic_engine.singular.closure import SingularClosureEngine
from arabic_engine.weight.closure import WeightClosureEngine
from arabic_engine.weight.mizan import MizanClassifier
from arabic_engine.composition.asnadi import AsnadiRelationBuilder
from arabic_engine.runtime.master_chain import MasterChain

from arabic_engine.semantic_kernel.root_kernel import RootKernelBuilder
from arabic_engine.semantic_kernel.pattern_transform import PatternTransformBuilder
from arabic_engine.semantic_kernel.form_profile import FormProfileBuilder
from arabic_engine.semantic_kernel.transfer import SemanticTransferEngine
from arabic_engine.semantic_kernel.compatibility import CompatibilityChecker
from arabic_engine.semantic_kernel.economy import EconomyOptimizer
from arabic_engine.semantic_kernel.closure import (
    SemanticKernelClosureEngine,
    ClosureTrace,
)
from arabic_engine.semantic_kernel.alignment import (
    project_root_to_pattern_space,
    project_root_to_form_space,
    project_pattern_to_form_space,
    project_to_common_space,
)
from arabic_engine.semantic_kernel.context import ContextDeltaBuilder, ContextFeatures
from arabic_engine.semantic_kernel.weight_scheduler import (
    WeightScheduler,
    BlendingWeights,
)
from arabic_engine.semantic_kernel.phonotactics import (
    PhonotacticChecker,
    RootType,
    classify_root_type,
)
from arabic_engine.semantic_kernel.metrics import TransferMetrics
from arabic_engine.semantic_kernel import seed_data


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_closed_singular(word_cat=WordCategory.FI3L) -> SingularUnit:
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
    return unit


def _make_closed_weighted(pattern="فَعَلَ", root="ك ت ب") -> WeightedUnit:
    unit = _make_closed_singular()
    record = WeightRecord(
        eligibility=WeightEligibility.ELIGIBLE,
        pattern=pattern, root=root,
        inflection=InflectionKind.MU3RAB,
        derivation_legality=DerivationKind.MUSHTAQ,
        verb_eligible=True,
    )
    weighted = WeightedUnit(singular=unit, weight=record)
    WeightClosureEngine.close(weighted)
    assert weighted.fully_closed
    return weighted


def _make_transfer_result(root_vals=None, pat_vals=None, form_vals=None):
    root = RootKernelBuilder.build(
        root_text="ك ت ب",
        semantic_values=root_vals or seed_data.SEED_ROOT_KTB,
    )
    pat = PatternTransformBuilder.build(
        pattern_code="فَعَلَ",
        transform_values=pat_vals or seed_data.SEED_PATTERN_FA3ALA,
    )
    form = FormProfileBuilder.build(
        pattern_id=pat.pattern_id,
        form_values=form_vals or seed_data.SEED_FORM_VERB_PAST_MS,
    )
    return SemanticTransferEngine.transfer(
        root_kernel=root, pattern_transform=pat, form_profile=form,
    )


# ===========================================================================
# Phase 1: Correctness fixes
# ===========================================================================


class TestPhase1ConditionalPersistence:
    """Phase 1.1: Only persist semantic transfer when closure == CLOSED."""

    def test_failed_transfer_not_persisted(self):
        """When semantic closure fails, weight record should NOT have transfer."""
        chain = MasterChain()
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
            pattern="فَعَلَ", root="ك ت ب",
            inflection=InflectionKind.MU3RAB,
            derivation_legality=DerivationKind.MUSHTAQ,
            verb_eligible=True,
        )
        chain.process_weight(weight)

        # Build an invalid root kernel (empty text → won't pass completeness)
        root_kernel = RootKernelBuilder.build(
            root_text="",
            semantic_values=seed_data.SEED_ROOT_KTB,
        )
        pat_transform = PatternTransformBuilder.build(
            pattern_code="فَعَلَ",
            transform_values=seed_data.SEED_PATTERN_FA3ALA,
        )
        form = FormProfileBuilder.build(
            pattern_id=pat_transform.pattern_id,
            form_values=seed_data.SEED_FORM_VERB_PAST_MS,
        )

        results = chain.process_semantic_transfer(
            root_kernel=root_kernel,
            pattern_transform=pat_transform,
            form_profile=form,
        )
        # Should fail (root text empty → root consistency or completeness fails)
        # The transfer should NOT be persisted on the weight
        assert chain.state.weighted.weight.semantic_transfer is None


class TestPhase1RootPatternConsistency:
    """Phase 1.2: Root/pattern consistency validation."""

    def test_mismatched_root_rejects(self):
        chain = MasterChain()
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
            pattern="فَعَلَ", root="ك ت ب",
            inflection=InflectionKind.MU3RAB,
            derivation_legality=DerivationKind.MUSHTAQ,
            verb_eligible=True,
        )
        chain.process_weight(weight)

        # Mismatched root
        root_kernel = RootKernelBuilder.build(
            root_text="ع ل م",  # Different from weight's "ك ت ب"
            semantic_values=seed_data.SEED_ROOT_3LM,
        )
        pat_transform = PatternTransformBuilder.build(
            pattern_code="فَعَلَ",
            transform_values=seed_data.SEED_PATTERN_FA3ALA,
        )
        form = FormProfileBuilder.build(
            pattern_id="test",
            form_values=seed_data.SEED_FORM_VERB_PAST_MS,
        )

        results = chain.process_semantic_transfer(
            root_kernel=root_kernel,
            pattern_transform=pat_transform,
            form_profile=form,
        )
        assert results[0].verdict is GateVerdict.REJECT
        assert "root_consistency" in results[0].missing_condition

    def test_mismatched_pattern_rejects(self):
        chain = MasterChain()
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
            pattern="فَعَلَ", root="ك ت ب",
            inflection=InflectionKind.MU3RAB,
            derivation_legality=DerivationKind.MUSHTAQ,
            verb_eligible=True,
        )
        chain.process_weight(weight)

        root_kernel = RootKernelBuilder.build(
            root_text="ك ت ب",
            semantic_values=seed_data.SEED_ROOT_KTB,
        )
        pat_transform = PatternTransformBuilder.build(
            pattern_code="فَعَّلَ",  # Different from weight's "فَعَلَ"
            transform_values=seed_data.SEED_PATTERN_FA33ALA,
        )
        form = FormProfileBuilder.build(
            pattern_id="test",
            form_values=seed_data.SEED_FORM_VERB_PAST_MS,
        )

        results = chain.process_semantic_transfer(
            root_kernel=root_kernel,
            pattern_transform=pat_transform,
            form_profile=form,
        )
        assert results[0].verdict is GateVerdict.REJECT
        assert "pattern_consistency" in results[0].missing_condition


class TestPhase1GracefulSemanticValues:
    """Phase 1.3: Graceful handling of invalid semantic_values."""

    def test_invalid_length_degrades_gracefully(self):
        """MizanClassifier with wrong-length semantic_values → no kernel."""
        unit = _make_closed_singular()
        record = MizanClassifier.classify(
            unit,
            pattern="فَعَلَ",
            root="ك ت ب",
            semantic_values=(0.5, 0.5),  # Wrong length (needs 13)
        )
        assert record.eligibility is WeightEligibility.ELIGIBLE
        assert record.semantic_kernel is None  # Graceful degradation


class TestPhase1ConstantCleanup:
    """Phase 1.4: _COMPAT_THRESHOLD removed, _OVERLAP_COMPAT_RATIO used."""

    def test_no_compat_threshold_constant(self):
        from arabic_engine.semantic_kernel import compatibility
        assert not hasattr(compatibility, '_COMPAT_THRESHOLD')
        assert hasattr(compatibility, '_OVERLAP_COMPAT_RATIO')


# ===========================================================================
# Phase 2: Architecture improvements
# ===========================================================================


class TestPhase2CosineCompatibility:
    """Phase 2.1: Cosine-similarity compatibility check."""

    def test_cosine_compatibility_score_returns_float(self):
        root = RootKernelBuilder.build(
            root_text="ك ت ب", semantic_values=seed_data.SEED_ROOT_KTB,
        )
        pat = PatternTransformBuilder.build(
            pattern_code="فَعَّلَ", transform_values=seed_data.SEED_PATTERN_FA33ALA,
        )
        score = CompatibilityChecker.cosine_compatibility_score(root, pat)
        assert isinstance(score, float)
        assert -1.0 <= score <= 1.0

    def test_cosine_score_zero_for_empty(self):
        root = RootKernelBuilder.build(
            root_text="ك ت ب", semantic_values=seed_data.SEED_ROOT_KTB,
        )
        pat = PatternTransformBuilder.build(
            pattern_code="فَعَلَ", transform_values=seed_data.SEED_PATTERN_FA3ALA,
        )
        # Zero pattern → cosine should be 0.0
        score = CompatibilityChecker.cosine_compatibility_score(root, pat)
        assert score == pytest.approx(0.0, abs=1e-9)


class TestPhase2Alignment:
    """Phase 2.2: Semantic alignment mappings."""

    def test_project_root_to_pattern_space(self):
        v = SemanticVector(values=tuple(float(i) for i in range(13)))
        projected = project_root_to_pattern_space(v)
        assert projected.dim == 12

    def test_project_root_to_form_space(self):
        v = SemanticVector(values=tuple(float(i) for i in range(13)))
        projected = project_root_to_form_space(v)
        assert projected.dim == 9

    def test_project_pattern_to_form_space(self):
        v = SemanticVector(values=tuple(float(i) for i in range(12)))
        projected = project_pattern_to_form_space(v)
        assert projected.dim == 9

    def test_project_to_common_space(self):
        r = SemanticVector(values=tuple(float(i) for i in range(13)))
        p = SemanticVector(values=tuple(float(i) for i in range(12)))
        f = SemanticVector(values=tuple(float(i) for i in range(9)))
        r_proj, p_proj, f_proj = project_to_common_space(r, p, f)
        assert r_proj.dim == 13
        assert p_proj.dim == 13
        assert f_proj.dim == 13

    def test_alignment_preserves_identity_for_root(self):
        """Root vector should be identity-projected (already 13-dim)."""
        r = SemanticVector(values=(1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        r_proj, _, _ = project_to_common_space(
            r,
            SemanticVector(values=tuple(0.0 for _ in range(12))),
            SemanticVector(values=tuple(0.0 for _ in range(9))),
        )
        assert r_proj.values == r.values


class TestPhase2ContextDelta:
    """Phase 2.3: Context delta builder."""

    def test_zero_context_delta(self):
        delta = ContextDeltaBuilder.zero()
        assert delta.dim == 13
        assert all(v == 0.0 for v in delta.values)

    def test_default_features_produce_small_delta(self):
        features = ContextFeatures()  # defaults
        delta = ContextDeltaBuilder.build(features)
        assert delta.dim == 13

    def test_sentence_initial_boosts_agency(self):
        features = ContextFeatures(syntactic_position=0.0)
        delta = ContextDeltaBuilder.build(features)
        # Agency is index 4
        assert delta.values[4] > 0.0

    def test_sentence_final_boosts_resultativity(self):
        features = ContextFeatures(syntactic_position=1.0)
        delta = ContextDeltaBuilder.build(features)
        # Resultativity is index 7
        assert delta.values[7] > 0.0

    def test_negation_inverts_agency_and_causality(self):
        features = ContextFeatures(negation=True)
        delta = ContextDeltaBuilder.build(features)
        assert delta.values[4] < 0.0  # AGENCY
        assert delta.values[6] < 0.0  # CAUSALITY

    def test_emphasis_amplifies_event_and_quality(self):
        features = ContextFeatures(emphasis=0.8)
        delta = ContextDeltaBuilder.build(features)
        assert delta.values[1] > 0.0  # EVENT
        assert delta.values[2] > 0.0  # QUALITY

    def test_collocational_bias_added(self):
        bias = tuple(0.1 * i for i in range(13))
        features = ContextFeatures(collocational_bias=bias)
        delta = ContextDeltaBuilder.build(features)
        for i in range(13):
            assert delta.values[i] >= bias[i]

    def test_context_delta_used_in_transfer(self):
        """Context delta should affect the transfer output."""
        root = RootKernelBuilder.build(root_text="ك ت ب", semantic_values=seed_data.SEED_ROOT_KTB)
        pat = PatternTransformBuilder.build(pattern_code="فَعَلَ", transform_values=seed_data.SEED_PATTERN_FA3ALA)
        form = FormProfileBuilder.build(pattern_id=pat.pattern_id, form_values=seed_data.SEED_FORM_VERB_PAST_MS)

        features = ContextFeatures(syntactic_position=0.0, emphasis=1.0)
        ctx = ContextDeltaBuilder.build(features)

        result_no_ctx = SemanticTransferEngine.transfer(root_kernel=root, pattern_transform=pat, form_profile=form)
        result_with_ctx = SemanticTransferEngine.transfer(
            root_kernel=root, pattern_transform=pat, form_profile=form, context_delta=ctx,
        )

        assert result_no_ctx.output_kernel.values != result_with_ctx.output_kernel.values


class TestPhase2WeightScheduler:
    """Phase 2.4: Adaptive blending weights."""

    def test_default_weights(self):
        w = BlendingWeights()
        assert w.w_root == pytest.approx(0.50)
        assert w.w_pattern == pytest.approx(0.30)
        assert w.w_form == pytest.approx(0.15)
        assert w.w_context == pytest.approx(0.05)

    def test_schedule_returns_blending_weights(self):
        root = RootKernelBuilder.build(root_text="ك ت ب", semantic_values=seed_data.SEED_ROOT_KTB)
        pat = PatternTransformBuilder.build(pattern_code="فَعَلَ", transform_values=seed_data.SEED_PATTERN_FA3ALA)
        form = FormProfileBuilder.build(pattern_id="test", form_values=seed_data.SEED_FORM_VERB_PAST_MS)
        w = WeightScheduler.schedule(root, pat, form)
        assert isinstance(w, BlendingWeights)
        assert w.w_root + w.w_pattern + w.w_form + w.w_context == pytest.approx(1.0, abs=1e-6)

    def test_high_transformability_shifts_weight_to_pattern(self):
        root = RootKernelBuilder.build(root_text="ك ت ب", semantic_values=seed_data.SEED_ROOT_KTB)
        pat = PatternTransformBuilder.build(
            pattern_code="فَعَّلَ", transform_values=seed_data.SEED_PATTERN_FA33ALA,
        )
        form = FormProfileBuilder.build(pattern_id="test", form_values=seed_data.SEED_FORM_VERB_PAST_MS)

        # Root with high transformability
        root.transformability_score = 0.9
        w = WeightScheduler.schedule(root, pat, form)
        assert w.w_root < 0.50  # Shifted down
        assert w.w_pattern > 0.30 or w.w_form > 0.15  # Shifted up somewhere


# ===========================================================================
# Phase 3: Data & Coverage Expansion
# ===========================================================================


class TestPhase3ExpandedSeedData:
    """Phase 3.1: Expanded seed data."""

    def test_at_least_20_roots(self):
        root_seeds = [
            name for name in dir(seed_data)
            if name.startswith("SEED_ROOT_")
        ]
        assert len(root_seeds) >= 20

    def test_at_least_10_patterns(self):
        pattern_seeds = [
            name for name in dir(seed_data)
            if name.startswith("SEED_PATTERN_")
        ]
        assert len(pattern_seeds) >= 10

    def test_at_least_6_form_profiles(self):
        form_seeds = [
            name for name in dir(seed_data)
            if name.startswith("SEED_FORM_")
        ]
        assert len(form_seeds) >= 6

    def test_all_new_roots_are_13_dim(self):
        for name in dir(seed_data):
            if name.startswith("SEED_ROOT_"):
                val = getattr(seed_data, name)
                assert len(val) == 13, f"{name} has {len(val)} dims, expected 13"

    def test_all_new_patterns_are_12_dim(self):
        for name in dir(seed_data):
            if name.startswith("SEED_PATTERN_"):
                val = getattr(seed_data, name)
                assert len(val) == 12, f"{name} has {len(val)} dims, expected 12"

    def test_all_new_forms_are_9_dim(self):
        for name in dir(seed_data):
            if name.startswith("SEED_FORM_"):
                val = getattr(seed_data, name)
                assert len(val) == 9, f"{name} has {len(val)} dims, expected 9"

    def test_new_patterns_build_successfully(self):
        new_patterns = {
            "تَفَعَّلَ": seed_data.SEED_PATTERN_TAFA33ALA,
            "اِفْتَعَلَ": seed_data.SEED_PATTERN_IFTA3ALA,
            "مِفْعَال": seed_data.SEED_PATTERN_MIF3AL,
            "مَفْعَل": seed_data.SEED_PATTERN_MAF3AL,
        }
        for code, vals in new_patterns.items():
            pat = PatternTransformBuilder.build(pattern_code=code, transform_values=vals)
            assert pat.pattern_code == code

    def test_new_form_profiles_build_successfully(self):
        new_forms = [
            seed_data.SEED_FORM_VERB_PRESENT_MS,
            seed_data.SEED_FORM_VERB_PASSIVE_PAST_MS,
            seed_data.SEED_FORM_NOUN_INDEF_FS,
            seed_data.SEED_FORM_NOUN_DEF_MD,
            seed_data.SEED_FORM_NOUN_DEF_MP,
            seed_data.SEED_FORM_VERB_IMPERATIVE_MS,
        ]
        for vals in new_forms:
            form = FormProfileBuilder.build(pattern_id="test", form_values=vals)
            assert form.form_semantic_vector.dim == 9


class TestPhase3Phonotactics:
    """Phase 3.2: Phonological compatibility checks."""

    def test_classify_sound_root(self):
        assert classify_root_type("ك ت ب") == RootType.SOUND

    def test_classify_hollow_root(self):
        assert classify_root_type("ق و ل") == RootType.HOLLOW

    def test_classify_defective_root(self):
        assert classify_root_type("ر م ي") == RootType.DEFECTIVE

    def test_classify_assimilated_root(self):
        assert classify_root_type("و ج د") == RootType.ASSIMILATED

    def test_classify_doubled_root(self):
        assert classify_root_type("م د د") == RootType.DOUBLED

    def test_classify_hamzated_root(self):
        assert classify_root_type("أ ك ل") == RootType.HAMZATED

    def test_classify_quadriliteral(self):
        assert classify_root_type("ز ل ز ل") == RootType.QUADRILITERAL

    def test_phonotactic_check_sound_root(self):
        result = PhonotacticChecker.check("ك ت ب", "فَعَلَ")
        assert result.compatible
        assert result.root_type == RootType.SOUND

    def test_phonotactic_doubled_with_fa33ala(self):
        result = PhonotacticChecker.check("م د د", "فَعَّلَ")
        assert result.compatible  # Dispreferred but possible
        assert "extra" in result.notes.lower() or result.notes == ""

    def test_extra_phonological_cost_doubled_fa33ala(self):
        cost = PhonotacticChecker.extra_phonological_cost("م د د", "فَعَّلَ")
        assert cost > 0.0

    def test_no_extra_cost_sound_root(self):
        cost = PhonotacticChecker.extra_phonological_cost("ك ت ب", "فَعَلَ")
        assert cost == 0.0


# ===========================================================================
# Phase 4: Robustness & Quality
# ===========================================================================


class TestPhase4WeightRecordDeduplication:
    """Phase 4.1: WeightRecord is defined in types_weight.py only."""

    def test_types_re_exports_from_types_weight(self):
        from arabic_engine.core import types
        from arabic_engine.core import types_weight
        assert types.WeightRecord is types_weight.WeightRecord
        assert types.WeightedUnit is types_weight.WeightedUnit


class TestPhase4ClosureTrace:
    """Phase 4.2: Error recovery mechanism (ClosureTrace)."""

    def test_closure_trace_on_success(self):
        result = _make_transfer_result()
        trace = SemanticKernelClosureEngine.close_with_trace(result)
        assert trace.final_status == ClosureStatus.CLOSED
        assert trace.failed_gate is None
        assert trace.suggestions == []

    def test_closure_trace_on_failure(self):
        root = RootKernelBuilder.build(root_text="", semantic_values=seed_data.SEED_ROOT_KTB)
        pat = PatternTransformBuilder.build(pattern_code="فَعَلَ", transform_values=seed_data.SEED_PATTERN_FA3ALA)
        form = FormProfileBuilder.build(pattern_id=pat.pattern_id, form_values=seed_data.SEED_FORM_VERB_PAST_MS)
        result = SemanticTransferEngine.transfer(root_kernel=root, pattern_transform=pat, form_profile=form)
        trace = SemanticKernelClosureEngine.close_with_trace(result)
        assert trace.final_status != ClosureStatus.CLOSED
        assert trace.failed_gate is not None
        assert len(trace.suggestions) > 0


class TestPhase4Metrics:
    """Phase 4.3: Performance metrics."""

    def test_initial_metrics_zero(self):
        m = TransferMetrics()
        assert m.transfer_count == 0
        assert m.avg_transfer_time_ms == 0.0

    def test_record_transfer(self):
        m = TransferMetrics()
        m.record_transfer(10.0)
        m.record_transfer(20.0)
        assert m.transfer_count == 2
        assert m.avg_transfer_time_ms == pytest.approx(15.0)

    def test_closure_pass_rate(self):
        m = TransferMetrics()
        m.record_closure(True)
        m.record_closure(True)
        m.record_closure(False)
        assert m.closure_pass_rate == pytest.approx(2 / 3)

    def test_summary_dict(self):
        m = TransferMetrics()
        m.record_transfer(5.0)
        s = m.summary()
        assert "transfer_count" in s
        assert "avg_transfer_time_ms" in s

    def test_reset(self):
        m = TransferMetrics()
        m.record_transfer(10.0)
        m.record_closure(True)
        m.record_cost(1.0)
        m.reset()
        assert m.transfer_count == 0


class TestPhase4ParetoOptimal:
    """Phase 4.4: Multi-objective economy optimization."""

    def test_pareto_empty(self):
        result = EconomyOptimizer.select_pareto_optimal([])
        assert result == []

    def test_pareto_single(self):
        r = _make_transfer_result()
        SemanticKernelClosureEngine.close(r)
        result = EconomyOptimizer.select_pareto_optimal([r])
        assert len(result) == 1

    def test_pareto_with_multiple_candidates(self):
        candidates = []
        for pat_vals in [
            seed_data.SEED_PATTERN_FA3ALA,
            seed_data.SEED_PATTERN_FA33ALA,
            seed_data.SEED_PATTERN_AF3ALA,
        ]:
            r = _make_transfer_result(pat_vals=pat_vals)
            SemanticKernelClosureEngine.close(r)
            candidates.append(r)

        pareto = EconomyOptimizer.select_pareto_optimal(candidates)
        assert len(pareto) >= 1
        assert len(pareto) <= len(candidates)


# ===========================================================================
# Phase 5: Integration & Higher Layers
# ===========================================================================


class TestPhase5AutoChainSemanticTransfer:
    """Phase 5.1: Auto-invoke semantic transfer in process_weight."""

    def test_process_weight_with_semantic_auto_chain(self):
        chain = MasterChain()
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
            pattern="فَعَلَ", root="ك ت ب",
            inflection=InflectionKind.MU3RAB,
            derivation_legality=DerivationKind.MUSHTAQ,
            verb_eligible=True,
        )

        # Auto-chain by providing all semantic data
        results = chain.process_weight(
            weight,
            semantic_values=seed_data.SEED_ROOT_KTB,
            pattern_transform_values=seed_data.SEED_PATTERN_FA3ALA,
            form_values=seed_data.SEED_FORM_VERB_PAST_MS,
        )
        assert all(r.passed for r in results)
        assert chain.state.semantic_transfer is not None
        assert chain.state.semantic_transfer.closure == ClosureStatus.CLOSED

    def test_process_weight_without_semantic_auto_chain(self):
        """Without semantic args, process_weight should NOT auto-chain."""
        chain = MasterChain()
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
            pattern="فَعَلَ", root="ك ت ب",
            inflection=InflectionKind.MU3RAB,
            derivation_legality=DerivationKind.MUSHTAQ,
            verb_eligible=True,
        )
        results = chain.process_weight(weight)
        assert all(r.passed for r in results)
        assert chain.state.semantic_transfer is None  # No auto-chain


class TestPhase5CompositionSemantic:
    """Phase 5.2: Semantic kernel access from composition."""

    def test_role_assignment_semantic_transfer(self):
        weighted = _make_closed_weighted()
        role = RoleAssignment(unit=weighted, role=RoleTag.MUSNAD_ILAYH)
        # No semantic transfer attached → None
        assert role.semantic_transfer is None

    def test_composition_semantic_compatibility_no_data(self):
        """Backward compatible: no semantic data → score = 1.0."""
        w1 = _make_closed_weighted()
        w2 = _make_closed_weighted()
        rel = CompositionRelation(
            kind=RelationKind.ASNADI,
            roles=[
                RoleAssignment(unit=w1, role=RoleTag.MUSNAD_ILAYH),
                RoleAssignment(unit=w2, role=RoleTag.MUSNAD),
            ],
            closure=ClosureStatus.CLOSED,
        )
        assert rel.semantic_compatibility_score == 1.0


class TestPhase5PropositionJudgement:
    """Phase 5.3: Semantic propagation to Proposition/Judgement."""

    def test_proposition_semantic_coherence_no_data(self):
        prop = Proposition(relations=[], closure=ClosureStatus.CLOSED)
        assert prop.semantic_coherence_score == 1.0

    def test_judgement_has_semantic_confidence(self):
        j = Judgement()
        assert j.semantic_confidence == 1.0  # default
