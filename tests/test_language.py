"""
Tests for the Language layer — the transcendental container (الوعاء الترنسندنتالي).

Tests cover:
  - Category registry (12 categories → 12 linguistic positions)
  - Constraint system (rank confusion prevention)
  - Predication engine (valid subject–predicate combinations)
  - Reference system (pronoun, demonstrative, relative bindings)
  - Testability interface (truth-evaluability of judgements)
  - Feedback loop (reverse flow from language to cognition)
  - Container builder (full Lang_tr construction)
  - Language closure engine (gate evaluation and closure)
  - Master chain integration (process_language method)
"""

import pytest

from arabic_engine.core.enums_gate import ClosureStatus, GateVerdict
from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.enums_language import (
    CognitiveCategory,
    ContainerFunction,
    ContainerValidityStatus,
    LinguisticPosition,
    RankConfusionKind,
)
from arabic_engine.core.types_language import (
    CategorySlot,
    ConstraintRecord,
    FeedbackRecord,
    PredicationRule,
    ReferenceBinding,
    TestabilityResult,
    TranscendentalContainer,
)

from arabic_engine.language.categories import CategoryRegistry
from arabic_engine.language.constraints import ConstraintSystem
from arabic_engine.language.predication import PredicationEngine
from arabic_engine.language.reference import ReferenceSystem
from arabic_engine.language.testability import TestabilityInterface
from arabic_engine.language.feedback import FeedbackLoop
from arabic_engine.language.container import TranscendentalContainerBuilder
from arabic_engine.language.closure import LanguageGate, LanguageClosureEngine


# ===================================================================
# 1. Category Registry Tests
# ===================================================================


class TestCategoryRegistry:
    """Tests for the category registry — maps 𝒦 to linguistic positions."""

    def test_build_all_slots_returns_12(self):
        """All 12 cognitive categories must be present."""
        slots = CategoryRegistry.build_all_slots()
        assert len(slots) == 12

    def test_all_categories_covered(self):
        """Every CognitiveCategory must appear in the slots."""
        slots = CategoryRegistry.build_all_slots()
        categories = {s.category for s in slots}
        assert categories == set(CognitiveCategory)

    def test_all_slots_are_valid(self):
        """All canonical slots must have VALID status."""
        slots = CategoryRegistry.build_all_slots()
        for slot in slots:
            assert slot.validity is ContainerValidityStatus.VALID

    def test_all_slots_have_labels(self):
        """Every slot must have both Arabic and English labels."""
        slots = CategoryRegistry.build_all_slots()
        for slot in slots:
            assert slot.label_ar, f"Missing Arabic label for {slot.category}"
            assert slot.label_en, f"Missing English label for {slot.category}"

    def test_entity_maps_to_ism(self):
        """ENTITY must map to ISM (الاسم)."""
        pos = CategoryRegistry.get_position(CognitiveCategory.ENTITY)
        assert pos is LinguisticPosition.ISM

    def test_event_maps_to_fi3l(self):
        """EVENT must map to FI3L_MASDAR (الفعل/المصدر)."""
        pos = CategoryRegistry.get_position(CognitiveCategory.EVENT)
        assert pos is LinguisticPosition.FI3L_MASDAR

    def test_quality_maps_to_na3t(self):
        """QUALITY must map to NA3T_SIFA_HAL."""
        pos = CategoryRegistry.get_position(CognitiveCategory.QUALITY)
        assert pos is LinguisticPosition.NA3T_SIFA_HAL

    def test_negation_maps_to_nafy(self):
        """NEGATION must map to ADAWAT_NAFY."""
        pos = CategoryRegistry.get_position(CognitiveCategory.NEGATION)
        assert pos is LinguisticPosition.ADAWAT_NAFY

    def test_reference_maps_to_damir(self):
        """REFERENCE must map to DAMIR_ISHARA_MAWSUL."""
        pos = CategoryRegistry.get_position(CognitiveCategory.REFERENCE)
        assert pos is LinguisticPosition.DAMIR_ISHARA_MAWSUL

    def test_reverse_lookup(self):
        """get_category_for_position must return the right category."""
        cat = CategoryRegistry.get_category_for_position(LinguisticPosition.ISM)
        assert cat is CognitiveCategory.ENTITY

    def test_reverse_lookup_none_for_unknown(self):
        """get_category_for_position returns None for unmapped positions."""
        # All 12 positions are mapped, so this is a completeness check
        for pos in LinguisticPosition:
            assert CategoryRegistry.get_category_for_position(pos) is not None

    def test_is_comprehensive(self):
        """All 12 slots make a comprehensive set."""
        slots = CategoryRegistry.build_all_slots()
        assert CategoryRegistry.is_comprehensive(slots)

    def test_is_not_comprehensive_when_missing(self):
        """Removing one slot breaks comprehensiveness."""
        slots = CategoryRegistry.build_all_slots()[:-1]  # remove last
        assert not CategoryRegistry.is_comprehensive(slots)

    def test_missing_categories(self):
        """Missing categories are correctly identified."""
        slots = CategoryRegistry.build_all_slots()[:10]  # only 10
        missing = CategoryRegistry.missing_categories(slots)
        assert len(missing) == 2

    def test_canonical_map_size(self):
        """The canonical map must have exactly 12 entries."""
        assert CategoryRegistry.canonical_map_size() == 12


