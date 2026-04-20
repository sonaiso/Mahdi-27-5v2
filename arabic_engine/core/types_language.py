"""
Language-layer data types for the Arabic Cognitive Fractal Engine.

Defines the data structures for the transcendental container (Lang_tr):

    Lang_tr = ⟨Lexicon, CategorySystem, PredicationRules,
              ConstraintSystem, ReferenceSystem, TestabilityInterface⟩

And the central equation:

    Lang_tr = Proj(Con(Ord(Rel(𝒦))))

i.e. language is the projection of categories that are:
  - related (Rel) — connected to their relations
  - ordered (Ord) — organized by rank
  - constrained (Con) — guarded against confusion
  - projected (Proj) — expressed in linguistic form
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .enums_gate import ClosureStatus
from .enums_language import (
    CognitiveCategory,
    ContainerFunction,
    ContainerValidityStatus,
    LinguisticPosition,
    RankConfusionKind,
)


# ---------------------------------------------------------------------------
# Category Slot — where a category is housed in the container
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CategorySlot:
    """A slot in the transcendental container that holds one cognitive category.

    Each slot maps a cognitive category to its linguistic position and tracks
    whether the assignment is valid.
    """

    category: CognitiveCategory
    position: LinguisticPosition
    validity: ContainerValidityStatus = ContainerValidityStatus.VALID
    label_ar: str = ""   # Arabic label for this category
    label_en: str = ""   # English label for this category


# ---------------------------------------------------------------------------
# Constraint Record — a single constraint preventing rank confusion
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ConstraintRecord:
    """A single constraint enforced by the container's prevention function.

    Represents: Con_lang(x) where Valid(x) ⟺ Category(x) ∧ ProperRole(x)
                                              ∧ NoRankConfusion(x)
    """

    category: CognitiveCategory
    confusion_kind: Optional[RankConfusionKind] = None
    is_violated: bool = False
    violation_reason: str = ""


# ---------------------------------------------------------------------------
# Predication Rule — how categories combine into judgements
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PredicationRule:
    """A rule governing how categories may combine in predication (الإسناد).

    Predication requires a subject (مسند إليه) and a predicate (مسند),
    each drawn from specific categories.
    """

    subject_category: CognitiveCategory
    predicate_category: CognitiveCategory
    is_permitted: bool = True
    rule_description: str = ""


# ---------------------------------------------------------------------------
# Reference Binding — connects discourse to its referents
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ReferenceBinding:
    """A binding in the reference system (نظام الإحالة).

    Connects a referring expression (pronoun, demonstrative, relative) to
    its referent category.
    """

    referent_category: CognitiveCategory
    reference_type: str = ""       # e.g. "ضمير", "إشارة", "موصول"
    is_resolved: bool = False
    referent_label: str = ""


# ---------------------------------------------------------------------------
# Testability Result — whether a judgement is testable
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TestabilityResult:
    """Result of the testability interface (واجهة الاختبار).

    Determines whether a judgement formed from categories can be tested
    for truth or falsity.
    """

    __test__ = False  # prevent pytest collection

    is_testable: bool = False
    testability_reason: str = ""
    truth_evaluable: bool = False    # can be evaluated as true/false (خبر)
    performative_only: bool = False  # performative, not truth-evaluable (إنشاء)


# ---------------------------------------------------------------------------
# Feedback Record — the reverse flow from language back to concepts
# ---------------------------------------------------------------------------

@dataclass
class FeedbackRecord:
    """Record of the feedback loop from language back to cognition.

    Lang_tr → Clarification(C_2) → Stabilization(J_p) → SharedRationality

    Language doesn't just project forward; it feeds back to:
    - Clarify composite concepts (C_2)
    - Stabilize judgements (J_p)
    - Enable shared rationality
    """

    clarification_applied: bool = False
    stabilization_applied: bool = False
    shared_rationality_enabled: bool = False
    feedback_description: str = ""


# ---------------------------------------------------------------------------
# TranscendentalContainer — the full Lang_tr structure
# ---------------------------------------------------------------------------

@dataclass
class TranscendentalContainer:
    """The transcendental container for language (الوعاء الترنسندنتالي للغة).

    Lang_tr = ⟨Lexicon, CategorySystem, PredicationRules,
              ConstraintSystem, ReferenceSystem, TestabilityInterface⟩

    This is the top-level structure that:
    - Collects (يجمع) categories in a single system
    - Prevents (يمنع) rank confusion
    - Carries (يحمل) meaning from mind to expression
    - Designates (يعيّن) each category its position
    - Tests (يختبر) judgements for truth/falsity

    Central equation: Lang_tr = Proj(Con(Ord(Rel(𝒦))))
    """

    # Category system — the 12 slots for cognitive categories
    category_slots: list[CategorySlot] = field(default_factory=list)

    # Predication rules — how categories combine
    predication_rules: list[PredicationRule] = field(default_factory=list)

    # Constraint records — active constraints preventing confusion
    constraint_records: list[ConstraintRecord] = field(default_factory=list)

    # Reference bindings — connecting discourse to referents
    reference_bindings: list[ReferenceBinding] = field(default_factory=list)

    # Testability results — judgement testability assessments
    testability_results: list[TestabilityResult] = field(default_factory=list)

    # Feedback — reverse flow from language to cognition
    feedback: Optional[FeedbackRecord] = None

    # Container-level functions that are active
    active_functions: set[ContainerFunction] = field(default_factory=set)

    # Closure status
    closure: ClosureStatus = ClosureStatus.OPEN

    @property
    def is_comprehensive(self) -> bool:
        """Whether the container is comprehensive (جامع) — all 12 categories present."""
        present = {slot.category for slot in self.category_slots}
        return len(present) == len(CognitiveCategory)

    @property
    def is_preventive(self) -> bool:
        """Whether the container is preventive (مانع) — no rank confusion."""
        return all(not c.is_violated for c in self.constraint_records)

    @property
    def is_complete(self) -> bool:
        """Whether the container is complete — comprehensive and preventive."""
        return self.is_comprehensive and self.is_preventive

    @property
    def collection_score(self) -> float:
        """Fraction of the 12 categories that are present in slots."""
        if not self.category_slots:
            return 0.0
        present = {slot.category for slot in self.category_slots}
        return len(present) / len(CognitiveCategory)

    @property
    def constraint_violation_count(self) -> int:
        """Number of constraint violations."""
        return sum(1 for c in self.constraint_records if c.is_violated)
