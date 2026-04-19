"""Integration tests for the semantic kernel within the full master chain.

Verifies:
1. The full pipeline: Singular → Weight → SemanticKernel → Transfer → K_F
2. Backward compatibility: all existing tests still pass with the new layer
3. The ascent path: K_F → (R, P, F) → explanation
4. Optional semantic enrichment on MizanClassifier
"""

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

from arabic_engine.singular.closure import SingularClosureEngine
from arabic_engine.weight.closure import WeightClosureEngine
from arabic_engine.weight.mizan import MizanClassifier
from arabic_engine.composition.asnadi import AsnadiRelationBuilder
from arabic_engine.runtime.master_chain import MasterChain
from arabic_engine.runtime.runtime_view import RuntimeView

from arabic_engine.semantic_kernel.root_kernel import RootKernelBuilder
from arabic_engine.semantic_kernel.pattern_transform import PatternTransformBuilder
from arabic_engine.semantic_kernel.form_profile import FormProfileBuilder
from arabic_engine.semantic_kernel.transfer import SemanticTransferEngine
from arabic_engine.semantic_kernel.closure import SemanticKernelClosureEngine
from arabic_engine.semantic_kernel import seed_data


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_closed_singular(
    word_cat: WordCategory = WordCategory.FI3L,
) -> SingularUnit:
    """Create a fully closed singular unit."""
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


def _make_closed_weighted(
    word_cat: WordCategory = WordCategory.FI3L,
    pattern: str = "فَعَلَ",
    root: str = "ك ت ب",
) -> WeightedUnit:
    """Create a fully closed weighted unit."""
    unit = _make_closed_singular(word_cat)
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
# Integration test: full semantic pipeline through master chain
# ---------------------------------------------------------------------------


def test_master_chain_with_semantic_transfer():
    """Full pipeline: Singular → Weight → SemanticTransfer → Composition → Judgement."""
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

    # Step 3: Semantic transfer
    root_kernel = RootKernelBuilder.build(
        root_text="ك ت ب",
        semantic_values=seed_data.SEED_ROOT_KTB,
    )
    pat_transform = PatternTransformBuilder.build(
        pattern_code="فَعَلَ",
        transform_values=seed_data.SEED_PATTERN_FA3ALA,
    )
    form_profile = FormProfileBuilder.build(
        pattern_id=pat_transform.pattern_id,
        form_values=seed_data.SEED_FORM_VERB_PAST_MS,
    )

    sem_results = chain.process_semantic_transfer(
        root_kernel=root_kernel,
        pattern_transform=pat_transform,
        form_profile=form_profile,
    )
    assert all(r.passed for r in sem_results)

    # Verify semantic data is stored in chain state
    assert chain.state.semantic_transfer is not None
    assert chain.state.semantic_transfer.closure is ClosureStatus.CLOSED
    assert chain.state.semantic_transfer.output_kernel.dim == 13

    # Step 4: Continue with composition → proposition → judgement
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

    rel, rel_results = AsnadiRelationBuilder.build(weighted2, chain.state.weighted)
    assert rel is not None

    results = chain.process_composition([rel])
    assert all(r.passed for r in results)

    result = chain.process_proposition()
    assert result.passed

    result = chain.process_judgement(
        direction=JudgementDirection.AFFIRMATION,
        rank=JudgementRank.CERTAIN,
        subject="الطالب",
        criterion="الإسناد",
        reason="كَتَبَ الطالبُ — إسناد صحيح مع نواة دلالية",
    )
    assert result.passed


def test_semantic_transfer_rejects_before_weight_closure():
    """Semantic transfer should reject if weight is not closed."""
    chain = MasterChain()

    root_kernel = RootKernelBuilder.build(
        root_text="ك ت ب",
        semantic_values=seed_data.SEED_ROOT_KTB,
    )
    pat_transform = PatternTransformBuilder.build(
        pattern_code="فَعَلَ",
        transform_values=seed_data.SEED_PATTERN_FA3ALA,
    )
    form_profile = FormProfileBuilder.build(
        pattern_id="test",
        form_values=seed_data.SEED_FORM_VERB_PAST_MS,
    )

    results = chain.process_semantic_transfer(
        root_kernel=root_kernel,
        pattern_transform=pat_transform,
        form_profile=form_profile,
    )
    assert results[0].verdict is GateVerdict.REJECT


def test_mizan_with_semantic_values():
    """MizanClassifier should attach a semantic kernel when values are provided."""
    unit = _make_closed_singular()
    record = MizanClassifier.classify(
        unit,
        pattern="فَعَلَ",
        root="ك ت ب",
        semantic_values=seed_data.SEED_ROOT_KTB,
    )
    assert record.eligibility is WeightEligibility.ELIGIBLE
    assert record.semantic_kernel is not None
    assert record.semantic_kernel.semantic_vector.dim == 13
    assert record.semantic_kernel.root_text == "ك ت ب"


def test_mizan_without_semantic_values_backward_compatible():
    """MizanClassifier without semantic_values should work exactly as before."""
    unit = _make_closed_singular()
    record = MizanClassifier.classify(unit, pattern="فَعَلَ", root="ك ت ب")
    assert record.eligibility is WeightEligibility.ELIGIBLE
    assert record.semantic_kernel is None
    assert record.semantic_transfer is None


