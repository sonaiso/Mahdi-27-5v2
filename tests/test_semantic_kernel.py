"""Tests for the semantic kernel layer — unit tests for all components."""

import math

import pytest

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_semantic import (
    CompatibilityStatus,
    FormSemanticDimension,
    PatternSemanticDimension,
    SemanticDimension,
)
from arabic_engine.core.types_semantic import (
    FormSemanticProfile,
    PatternSemanticTransform,
    RootSemanticKernel,
    SemanticCost,
    SemanticTransferResult,
    SemanticVector,
)

from arabic_engine.semantic_kernel.root_kernel import RootKernelBuilder
from arabic_engine.semantic_kernel.pattern_transform import PatternTransformBuilder
from arabic_engine.semantic_kernel.form_profile import FormProfileBuilder
from arabic_engine.semantic_kernel.transfer import SemanticTransferEngine
from arabic_engine.semantic_kernel.compatibility import CompatibilityChecker
from arabic_engine.semantic_kernel.economy import EconomyOptimizer
from arabic_engine.semantic_kernel.closure import SemanticKernelClosureEngine
from arabic_engine.semantic_kernel import seed_data


# ===========================================================================
# SemanticVector tests
# ===========================================================================


class TestSemanticVector:
    """Tests for the SemanticVector dataclass."""

    def test_create_empty(self):
        v = SemanticVector(values=())
        assert v.dim == 0

    def test_create_with_values(self):
        v = SemanticVector(values=(1.0, 2.0, 3.0))
        assert v.dim == 3
        assert v.values == (1.0, 2.0, 3.0)

    def test_create_with_dimension_names(self):
        v = SemanticVector(
            values=(1.0, 2.0),
            dimension_names=("A", "B"),
        )
        assert v.dimension_names == ("A", "B")

    def test_mismatched_names_raises(self):
        with pytest.raises(ValueError, match="dimension_names length"):
            SemanticVector(
                values=(1.0, 2.0, 3.0),
                dimension_names=("A", "B"),
            )

    def test_dot_product(self):
        a = SemanticVector(values=(1.0, 2.0, 3.0))
        b = SemanticVector(values=(4.0, 5.0, 6.0))
        assert a.dot(b) == pytest.approx(32.0)

    def test_dot_different_dims_raises(self):
        a = SemanticVector(values=(1.0, 2.0))
        b = SemanticVector(values=(1.0,))
        with pytest.raises(ValueError, match="different dimensions"):
            a.dot(b)

    def test_norm(self):
        v = SemanticVector(values=(3.0, 4.0))
        assert v.norm() == pytest.approx(5.0)

    def test_norm_zero(self):
        v = SemanticVector(values=(0.0, 0.0))
        assert v.norm() == 0.0

    def test_cosine_similarity_identical(self):
        v = SemanticVector(values=(1.0, 2.0, 3.0))
        assert v.cosine_similarity(v) == pytest.approx(1.0)

    def test_cosine_similarity_orthogonal(self):
        a = SemanticVector(values=(1.0, 0.0))
        b = SemanticVector(values=(0.0, 1.0))
        assert a.cosine_similarity(b) == pytest.approx(0.0)

    def test_cosine_similarity_zero_vector(self):
        a = SemanticVector(values=(0.0, 0.0))
        b = SemanticVector(values=(1.0, 2.0))
        assert a.cosine_similarity(b) == 0.0

    def test_add(self):
        a = SemanticVector(values=(1.0, 2.0))
        b = SemanticVector(values=(3.0, 4.0))
        c = a.add(b)
        assert c.values == (4.0, 6.0)

    def test_add_different_dims_raises(self):
        a = SemanticVector(values=(1.0, 2.0))
        b = SemanticVector(values=(1.0,))
        with pytest.raises(ValueError, match="different dimensions"):
            a.add(b)

    def test_scale(self):
        v = SemanticVector(values=(1.0, 2.0, 3.0))
        s = v.scale(2.0)
        assert s.values == (2.0, 4.0, 6.0)

    def test_scale_zero(self):
        v = SemanticVector(values=(1.0, 2.0))
        s = v.scale(0.0)
        assert s.values == (0.0, 0.0)

    def test_frozen(self):
        v = SemanticVector(values=(1.0,))
        with pytest.raises(AttributeError):
            v.values = (2.0,)


