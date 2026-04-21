"""Focused tests for currently uncovered/undercovered branches."""

from arabic_engine.core.enums_domain import RelationKind, RoleTag
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_semantic import CompatibilityStatus
from arabic_engine.core.types_composition import CompositionRelation, RoleAssignment
from arabic_engine.core.types_gate import GateResult
from arabic_engine.core.types_judgement import Judgement
from arabic_engine.core.types_semantic import (
    FormSemanticProfile,
    PatternSemanticTransform,
    RootSemanticKernel,
    SemanticTransferResult,
    SemanticVector,
)
from arabic_engine.core.types_weight import WeightRecord, WeightedUnit
from arabic_engine.judgement.closure import JudgementClosureEngine
from arabic_engine.judgement.transition import JudgementTransitionEngine
from arabic_engine.semantic_kernel.compatibility import CompatibilityChecker
from arabic_engine.semantic_kernel.transfer import SemanticTransferEngine

ROOT_VECTOR_DIM = 13
PATTERN_VECTOR_DIM = 12
FORM_VECTOR_DIM = 9


def _weighted_with_output_dim(values: tuple[float, ...]) -> WeightedUnit:
    transfer = SemanticTransferResult(output_kernel=SemanticVector(values=values))
    return WeightedUnit(weight=WeightRecord(semantic_transfer=transfer))


def _minimal_transfer_inputs() -> tuple[RootSemanticKernel, PatternSemanticTransform, FormSemanticProfile]:
    root = RootSemanticKernel(
        semantic_vector=SemanticVector(values=tuple(1.0 for _ in range(ROOT_VECTOR_DIM)))
    )
    pattern = PatternSemanticTransform(
        semantic_transform_vector=SemanticVector(values=tuple(1.0 for _ in range(PATTERN_VECTOR_DIM)))
    )
    form = FormSemanticProfile(
        form_semantic_vector=SemanticVector(values=tuple(1.0 for _ in range(FORM_VECTOR_DIM)))
    )
    return root, pattern, form


def test_judgement_closure_sets_closed_on_pass(monkeypatch):
    judgement = Judgement()
    expected = GateResult(verdict=GateVerdict.PASS, layer=Layer.JUDGEMENT)
    monkeypatch.setattr(
        JudgementTransitionEngine,
        "validate_transition",
        staticmethod(lambda _: expected),
    )

    result = JudgementClosureEngine.close(judgement)

    assert result is expected
    assert judgement.closure is ClosureStatus.CLOSED


def test_judgement_closure_sets_suspended_on_suspend(monkeypatch):
    judgement = Judgement()
    expected = GateResult(verdict=GateVerdict.SUSPEND, layer=Layer.JUDGEMENT)
    monkeypatch.setattr(
        JudgementTransitionEngine,
        "validate_transition",
        staticmethod(lambda _: expected),
    )

    JudgementClosureEngine.close(judgement)

    assert judgement.closure is ClosureStatus.SUSPENDED


def test_judgement_closure_sets_blocked_on_reject(monkeypatch):
    judgement = Judgement()
    expected = GateResult(verdict=GateVerdict.REJECT, layer=Layer.JUDGEMENT)
    monkeypatch.setattr(
        JudgementTransitionEngine,
        "validate_transition",
        staticmethod(lambda _: expected),
    )

    JudgementClosureEngine.close(judgement)

    assert judgement.closure is ClosureStatus.BLOCKED


def test_composition_semantic_compatibility_returns_one_for_zero_dim_outputs():
    relation = CompositionRelation(
        kind=RelationKind.ASNADI,
        roles=[
            RoleAssignment(unit=_weighted_with_output_dim(()), role=RoleTag.MUSNAD),
            RoleAssignment(unit=_weighted_with_output_dim(()), role=RoleTag.MUSNAD_ILAYH),
        ],
    )

    assert relation.semantic_compatibility_score == 1.0


def test_composition_semantic_compatibility_returns_half_score_on_dim_mismatch():
    relation = CompositionRelation(
        kind=RelationKind.ASNADI,
        roles=[
            RoleAssignment(unit=_weighted_with_output_dim((1.0, 0.0)), role=RoleTag.MUSNAD),
            RoleAssignment(unit=_weighted_with_output_dim((1.0, 0.0, 1.0)), role=RoleTag.MUSNAD_ILAYH),
        ],
    )

    assert relation.semantic_compatibility_score == 0.5


def test_transfer_maps_partial_compatibility_to_half_score(monkeypatch):
    root, pattern, form = _minimal_transfer_inputs()
    monkeypatch.setattr(
        CompatibilityChecker,
        "check_root_pattern",
        staticmethod(lambda *_args, **_kwargs: CompatibilityStatus.PARTIAL),
    )

    result = SemanticTransferEngine.transfer(root, pattern, form)

    assert result.compatibility_score == 0.5


def test_transfer_maps_incompatible_to_zero_score(monkeypatch):
    root, pattern, form = _minimal_transfer_inputs()
    monkeypatch.setattr(
        CompatibilityChecker,
        "check_root_pattern",
        staticmethod(lambda *_args, **_kwargs: CompatibilityStatus.INCOMPATIBLE),
    )

    result = SemanticTransferEngine.transfer(root, pattern, form)

    assert result.compatibility_score == 0.0


def test_transfer_project_pads_and_truncates():
    padded = SemanticTransferEngine._project(SemanticVector(values=(1.0, 2.0)), target_dim=4)
    truncated = SemanticTransferEngine._project(
        SemanticVector(values=(1.0, 2.0, 3.0, 4.0)),
        target_dim=2,
    )

    assert padded.values == (1.0, 2.0, 0.0, 0.0)
    assert truncated.values == (1.0, 2.0)