# ===================================================================
# 2. Constraint System Tests
# ===================================================================


class TestConstraintSystem:
    """Tests for the constraint system — prevents rank confusion."""

    def test_valid_canonical_slots(self):
        """All canonical slots pass constraint validation."""
        slots = CategoryRegistry.build_all_slots()
        records = ConstraintSystem.validate_all_slots(slots)
        assert not ConstraintSystem.has_violations(records)

    def test_entity_in_quality_position_is_violated(self):
        """ENTITY in NA3T_SIFA_HAL is a rank confusion."""
        slot = CategorySlot(
            category=CognitiveCategory.ENTITY,
            position=LinguisticPosition.NA3T_SIFA_HAL,
        )
        record = ConstraintSystem.validate_slot(slot)
        assert record.is_violated
        assert record.confusion_kind is RankConfusionKind.ENTITY_AS_QUALITY

    def test_quality_in_ism_position_is_violated(self):
        """QUALITY in ISM is a rank confusion."""
        slot = CategorySlot(
            category=CognitiveCategory.QUALITY,
            position=LinguisticPosition.ISM,
        )
        record = ConstraintSystem.validate_slot(slot)
        assert record.is_violated
        assert record.confusion_kind is RankConfusionKind.QUALITY_AS_ENTITY

    def test_event_in_ism_position_is_violated(self):
        """EVENT in ISM is a rank confusion — treating event as static."""
        slot = CategorySlot(
            category=CognitiveCategory.EVENT,
            position=LinguisticPosition.ISM,
        )
        record = ConstraintSystem.validate_slot(slot)
        assert record.is_violated
        assert record.confusion_kind is RankConfusionKind.EVENT_AS_STATIC

    def test_cause_in_shart_position_is_violated(self):
        """CAUSE in ADAWAT_SHART is a rank confusion."""
        slot = CategorySlot(
            category=CognitiveCategory.CAUSE,
            position=LinguisticPosition.ADAWAT_SHART,
        )
        record = ConstraintSystem.validate_slot(slot)
        assert record.is_violated
        assert record.confusion_kind is RankConfusionKind.CAUSE_AS_CONDITION

    def test_condition_in_sabab_position_is_violated(self):
        """CONDITION in ADAWAT_SABAB is a rank confusion."""
        slot = CategorySlot(
            category=CognitiveCategory.CONDITION,
            position=LinguisticPosition.ADAWAT_SABAB,
        )
        record = ConstraintSystem.validate_slot(slot)
        assert record.is_violated
        assert record.confusion_kind is RankConfusionKind.CAUSE_AS_CONDITION

    def test_valid_slot_no_violation(self):
        """A properly placed category has no violation."""
        slot = CategorySlot(
            category=CognitiveCategory.ENTITY,
            position=LinguisticPosition.ISM,
        )
        record = ConstraintSystem.validate_slot(slot)
        assert not record.is_violated
        assert record.confusion_kind is None

    def test_get_violations(self):
        """get_violations returns only violated records."""
        slots = [
            CategorySlot(
                category=CognitiveCategory.ENTITY,
                position=LinguisticPosition.ISM,
            ),
            CategorySlot(
                category=CognitiveCategory.ENTITY,
                position=LinguisticPosition.NA3T_SIFA_HAL,
            ),
        ]
        records = ConstraintSystem.validate_all_slots(slots)
        violations = ConstraintSystem.get_violations(records)
        assert len(violations) == 1

    def test_compute_validity_valid(self):
        """compute_validity returns VALID for a well-placed slot."""
        slot = CategorySlot(
            category=CognitiveCategory.ENTITY,
            position=LinguisticPosition.ISM,
        )
        assert ConstraintSystem.compute_validity(slot) is ContainerValidityStatus.VALID

    def test_compute_validity_invalid(self):
        """compute_validity returns INVALID for a mis-placed slot."""
        slot = CategorySlot(
            category=CognitiveCategory.ENTITY,
            position=LinguisticPosition.NA3T_SIFA_HAL,
        )
        assert ConstraintSystem.compute_validity(slot) is ContainerValidityStatus.INVALID


