"""Tests for the weight closure pipeline (Layer 4)."""

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_singular import (
    Definiteness,
    DerivationKind,
    Gender,
    StabilityKind,
    WordCategory,
)
from arabic_engine.core.enums_weight import (
    InflectionKind,
    WeightEligibility,
)
from arabic_engine.core.types_singular import (
    PreU0,
    SingularConceptual,
    SingularInformational,
    SingularPerceptual,
    SingularUnit,
)
from arabic_engine.core.types_weight import WeightRecord, WeightedUnit

from arabic_engine.singular.closure import SingularClosureEngine
from arabic_engine.weight.mizan import MizanClassifier
from arabic_engine.weight.legality import WeightLegalityGate
from arabic_engine.weight.derivation import DerivationEligibilityGate
from arabic_engine.weight.closure import WeightClosureEngine


def _make_closed_singular() -> SingularUnit:
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
            word_category=WordCategory.FI3L,
            definiteness=Definiteness.INDEFINITE,
            gender=Gender.MASCULINE,
            derivation=DerivationKind.MUSHTAQ,
        ),
    )
    SingularClosureEngine.close_all(unit)
    assert unit.singular_closed
    return unit


def test_mizan_classifies_verb():
    unit = _make_closed_singular()
    record = MizanClassifier.classify(unit, pattern="فَعَلَ", root="ك ت ب")
    assert record.eligibility is WeightEligibility.ELIGIBLE
    assert record.pattern == "فَعَلَ"


def test_mizan_rejects_particle():
    unit = SingularUnit()
    unit.conceptual.word_category = WordCategory.HARF
    record = MizanClassifier.classify(unit)
    assert record.eligibility is WeightEligibility.NOT_ELIGIBLE


def test_legality_rejects_ineligible():
    record = WeightRecord()
    result = WeightLegalityGate.evaluate(record)
    assert result.verdict is GateVerdict.REJECT


def test_legality_suspends_no_inflection():
    record = WeightRecord(eligibility=WeightEligibility.ELIGIBLE)
    result = WeightLegalityGate.evaluate(record)
    assert result.verdict is GateVerdict.SUSPEND


def test_legality_passes_complete():
    record = WeightRecord(
        eligibility=WeightEligibility.ELIGIBLE,
        inflection=InflectionKind.MU3RAB,
        derivation_legality=DerivationKind.MUSHTAQ,
    )
    result = WeightLegalityGate.evaluate(record)
    assert result.passed


def test_derivation_rejects_no_structural_elig():
    record = WeightRecord(
        eligibility=WeightEligibility.ELIGIBLE,
        inflection=InflectionKind.MU3RAB,
        derivation_legality=DerivationKind.MUSHTAQ,
    )
    result = DerivationEligibilityGate.evaluate(record)
    assert result.verdict is GateVerdict.SUSPEND


def test_weight_full_closure():
    unit = _make_closed_singular()
    record = WeightRecord(
        eligibility=WeightEligibility.ELIGIBLE,
        pattern="فَعَلَ",
        root="ك ت ب",
        inflection=InflectionKind.MU3RAB,
        derivation_legality=DerivationKind.MUSHTAQ,
        verb_eligible=True,
    )
    weighted = WeightedUnit(singular=unit, weight=record)
    results = WeightClosureEngine.close(weighted)
    assert all(r.passed for r in results)
    assert weighted.fully_closed


def test_weight_rejects_unclosed_singular():
    unit = SingularUnit()  # not closed
    record = WeightRecord(
        eligibility=WeightEligibility.ELIGIBLE,
        inflection=InflectionKind.MU3RAB,
        derivation_legality=DerivationKind.MUSHTAQ,
        verb_eligible=True,
    )
    weighted = WeightedUnit(singular=unit, weight=record)
    results = WeightClosureEngine.close(weighted)
    assert results[0].verdict is GateVerdict.REJECT
