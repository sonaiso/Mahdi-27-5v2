"""Tests for contracts (adjacency, anti-jump, invariants, state mapping)."""

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.types_weight import WeightedUnit

from arabic_engine.contracts.adjacency import AdjacencyContract
from arabic_engine.contracts.anti_jump import AntiJumpContract
from arabic_engine.contracts.invariants import InvariantChecker
from arabic_engine.contracts.state_mapping import StateMapper


# ---------------------------------------------------------------------------
# Adjacency contract tests
# ---------------------------------------------------------------------------


def test_adjacency_passes_with_all_predecessors_closed():
    closed = {
        Layer.PRE_U0_ADMISSIBILITY,
        Layer.SINGULAR_PERCEPTUAL,
        Layer.SINGULAR_INFORMATIONAL,
        Layer.SINGULAR_CONCEPTUAL,
    }
    result = AdjacencyContract.check(Layer.WEIGHT_MIZAN, closed)
    assert result.passed


def test_adjacency_rejects_missing_predecessor():
    closed = {
        Layer.PRE_U0_ADMISSIBILITY,
        Layer.SINGULAR_PERCEPTUAL,
        # missing SINGULAR_INFORMATIONAL
        Layer.SINGULAR_CONCEPTUAL,
    }
    result = AdjacencyContract.check(Layer.WEIGHT_MIZAN, closed)
    assert result.verdict is GateVerdict.REJECT


def test_adjacency_first_layer_always_passes():
    result = AdjacencyContract.check(Layer.PRE_U0_ADMISSIBILITY, set())
    assert result.passed


# ---------------------------------------------------------------------------
# Anti-jump contract tests
# ---------------------------------------------------------------------------


def test_anti_jump_allows_adjacent():
    result = AntiJumpContract.check_transition(
        Layer.SINGULAR_CONCEPTUAL, Layer.WEIGHT_MIZAN
    )
    assert result.passed


def test_anti_jump_rejects_skip():
    result = AntiJumpContract.check_transition(
        Layer.SINGULAR_PERCEPTUAL, Layer.WEIGHT_MIZAN
    )
    assert result.verdict is GateVerdict.REJECT


def test_anti_jump_rejects_backward():
    result = AntiJumpContract.check_transition(
        Layer.WEIGHT_MIZAN, Layer.SINGULAR_PERCEPTUAL
    )
    assert result.verdict is GateVerdict.REJECT


# ---------------------------------------------------------------------------
# Invariant checker tests
# ---------------------------------------------------------------------------


def test_invariant_passes_default_unit():
    unit = WeightedUnit()  # both unclosed — valid state
    results = InvariantChecker.check_weighted_unit(unit)
    assert all(r.passed for r in results)


def test_invariant_detects_weight_closed_without_singular():
    unit = WeightedUnit()
    unit.weight.closure = ClosureStatus.CLOSED  # violate invariant
    results = InvariantChecker.check_weighted_unit(unit)
    assert any(r.verdict is GateVerdict.REJECT for r in results)


# ---------------------------------------------------------------------------
# State mapper tests
# ---------------------------------------------------------------------------


def test_verdict_to_closure_mapping():
    assert StateMapper.verdict_to_closure(GateVerdict.PASS) is ClosureStatus.CLOSED
    assert StateMapper.verdict_to_closure(GateVerdict.REJECT) is ClosureStatus.BLOCKED
    assert StateMapper.verdict_to_closure(GateVerdict.SUSPEND) is ClosureStatus.SUSPENDED


def test_closure_to_verdict_mapping():
    assert StateMapper.closure_to_verdict(ClosureStatus.CLOSED) is GateVerdict.PASS
    assert StateMapper.closure_to_verdict(ClosureStatus.BLOCKED) is GateVerdict.REJECT
    assert StateMapper.closure_to_verdict(ClosureStatus.OPEN) is GateVerdict.SUSPEND