# ===================================================================
# 3. Predication Engine Tests
# ===================================================================


class TestPredicationEngine:
    """Tests for the predication engine — valid subject–predicate rules."""

    def test_entity_is_valid_subject(self):
        """ENTITY can serve as subject."""
        assert PredicationEngine.is_valid_subject(CognitiveCategory.ENTITY)

    def test_reference_is_valid_subject(self):
        """REFERENCE can serve as subject (pronouns)."""
        assert PredicationEngine.is_valid_subject(CognitiveCategory.REFERENCE)

    def test_event_is_not_subject(self):
        """EVENT cannot serve as subject."""
        assert not PredicationEngine.is_valid_subject(CognitiveCategory.EVENT)

    def test_quality_is_valid_predicate(self):
        """QUALITY can serve as predicate."""
        assert PredicationEngine.is_valid_predicate(CognitiveCategory.QUALITY)

    def test_event_is_valid_predicate(self):
        """EVENT can serve as predicate."""
        assert PredicationEngine.is_valid_predicate(CognitiveCategory.EVENT)

    def test_negation_is_not_predicate(self):
        """NEGATION cannot serve as predicate."""
        assert not PredicationEngine.is_valid_predicate(CognitiveCategory.NEGATION)

    def test_valid_predication(self):
        """ENTITY ← QUALITY is a valid predication."""
        rule = PredicationEngine.check_predication(
            CognitiveCategory.ENTITY, CognitiveCategory.QUALITY,
        )
        assert rule.is_permitted
        assert rule.rule_description

    def test_invalid_subject(self):
        """NEGATION ← QUALITY is invalid (NEGATION can't be subject)."""
        rule = PredicationEngine.check_predication(
            CognitiveCategory.NEGATION, CognitiveCategory.QUALITY,
        )
        assert not rule.is_permitted

    def test_invalid_predicate(self):
        """ENTITY ← NEGATION is invalid (NEGATION can't be predicate)."""
        rule = PredicationEngine.check_predication(
            CognitiveCategory.ENTITY, CognitiveCategory.NEGATION,
        )
        assert not rule.is_permitted

    def test_build_all_rules(self):
        """All valid subject–predicate rules are generated."""
        rules = PredicationEngine.build_all_rules()
        # Exactly 2 subject categories × 6 predicate categories = 12 rules
        assert len(rules) == 12
        assert all(isinstance(r, PredicationRule) for r in rules)
        assert all(r.is_permitted for r in rules)

    def test_nominal_predication(self):
        """ENTITY ← ENTITY is valid (nominal predicate — الجملة الاسمية)."""
        rule = PredicationEngine.check_predication(
            CognitiveCategory.ENTITY, CognitiveCategory.ENTITY,
        )
        assert rule.is_permitted


# ===================================================================
# 4. Reference System Tests
# ===================================================================