# ===========================================================================
# RootKernelBuilder tests
# ===========================================================================


class TestRootKernelBuilder:
    """Tests for the RootKernelBuilder."""

    def test_build_basic(self):
        kernel = RootKernelBuilder.build(
            root_text="ك ت ب",
            semantic_values=seed_data.SEED_ROOT_KTB,
        )
        assert kernel.root_text == "ك ت ب"
        assert kernel.semantic_vector.dim == 13
        assert kernel.root_id  # auto-generated

    def test_build_with_custom_id(self):
        kernel = RootKernelBuilder.build(
            root_text="ع ل م",
            semantic_values=seed_data.SEED_ROOT_3LM,
            root_id="root-3lm",
        )
        assert kernel.root_id == "root-3lm"

    def test_build_wrong_dim_raises(self):
        with pytest.raises(ValueError, match="exactly 13"):
            RootKernelBuilder.build(
                root_text="ك ت ب",
                semantic_values=(1.0, 2.0),
            )

    def test_identity_score_concentrated(self):
        # A root with one very dominant dimension should have high identity
        values = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
        kernel = RootKernelBuilder.build(root_text="test", semantic_values=values)
        assert kernel.identity_score > 0.8

    def test_identity_score_uniform(self):
        # A root with uniform distribution has lower identity
        values = tuple(1.0 for _ in range(13))
        kernel = RootKernelBuilder.build(root_text="test", semantic_values=values)
        assert kernel.identity_score < 0.1

    def test_transformability_score_moderate(self):
        # A root with moderate spread is most transformable
        kernel = RootKernelBuilder.build(
            root_text="ك ت ب",
            semantic_values=seed_data.SEED_ROOT_KTB,
        )
        assert 0.0 < kernel.transformability_score <= 1.0

    def test_all_seed_roots_valid(self):
        """All seed roots should produce valid 13-dim kernels."""
        for name, values in [
            ("ك ت ب", seed_data.SEED_ROOT_KTB),
            ("ع ل م", seed_data.SEED_ROOT_3LM),
            ("ق ت ل", seed_data.SEED_ROOT_QTL),
            ("ح س ن", seed_data.SEED_ROOT_HSN),
            ("خ ر ج", seed_data.SEED_ROOT_XRJ),
        ]:
            kernel = RootKernelBuilder.build(root_text=name, semantic_values=values)
            assert kernel.semantic_vector.dim == 13
            assert kernel.identity_score > 0.0
            assert kernel.transformability_score > 0.0


# ===========================================================================
# PatternTransformBuilder tests
# ===========================================================================


class TestPatternTransformBuilder:
    """Tests for the PatternTransformBuilder."""

    def test_build_basic(self):
        transform = PatternTransformBuilder.build(
            pattern_code="فَعَلَ",
            transform_values=seed_data.SEED_PATTERN_FA3ALA,
        )
        assert transform.pattern_code == "فَعَلَ"
        assert transform.semantic_transform_vector.dim == 12
        assert transform.pattern_id  # auto-generated

    def test_build_wrong_dim_raises(self):
        with pytest.raises(ValueError, match="exactly 12"):
            PatternTransformBuilder.build(
                pattern_code="test",
                transform_values=(1.0, 2.0),
            )

    def test_neutral_pattern_zero_closure_index(self):
        """فَعَلَ (neutral) should have closure_index close to 0."""
        transform = PatternTransformBuilder.build(
            pattern_code="فَعَلَ",
            transform_values=seed_data.SEED_PATTERN_FA3ALA,
        )
        assert transform.closure_index == pytest.approx(0.0, abs=0.01)

    def test_intensive_pattern_nonzero_closure_index(self):
        """فَعَّلَ (intensive) should have a higher closure_index."""
        transform = PatternTransformBuilder.build(
            pattern_code="فَعَّلَ",
            transform_values=seed_data.SEED_PATTERN_FA33ALA,
        )
        assert transform.closure_index > 0.3

    def test_all_seed_patterns_valid(self):
        """All seed patterns should produce valid 12-dim transforms."""
        patterns = [
            ("فَعَلَ", seed_data.SEED_PATTERN_FA3ALA),
            ("فَعَّلَ", seed_data.SEED_PATTERN_FA33ALA),
            ("أَفْعَلَ", seed_data.SEED_PATTERN_AF3ALA),
            ("اِنْفَعَلَ", seed_data.SEED_PATTERN_INFA3ALA),
            ("اِسْتَفْعَلَ", seed_data.SEED_PATTERN_ISTAF3ALA),
            ("تَفَاعَلَ", seed_data.SEED_PATTERN_TAFA3ALA),
            ("فاعِل", seed_data.SEED_PATTERN_FA3IL),
            ("مَفْعُول", seed_data.SEED_PATTERN_MAF3UL),
        ]
        for code, values in patterns:
            t = PatternTransformBuilder.build(pattern_code=code, transform_values=values)
            assert t.semantic_transform_vector.dim == 12


