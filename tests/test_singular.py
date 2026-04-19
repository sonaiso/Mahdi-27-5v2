"""Tests for the singular closure pipeline (Layers 0-3)."""

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_singular import (
    Definiteness,
    DerivationKind,
    Gender,
    StabilityKind,
    WordCategory,
)
from arabic_engine.core.types_singular import (
    PreU0,
    SingularConceptual,
    SingularInformational,
    SingularPerceptual,
    SingularUnit,
)
from arabic_engine.singular.perception import PerceptionGate
from arabic_engine.singular.information import InformationGate
from arabic_engine.singular.concept import ConceptGate
from arabic_engine.singular.closure import SingularClosureEngine


# ---------------------------------------------------------------------------
# Perception gate tests
# ---------------------------------------------------------------------------


def test_perception_rejects_empty_trace():
    p = SingularPerceptual()
    result = PerceptionGate.evaluate(p)
    assert result.verdict is GateVerdict.REJECT
    assert result.missing_condition == "sensory_trace"


def test_perception_suspends_without_stability():
    p = SingularPerceptual(sensory_trace="كتب")
    result = PerceptionGate.evaluate(p)
    assert result.verdict is GateVerdict.SUSPEND


def test_perception_passes_complete():
    p = SingularPerceptual(sensory_trace="كتب", stability=StabilityKind.TRANSFORMING)
    result = PerceptionGate.evaluate(p)
    assert result.passed


def test_perception_close_sets_closure():
    p = SingularPerceptual(sensory_trace="كتب", stability=StabilityKind.STABLE)
    PerceptionGate.close(p)
    assert p.closure is ClosureStatus.CLOSED


# ---------------------------------------------------------------------------
# Information gate tests
# ---------------------------------------------------------------------------


def test_information_rejects_unbound():
    info = SingularInformational()
    result = InformationGate.evaluate(info)
    assert result.verdict is GateVerdict.REJECT


def test_information_suspends_no_potentials():
    info = SingularInformational(prior_knowledge_bound=True)
    result = InformationGate.evaluate(info)
    assert result.verdict is GateVerdict.SUSPEND


def test_information_passes_with_potential():
    info = SingularInformational(
        prior_knowledge_bound=True, agency_potential=True
    )
    result = InformationGate.evaluate(info)
    assert result.passed


# ---------------------------------------------------------------------------
# Concept gate tests
# ---------------------------------------------------------------------------


def test_concept_rejects_no_category():
    c = SingularConceptual()
    result = ConceptGate.evaluate(c)
    assert result.verdict is GateVerdict.REJECT


def test_concept_suspends_no_definiteness():
    c = SingularConceptual(word_category=WordCategory.ISM)
    result = ConceptGate.evaluate(c)
    assert result.verdict is GateVerdict.SUSPEND
    assert result.missing_condition == "definiteness"


def test_concept_passes_complete():
    c = SingularConceptual(
        word_category=WordCategory.ISM,
        definiteness=Definiteness.DEFINITE,
        gender=Gender.MASCULINE,
        derivation=DerivationKind.MUSHTAQ,
    )
    result = ConceptGate.evaluate(c)
    assert result.passed


# ---------------------------------------------------------------------------
# Full singular closure tests
# ---------------------------------------------------------------------------


def _make_complete_unit() -> SingularUnit:
    """Create a fully-populated singular unit."""
    return SingularUnit(
        pre_u0=PreU0(
            codepoint=0x0643,
            char="ك",
            is_present=True,
            is_distinguishable=True,
            is_admissible=True,
        ),
        perceptual=SingularPerceptual(
            sensory_trace="كتب",
            stability=StabilityKind.TRANSFORMING,
        ),
        informational=SingularInformational(
            prior_knowledge_bound=True,
            agency_potential=True,
            temporal_potential=True,
        ),
        conceptual=SingularConceptual(
            word_category=WordCategory.FI3L,
            definiteness=Definiteness.INDEFINITE,
            gender=Gender.MASCULINE,
            derivation=DerivationKind.MUSHTAQ,
        ),
    )


def test_singular_full_closure():
    unit = _make_complete_unit()
    results = SingularClosureEngine.close_all(unit)
    assert all(r.passed for r in results)
    assert unit.singular_closed


def test_singular_stops_at_first_failure():
    unit = SingularUnit(
        pre_u0=PreU0(
            codepoint=0x0643,
            char="ك",
            is_present=True,
            is_distinguishable=True,
            is_admissible=True,
        ),
        perceptual=SingularPerceptual(),  # missing sensory_trace
    )
    results = SingularClosureEngine.close_all(unit)
    # Layer 0 passes, Layer 1 fails
    assert results[0].passed
    assert not results[1].passed
    assert not unit.singular_closed


def test_singular_pre_u0_failure():
    unit = SingularUnit()  # all defaults — is_present=False
    results = SingularClosureEngine.close_all(unit)
    assert len(results) == 1
    assert results[0].verdict is GateVerdict.REJECT