class TestReferenceSystem:
    """Tests for the reference system — discourse binding."""

    def test_entity_can_be_referent(self):
        """ENTITY is a valid referent."""
        assert ReferenceSystem.can_refer_to(CognitiveCategory.ENTITY)

    def test_negation_cannot_be_referent(self):
        """NEGATION is not a valid referent."""
        assert not ReferenceSystem.can_refer_to(CognitiveCategory.NEGATION)

    def test_bind_pronoun(self):
        """Pronoun binding to ENTITY is resolved."""
        binding = ReferenceSystem.bind_pronoun(
            CognitiveCategory.ENTITY, "هو",
        )
        assert binding.is_resolved
        assert binding.reference_type == "ضمير"
        assert binding.referent_label == "هو"

    def test_bind_demonstrative(self):
        """Demonstrative binding to ENTITY is resolved."""
        binding = ReferenceSystem.bind_demonstrative(
            CognitiveCategory.ENTITY, "هذا",
        )
        assert binding.is_resolved
        assert binding.reference_type == "إشارة"

    def test_bind_relative(self):
        """Relative pronoun binding to EVENT is resolved."""
        binding = ReferenceSystem.bind_relative(
            CognitiveCategory.EVENT, "الذي",
        )
        assert binding.is_resolved
        assert binding.reference_type == "موصول"

    def test_unresolved_binding(self):
        """Binding to NEGATION is unresolved."""
        binding = ReferenceSystem.bind(
            CognitiveCategory.NEGATION, "ضمير",
        )
        assert not binding.is_resolved

    def test_all_resolved(self):
        """all_resolved returns True when all bindings are resolved."""
        bindings = [
            ReferenceSystem.bind_pronoun(CognitiveCategory.ENTITY),
            ReferenceSystem.bind_demonstrative(CognitiveCategory.QUALITY),
        ]
        assert ReferenceSystem.all_resolved(bindings)

    def test_not_all_resolved(self):
        """all_resolved returns False when some are unresolved."""
        bindings = [
            ReferenceSystem.bind_pronoun(CognitiveCategory.ENTITY),
            ReferenceSystem.bind(CognitiveCategory.NEGATION, "ضمير"),
        ]
        assert not ReferenceSystem.all_resolved(bindings)

    def test_unresolved_bindings_filter(self):
        """unresolved_bindings returns only unresolved."""
        bindings = [
            ReferenceSystem.bind_pronoun(CognitiveCategory.ENTITY),
            ReferenceSystem.bind(CognitiveCategory.NEGATION, "ضمير"),
        ]
        unresolved = ReferenceSystem.unresolved_bindings(bindings)
        assert len(unresolved) == 1


# ===================================================================
# 5. Testability Interface Tests
# ===================================================================


class TestTestabilityInterface:
    """Tests for testability — truth/falsity evaluation."""

    def test_testable_predication(self):
        """ENTITY ← QUALITY yields a testable judgement."""
        rule = PredicationEngine.check_predication(
            CognitiveCategory.ENTITY, CognitiveCategory.QUALITY,
        )
        result = TestabilityInterface.evaluate_predication(rule)
        assert result.is_testable
        assert result.truth_evaluable
        assert not result.performative_only

    def test_invalid_predication_not_testable(self):
        """Invalid predication is not testable."""
        rule = PredicationRule(
            subject_category=CognitiveCategory.NEGATION,
            predicate_category=CognitiveCategory.QUALITY,
            is_permitted=False,
        )
        result = TestabilityInterface.evaluate_predication(rule)
        assert not result.is_testable

    def test_performative_predication(self):
        """ENTITY ← CONDITION is performative (إنشاء), not testable."""
        rule = PredicationRule(
            subject_category=CognitiveCategory.ENTITY,
            predicate_category=CognitiveCategory.CONDITION,
            is_permitted=True,
        )
        result = TestabilityInterface.evaluate_predication(rule)
        assert not result.is_testable
        assert result.performative_only

    def test_evaluate_all_slots(self):
        """Full canonical slots yield testable result."""
        slots = CategoryRegistry.build_all_slots()
        result = TestabilityInterface.evaluate_slots(slots)
        assert result.is_testable

    def test_evaluate_empty_slots(self):
        """Empty slots yield non-testable result."""
        result = TestabilityInterface.evaluate_slots([])
        assert not result.is_testable