# ===========================================================================
# FormProfileBuilder tests
# ===========================================================================


class TestFormProfileBuilder:
    """Tests for the FormProfileBuilder."""

    def test_build_basic(self):
        profile = FormProfileBuilder.build(
            pattern_id="pat-fa3ala",
            form_values=seed_data.SEED_FORM_VERB_PAST_MS,
        )
        assert profile.pattern_id == "pat-fa3ala"
        assert profile.form_semantic_vector.dim == 9

    def test_build_wrong_dim_raises(self):
        with pytest.raises(ValueError, match="exactly 9"):
            FormProfileBuilder.build(
                pattern_id="test",
                form_values=(1.0, 2.0),
            )


# ===========================================================================
# CompatibilityChecker tests
# ===========================================================================


class TestCompatibilityChecker:
    """Tests for the CompatibilityChecker."""

    def _make_root(self, values=None):
        return RootKernelBuilder.build(
            root_text="ك ت ب",
            semantic_values=values or seed_data.SEED_ROOT_KTB,
        )

    def _make_pattern(self, values=None):
        return PatternTransformBuilder.build(
            pattern_code="فَعَلَ",
            transform_values=values or seed_data.SEED_PATTERN_FA3ALA,
        )

    def _make_form(self, values=None):
        return FormProfileBuilder.build(
            pattern_id="pat-test",
            form_values=values or seed_data.SEED_FORM_VERB_PAST_MS,
        )

    def test_neutral_pattern_always_compatible(self):
        root = self._make_root()
        pat = self._make_pattern(seed_data.SEED_PATTERN_FA3ALA)
        assert CompatibilityChecker.check_root_pattern(root, pat) is CompatibilityStatus.COMPATIBLE

    def test_intensive_pattern_compatible_with_event_root(self):
        root = self._make_root(seed_data.SEED_ROOT_KTB)  # EVENT-high
        pat = self._make_pattern(seed_data.SEED_PATTERN_FA33ALA)
        result = CompatibilityChecker.check_root_pattern(root, pat)
        assert result in (CompatibilityStatus.COMPATIBLE, CompatibilityStatus.PARTIAL)

    def test_valid_root(self):
        root = self._make_root()
        assert CompatibilityChecker.valid_root(root) is True

    def test_invalid_root_empty_text(self):
        root = RootSemanticKernel()
        assert CompatibilityChecker.valid_root(root) is False

    def test_valid_pattern(self):
        pat = self._make_pattern()
        assert CompatibilityChecker.valid_pattern(pat) is True

    def test_invalid_pattern_empty_code(self):
        pat = PatternSemanticTransform()
        assert CompatibilityChecker.valid_pattern(pat) is False

    def test_realizable_form(self):
        form = self._make_form()
        assert CompatibilityChecker.realizable_form(form) is True

    def test_unrealizable_form_empty_pattern_id(self):
        form = FormSemanticProfile()
        assert CompatibilityChecker.realizable_form(form) is False

    def test_complete_min_success(self):
        root = self._make_root()
        pat = self._make_pattern()
        form = self._make_form()
        assert CompatibilityChecker.check_complete_min(root, pat, form) is True

    def test_complete_min_fails_invalid_root(self):
        root = RootSemanticKernel()
        pat = self._make_pattern()
        form = self._make_form()
        assert CompatibilityChecker.check_complete_min(root, pat, form) is False

    def test_complete_min_fails_unrealizable_form(self):
        root = self._make_root()
        pat = self._make_pattern()
        form = FormSemanticProfile()
        assert CompatibilityChecker.check_complete_min(root, pat, form) is False