def test_weight_closure_with_semantic_transfer():
    """Weight closure should run the semantic kernel gate when transfer is present."""
    unit = _make_closed_singular()
    record = WeightRecord(
        eligibility=WeightEligibility.ELIGIBLE,
        pattern="فَعَلَ",
        root="ك ت ب",
        inflection=InflectionKind.MU3RAB,
        derivation_legality=DerivationKind.MUSHTAQ,
        verb_eligible=True,
    )

    # Build and attach semantic transfer
    root_kernel = RootKernelBuilder.build(
        root_text="ك ت ب",
        semantic_values=seed_data.SEED_ROOT_KTB,
    )
    pat_transform = PatternTransformBuilder.build(
        pattern_code="فَعَلَ",
        transform_values=seed_data.SEED_PATTERN_FA3ALA,
    )
    form_profile = FormProfileBuilder.build(
        pattern_id=pat_transform.pattern_id,
        form_values=seed_data.SEED_FORM_VERB_PAST_MS,
    )
    transfer_result = SemanticTransferEngine.transfer(
        root_kernel=root_kernel,
        pattern_transform=pat_transform,
        form_profile=form_profile,
    )
    record.semantic_transfer = transfer_result

    weighted = WeightedUnit(singular=unit, weight=record)
    results = WeightClosureEngine.close(weighted)
    assert all(r.passed for r in results)
    assert weighted.fully_closed
    assert record.semantic_transfer.closure is ClosureStatus.CLOSED


def test_ascent_path_explains_transfer():
    """Ascent: from K_F, retrieve R, P, F and explain the transfer."""
    root = RootKernelBuilder.build(
        root_text="ك ت ب",
        semantic_values=seed_data.SEED_ROOT_KTB,
    )
    pat = PatternTransformBuilder.build(
        pattern_code="فَعَلَ",
        transform_values=seed_data.SEED_PATTERN_FA3ALA,
    )
    form = FormProfileBuilder.build(
        pattern_id=pat.pattern_id,
        form_values=seed_data.SEED_FORM_VERB_PAST_MS,
    )

    result = SemanticTransferEngine.transfer(
        root_kernel=root,
        pattern_transform=pat,
        form_profile=form,
    )

    # Ascent: from the result, recover the components
    assert result.root_kernel.root_text == "ك ت ب"
    assert result.pattern_transform.pattern_code == "فَعَلَ"
    assert result.form_profile.pattern_id == pat.pattern_id

    # Why this pattern? Because transformation_score indicates preservation
    assert result.transformation_score > 0.0

    # The output kernel is computable and interpretable
    assert result.output_kernel.dim == 13


def test_different_patterns_produce_different_outputs():
    """Different patterns applied to the same root should yield different K_F."""
    root = RootKernelBuilder.build(
        root_text="ك ت ب",
        semantic_values=seed_data.SEED_ROOT_KTB,
    )
    form = FormProfileBuilder.build(
        pattern_id="test",
        form_values=seed_data.SEED_FORM_VERB_PAST_MS,
    )

    results = {}
    for name, vals in [
        ("فَعَلَ", seed_data.SEED_PATTERN_FA3ALA),
        ("فَعَّلَ", seed_data.SEED_PATTERN_FA33ALA),
        ("أَفْعَلَ", seed_data.SEED_PATTERN_AF3ALA),
        ("اِنْفَعَلَ", seed_data.SEED_PATTERN_INFA3ALA),
        ("اِسْتَفْعَلَ", seed_data.SEED_PATTERN_ISTAF3ALA),
    ]:
        pat = PatternTransformBuilder.build(pattern_code=name, transform_values=vals)
        r = SemanticTransferEngine.transfer(
            root_kernel=root,
            pattern_transform=pat,
            form_profile=form,
        )
        results[name] = r.output_kernel.values

    # All outputs should be distinct
    values_set = set(results.values())
    assert len(values_set) == len(results), "All patterns should produce distinct outputs"


def test_fractal_hypothesis_identity_preservation():
    """Fractal hypothesis: Id(T_n(x_n), x_n) ≥ ε.

    The transformation should preserve some identity between input and output.
    """
    root = RootKernelBuilder.build(
        root_text="ك ت ب",
        semantic_values=seed_data.SEED_ROOT_KTB,
    )
    pat = PatternTransformBuilder.build(
        pattern_code="فَعَلَ",
        transform_values=seed_data.SEED_PATTERN_FA3ALA,
    )
    form = FormProfileBuilder.build(
        pattern_id=pat.pattern_id,
        form_values=seed_data.SEED_FORM_VERB_PAST_MS,
    )

    result = SemanticTransferEngine.transfer(
        root_kernel=root,
        pattern_transform=pat,
        form_profile=form,
    )

    # The identity score should be above a threshold ε
    epsilon = 0.3
    assert result.transformation_score >= epsilon, (
        f"Identity preservation failed: {result.transformation_score} < {epsilon}"
    )


def test_fractal_hypothesis_structural_similarity():
    """Fractal hypothesis: StructSim(T_n(x_n), x_n) ≥ λ.

    The same SemanticVector structure is used at all levels,
    and the output dimension matches the input dimension.
    """
    root = RootKernelBuilder.build(
        root_text="ك ت ب",
        semantic_values=seed_data.SEED_ROOT_KTB,
    )
    pat = PatternTransformBuilder.build(
        pattern_code="فَعَلَ",
        transform_values=seed_data.SEED_PATTERN_FA3ALA,
    )
    form = FormProfileBuilder.build(
        pattern_id=pat.pattern_id,
        form_values=seed_data.SEED_FORM_VERB_PAST_MS,
    )

    result = SemanticTransferEngine.transfer(
        root_kernel=root,
        pattern_transform=pat,
        form_profile=form,
    )

    # Structural similarity: same type, same dimension
    assert isinstance(result.input_kernel, SemanticVector)
    assert isinstance(result.output_kernel, SemanticVector)
    assert result.output_kernel.dim == max(
        root.semantic_vector.dim,
        pat.semantic_transform_vector.dim,
        form.form_semantic_vector.dim,
    )