# ===================================================================
# 6. Feedback Loop Tests
# ===================================================================


class TestFeedbackLoop:
    """Tests for the feedback loop — reverse flow to cognition."""

    def test_empty_container_no_feedback(self):
        """Empty container gets no feedback applied."""
        container = TranscendentalContainer()
        record = FeedbackLoop.apply(container)
        assert not record.clarification_applied
        assert not record.stabilization_applied
        assert not record.shared_rationality_enabled

    def test_clarification_with_slots(self):
        """Container with slots gets clarification applied."""
        container = TranscendentalContainer(
            category_slots=CategoryRegistry.build_all_slots(),
        )
        record = FeedbackLoop.apply(container)
        assert record.clarification_applied

    def test_stabilization_with_constraints(self):
        """Container with valid constraints gets stabilization."""
        slots = CategoryRegistry.build_all_slots()
        records = ConstraintSystem.validate_all_slots(slots)
        container = TranscendentalContainer(
            category_slots=slots,
            constraint_records=records,
        )
        record = FeedbackLoop.apply(container)
        assert record.stabilization_applied

    def test_shared_rationality_with_all_functions(self):
        """Container with all 5 functions enables shared rationality."""
        container = TranscendentalContainer(
            category_slots=CategoryRegistry.build_all_slots(),
            constraint_records=ConstraintSystem.validate_all_slots(
                CategoryRegistry.build_all_slots()
            ),
            active_functions=set(ContainerFunction),
        )
        record = FeedbackLoop.apply(container)
        assert record.shared_rationality_enabled

    def test_feedback_description_not_empty(self):
        """Feedback description is populated when feedback is applied."""
        container = TranscendentalContainer(
            category_slots=CategoryRegistry.build_all_slots(),
        )
        record = FeedbackLoop.apply(container)
        assert record.feedback_description


# ===================================================================
# 7. Container Builder Tests
# ===================================================================


class TestTranscendentalContainerBuilder:
    """Tests for the container builder — full Lang_tr construction."""

    def test_build_produces_container(self):
        """Builder produces a TranscendentalContainer."""
        container = TranscendentalContainerBuilder.build()
        assert isinstance(container, TranscendentalContainer)

    def test_build_is_comprehensive(self):
        """Built container is comprehensive (all 12 categories)."""
        container = TranscendentalContainerBuilder.build()
        assert container.is_comprehensive

    def test_build_is_preventive(self):
        """Built container is preventive (no rank confusion)."""
        container = TranscendentalContainerBuilder.build()
        assert container.is_preventive

    def test_build_has_all_functions(self):
        """Built container has all 5 container functions active."""
        container = TranscendentalContainerBuilder.build()
        assert container.active_functions == set(ContainerFunction)

    def test_build_has_12_slots(self):
        """Built container has exactly 12 category slots."""
        container = TranscendentalContainerBuilder.build()
        assert len(container.category_slots) == 12

    def test_build_has_predication_rules(self):
        """Built container has predication rules."""
        container = TranscendentalContainerBuilder.build()
        assert len(container.predication_rules) > 0

    def test_build_has_constraint_records(self):
        """Built container has constraint records."""
        container = TranscendentalContainerBuilder.build()
        assert len(container.constraint_records) > 0

    def test_build_has_testability(self):
        """Built container has testability results."""
        container = TranscendentalContainerBuilder.build()
        assert len(container.testability_results) > 0
        assert any(t.is_testable for t in container.testability_results)

    def test_build_has_feedback(self):
        """Built container has feedback loop applied."""
        container = TranscendentalContainerBuilder.build()
        assert container.feedback is not None
        assert container.feedback.clarification_applied

    def test_build_with_reference_bindings(self):
        """Builder accepts reference bindings."""
        bindings = [
            ReferenceSystem.bind_pronoun(CognitiveCategory.ENTITY, "هو"),
        ]
        container = TranscendentalContainerBuilder.build(
            reference_bindings=bindings,
        )
        assert len(container.reference_bindings) == 1

    def test_collection_score(self):
        """Collection score is 1.0 for a complete container."""
        container = TranscendentalContainerBuilder.build()
        assert container.collection_score == 1.0

    def test_is_complete(self):
        """Built container is complete (comprehensive + preventive)."""
        container = TranscendentalContainerBuilder.build()
        assert container.is_complete

    def test_constraint_violation_count_zero(self):
        """Built container has zero constraint violations."""
        container = TranscendentalContainerBuilder.build()
        assert container.constraint_violation_count == 0