# ===========================================================================
# SemanticTransferEngine tests
# ===========================================================================


class TestSemanticTransferEngine:
    """Tests for the SemanticTransferEngine."""

    def _make_root(self):
        return RootKernelBuilder.build(
            root_text="ك ت ب",
            semantic_values=seed_data.SEED_ROOT_KTB,
        )

    def _make_pattern(self, values=None):
        return PatternTransformBuilder.build(
            pattern_code="فَعَلَ",
            transform_values=values or seed_data.SEED_PATTERN_FA3ALA,
        )

    def _make_form(self):
        return FormProfileBuilder.build(
            pattern_id="pat-test",
            form_values=seed_data.SEED_FORM_VERB_PAST_MS,
        )

    def test_transfer_produces_result(self):
        result = SemanticTransferEngine.transfer(
            root_kernel=self._make_root(),
            pattern_transform=self._make_pattern(),
            form_profile=self._make_form(),
        )
        assert isinstance(result, SemanticTransferResult)
        assert result.output_kernel.dim > 0

    def test_transfer_neutral_pattern_preserves_root(self):
        """With a neutral pattern (فَعَلَ), output should be similar to root."""
        result = SemanticTransferEngine.transfer(
            root_kernel=self._make_root(),
            pattern_transform=self._make_pattern(seed_data.SEED_PATTERN_FA3ALA),
            form_profile=self._make_form(),
        )
        # Transformation score should be high for neutral pattern
        assert result.transformation_score > 0.5

    def test_transfer_intensive_pattern_shifts_meaning(self):
        """With فَعَّلَ, the meaning should shift (lower similarity)."""
        result_neutral = SemanticTransferEngine.transfer(
            root_kernel=self._make_root(),
            pattern_transform=self._make_pattern(seed_data.SEED_PATTERN_FA3ALA),
            form_profile=self._make_form(),
        )
        result_intensive = SemanticTransferEngine.transfer(
            root_kernel=self._make_root(),
            pattern_transform=self._make_pattern(seed_data.SEED_PATTERN_FA33ALA),
            form_profile=self._make_form(),
        )
        # The intensive pattern should shift meaning more than the neutral
        assert result_intensive.output_kernel != result_neutral.output_kernel

    def test_transfer_with_context_delta(self):
        ctx = SemanticVector(values=tuple(0.1 for _ in range(13)))
        result = SemanticTransferEngine.transfer(
            root_kernel=self._make_root(),
            pattern_transform=self._make_pattern(),
            form_profile=self._make_form(),
            context_delta=ctx,
        )
        assert result.output_kernel.dim > 0

    def test_transfer_compatibility_score(self):
        result = SemanticTransferEngine.transfer(
            root_kernel=self._make_root(),
            pattern_transform=self._make_pattern(),
            form_profile=self._make_form(),
        )
        assert 0.0 <= result.compatibility_score <= 1.0

    def test_transfer_equation_values(self):
        """Verify K_F = W_r·r + W_p·p + W_f·f + Δ_ctx with default weights."""
        root = self._make_root()
        pat = self._make_pattern(seed_data.SEED_PATTERN_FA33ALA)
        form = self._make_form()

        result = SemanticTransferEngine.transfer(
            root_kernel=root,
            pattern_transform=pat,
            form_profile=form,
        )

        # Manual computation with default weights (0.5, 0.3, 0.15, 0.05)
        out_dim = 13  # max of 13, 12, 9
        r_vals = root.semantic_vector.values + (0.0,) * 0  # already 13
        p_vals = pat.semantic_transform_vector.values + (0.0,)  # 12 → 13
        f_vals = form.form_semantic_vector.values + (0.0,) * 4  # 9 → 13

        expected = tuple(
            0.5 * r_vals[i] + 0.3 * p_vals[i] + 0.15 * f_vals[i] + 0.05 * 0.0
            for i in range(out_dim)
        )

        for i in range(out_dim):
            assert result.output_kernel.values[i] == pytest.approx(
                expected[i], abs=1e-9
            )