# ===================================================================
# 8. Language Closure Engine Tests
# ===================================================================


class TestLanguageClosure:
    """Tests for the language gate and closure engine."""

    def test_gate_passes_for_complete_container(self):
        """Gate passes for a fully built container."""
        container = TranscendentalContainerBuilder.build()
        result = LanguageGate.evaluate(container)
        assert result.verdict is GateVerdict.PASS
        assert result.layer is Layer.LANGUAGE

    def test_gate_suspends_for_empty_container(self):
        """Gate suspends for an empty container (not comprehensive)."""
        container = TranscendentalContainer()
        result = LanguageGate.evaluate(container)
        assert result.verdict is GateVerdict.SUSPEND
        assert "غير جامع" in result.reason

    def test_gate_rejects_for_violated_container(self):
        """Gate rejects when rank confusion is present."""
        container = TranscendentalContainerBuilder.build()
        # Inject a violation
        from arabic_engine.core.types_language import ConstraintRecord
        container.constraint_records.append(ConstraintRecord(
            category=CognitiveCategory.ENTITY,
            confusion_kind=RankConfusionKind.ENTITY_AS_QUALITY,
            is_violated=True,
            violation_reason="test violation",
        ))
        result = LanguageGate.evaluate(container)
        assert result.verdict is GateVerdict.REJECT
        assert "خلط" in result.reason

    def test_gate_suspends_for_missing_functions(self):
        """Gate suspends when not all functions are active."""
        container = TranscendentalContainerBuilder.build()
        container.active_functions.discard(ContainerFunction.TESTABILITY)
        result = LanguageGate.evaluate(container)
        assert result.verdict is GateVerdict.SUSPEND
        assert "ناقصة" in result.reason

    def test_gate_suspends_for_no_testability(self):
        """Gate suspends when no testability result is positive."""
        container = TranscendentalContainerBuilder.build()
        container.testability_results = [TestabilityResult()]
        result = LanguageGate.evaluate(container)
        assert result.verdict is GateVerdict.SUSPEND
        assert "اختبار" in result.reason

    def test_gate_suspends_for_no_feedback(self):
        """Gate suspends when feedback is not applied."""
        container = TranscendentalContainerBuilder.build()
        container.feedback = None
        result = LanguageGate.evaluate(container)
        assert result.verdict is GateVerdict.SUSPEND
        assert "ارتجاع" in result.reason

    def test_closure_sets_closed(self):
        """Closure engine sets CLOSED on a valid container."""
        container = TranscendentalContainerBuilder.build()
        results = LanguageClosureEngine.close(container)
        assert container.closure is ClosureStatus.CLOSED
        assert results[0].verdict is GateVerdict.PASS

    def test_closure_sets_suspended(self):
        """Closure engine sets SUSPENDED on an incomplete container."""
        container = TranscendentalContainer()
        results = LanguageClosureEngine.close(container)
        assert container.closure is ClosureStatus.SUSPENDED

    def test_closure_sets_blocked(self):
        """Closure engine sets BLOCKED on a violated container."""
        container = TranscendentalContainerBuilder.build()
        from arabic_engine.core.types_language import ConstraintRecord
        container.constraint_records.append(ConstraintRecord(
            category=CognitiveCategory.ENTITY,
            confusion_kind=RankConfusionKind.ENTITY_AS_QUALITY,
            is_violated=True,
        ))
        results = LanguageClosureEngine.close(container)
        assert container.closure is ClosureStatus.BLOCKED


# ===================================================================
# 9. Enum Integrity Tests
# ===================================================================


class TestEnumIntegrity:
    """Tests that enum values are consistent and complete."""

    def test_12_cognitive_categories(self):
        """There must be exactly 12 cognitive categories."""
        assert len(CognitiveCategory) == 12

    def test_5_container_functions(self):
        """There must be exactly 5 container functions."""
        assert len(ContainerFunction) == 5

    def test_12_linguistic_positions(self):
        """There must be exactly 12 linguistic positions."""
        assert len(LinguisticPosition) == 12

    def test_8_rank_confusion_kinds(self):
        """There must be at least 8 rank confusion kinds."""
        assert len(RankConfusionKind) >= 8

    def test_layer_language_exists(self):
        """Layer.LANGUAGE must exist with value 9."""
        assert Layer.LANGUAGE.value == 9


# ===================================================================
# 10. Container Properties Tests
# ===================================================================


class TestContainerProperties:
    """Tests for TranscendentalContainer computed properties."""

    def test_empty_container_not_comprehensive(self):
        container = TranscendentalContainer()
        assert not container.is_comprehensive

    def test_empty_container_is_preventive(self):
        """Empty constraint list means no violations — trivially preventive."""
        container = TranscendentalContainer()
        assert container.is_preventive

    def test_collection_score_empty(self):
        container = TranscendentalContainer()
        assert container.collection_score == 0.0

    def test_collection_score_partial(self):
        slots = CategoryRegistry.build_all_slots()[:6]
        container = TranscendentalContainer(category_slots=slots)
        assert container.collection_score == pytest.approx(0.5)


# ===================================================================
# 11. Central Equation Integration Tests
# ===================================================================


class TestCentralEquation:
    """Tests that Lang_tr = Proj(Con(Ord(Rel(𝒦)))) holds."""

    def test_rel_step(self):
        """Rel(𝒦): categories are related to their positions."""
        slots = CategoryRegistry.build_all_slots()
        # Every slot has a category and position — they are related
        for slot in slots:
            assert slot.category is not None
            assert slot.position is not None

    def test_ord_step(self):
        """Ord: predication rules establish ordering."""
        rules = PredicationEngine.build_all_rules()
        # Rules exist — ordering is established
        assert len(rules) > 0

    def test_con_step(self):
        """Con: constraints prevent confusion."""
        slots = CategoryRegistry.build_all_slots()
        records = ConstraintSystem.validate_all_slots(slots)
        # No violations — constraints are satisfied
        assert not ConstraintSystem.has_violations(records)

    def test_proj_step(self):
        """Proj: the container projects categories into linguistic form."""
        container = TranscendentalContainerBuilder.build()
        # The container exists, is complete, and is closed-able
        results = LanguageClosureEngine.close(container)
        assert container.closure is ClosureStatus.CLOSED

    def test_full_equation(self):
        """The full equation: Lang_tr = Proj(Con(Ord(Rel(𝒦))))."""
        # Build from scratch
        container = TranscendentalContainerBuilder.build()
        # Verify all steps
        assert container.is_comprehensive      # Rel + collection
        assert container.is_preventive         # Con
        assert len(container.predication_rules) > 0  # Ord
        assert container.is_complete           # Proj
        # Close
        LanguageClosureEngine.close(container)
        assert container.closure is ClosureStatus.CLOSED


# ===================================================================
# 12. Reverse Flow Tests
# ===================================================================


class TestReverseFlow:
    """Tests for: Lang_tr → Clarification(C_2) → Stabilization(J_p) → SharedRationality."""

    def test_full_reverse_flow(self):
        """Complete container enables the full reverse flow."""
        container = TranscendentalContainerBuilder.build()
        assert container.feedback is not None
        assert container.feedback.clarification_applied
        assert container.feedback.stabilization_applied
        assert container.feedback.shared_rationality_enabled

    def test_partial_reverse_flow(self):
        """Incomplete container enables only partial feedback."""
        container = TranscendentalContainer(
            category_slots=CategoryRegistry.build_all_slots(),
        )
        record = FeedbackLoop.apply(container)
        assert record.clarification_applied
        assert not record.stabilization_applied  # no constraints
        assert not record.shared_rationality_enabled  # no functions