# ===========================================================================
# EconomyOptimizer tests
# ===========================================================================


class TestEconomyOptimizer:
    """Tests for the EconomyOptimizer."""

    def _make_result(self, morph_cost=0.0, compat=1.0, transform=0.8):
        return SemanticTransferResult(
            transfer_id="test",
            pattern_transform=PatternSemanticTransform(
                morphological_cost=morph_cost,
            ),
            compatibility_score=compat,
            transformation_score=transform,
        )

    def test_compute_cost_low(self):
        result = self._make_result(morph_cost=0.0, compat=1.0, transform=1.0)
        cost = EconomyOptimizer.compute_cost(result)
        assert cost.total == pytest.approx(0.0)

    def test_compute_cost_high(self):
        result = self._make_result(morph_cost=1.0, compat=0.0, transform=0.0)
        cost = EconomyOptimizer.compute_cost(result)
        assert cost.total > 2.0

    def test_select_optimal_empty(self):
        assert EconomyOptimizer.select_optimal([]) is None

    def test_select_optimal_single(self):
        r = self._make_result()
        assert EconomyOptimizer.select_optimal([r]) is r

    def test_select_optimal_picks_cheapest(self):
        cheap = self._make_result(morph_cost=0.1, compat=1.0, transform=0.9)
        expensive = self._make_result(morph_cost=1.0, compat=0.0, transform=0.1)
        assert EconomyOptimizer.select_optimal([expensive, cheap]) is cheap

    def test_semantic_cost_total(self):
        cost = SemanticCost(
            phonological_cost=1.0,
            morphological_cost=2.0,
            cognitive_cost=3.0,
            semantic_ambiguity_cost=4.0,
        )
        assert cost.total == pytest.approx(10.0)


# ===========================================================================
# SemanticKernelClosureEngine tests
# ===========================================================================


class TestSemanticKernelClosureEngine:
    """Tests for the SemanticKernelClosureEngine."""

    def _make_full_result(self):
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
        return SemanticTransferEngine.transfer(
            root_kernel=root,
            pattern_transform=pat,
            form_profile=form,
        )

    def test_closure_passes_valid_result(self):
        result = self._make_full_result()
        gates = SemanticKernelClosureEngine.close(result)
        assert all(g.passed for g in gates)
        assert result.closure is ClosureStatus.CLOSED

    def test_closure_blocks_incompatible(self):
        """A result with empty root should fail compatibility."""
        result = SemanticTransferResult(
            root_kernel=RootSemanticKernel(),
            pattern_transform=PatternSemanticTransform(),
            form_profile=FormSemanticProfile(),
        )
        gates = SemanticKernelClosureEngine.close(result)
        assert any(not g.passed for g in gates)
        assert result.closure is not ClosureStatus.CLOSED

    def test_closure_suspends_incomplete(self):
        """A result with valid root+pattern but empty form should suspend."""
        root = RootKernelBuilder.build(
            root_text="ك ت ب",
            semantic_values=seed_data.SEED_ROOT_KTB,
        )
        pat = PatternTransformBuilder.build(
            pattern_code="فَعَلَ",
            transform_values=seed_data.SEED_PATTERN_FA3ALA,
        )
        result = SemanticTransferEngine.transfer(
            root_kernel=root,
            pattern_transform=pat,
            form_profile=FormSemanticProfile(),  # empty form
        )
        gates = SemanticKernelClosureEngine.close(result)
        assert any(not g.passed for g in gates)
        assert result.closure is ClosureStatus.SUSPENDED


# ===========================================================================
# Enum tests
# ===========================================================================


class TestEnums:
    """Tests for the semantic enumerations."""

    def test_semantic_dimension_count(self):
        assert len(SemanticDimension) == 13

    def test_pattern_semantic_dimension_count(self):
        assert len(PatternSemanticDimension) == 12

    def test_form_semantic_dimension_count(self):
        assert len(FormSemanticDimension) == 9

    def test_compatibility_values(self):
        assert CompatibilityStatus.COMPATIBLE is not None
        assert CompatibilityStatus.INCOMPATIBLE is not None
        assert CompatibilityStatus.PARTIAL is not None
