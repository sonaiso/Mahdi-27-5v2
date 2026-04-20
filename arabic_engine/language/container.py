"""
Transcendental container builder — constructs Lang_tr.

Implements the central equation:

    Lang_tr = Proj(Con(Ord(Rel(𝒦))))

That is, the transcendental language container is the **projection**
of cognitive categories that are **related**, **ordered**, **constrained**,
and **projected** into linguistic form.

The builder orchestrates:
    1. CategoryRegistry → builds all 12 category slots (Rel(𝒦))
    2. ConstraintSystem → validates all slots (Con)
    3. PredicationEngine → builds predication rules (Ord)
    4. ReferenceSystem → builds reference bindings
    5. TestabilityInterface → evaluates testability
    6. FeedbackLoop → applies reverse flow
"""

from __future__ import annotations

from arabic_engine.core.enums_language import ContainerFunction
from arabic_engine.core.types_language import (
    ReferenceBinding,
    TranscendentalContainer,
)

from .categories import CategoryRegistry
from .constraints import ConstraintSystem
from .feedback import FeedbackLoop
from .predication import PredicationEngine
from .reference import ReferenceSystem
from .testability import TestabilityInterface


class TranscendentalContainerBuilder:
    """Builds the complete transcendental container (Lang_tr).

    The builder follows the equation:
        Lang_tr = Proj(Con(Ord(Rel(𝒦))))

    Steps:
    1. Relate (Rel): Build category slots with their positions
    2. Order (Ord): Build predication rules from categories
    3. Constrain (Con): Validate constraints on all slots
    4. Project (Proj): Assemble into the final container

    Additional subsystems (Reference, Testability, Feedback) are
    built as part of the projection step.
    """

    @staticmethod
    def build(
        reference_bindings: list[ReferenceBinding] | None = None,
    ) -> TranscendentalContainer:
        """Build a complete transcendental container.

        Parameters
        ----------
        reference_bindings : list[ReferenceBinding] | None
            Optional reference bindings. If not provided, an empty list is used.

        Returns
        -------
        TranscendentalContainer
            The fully built container with all subsystems populated.
        """
        # Step 1: Rel(𝒦) — relate categories to positions
        slots = CategoryRegistry.build_all_slots()

        # Step 2: Con — constrain, validate against rank confusion
        constraint_records = ConstraintSystem.validate_all_slots(slots)

        # Step 3: Ord — order via predication rules
        predication_rules = PredicationEngine.build_all_rules()

        # Step 4: Reference system
        refs = reference_bindings if reference_bindings is not None else []

        # Step 5: Testability
        testability_results = [TestabilityInterface.evaluate_slots(slots)]

        # Step 6: Assemble active functions
        active_functions: set[ContainerFunction] = set()

        # Collection — if all 12 slots are present
        if CategoryRegistry.is_comprehensive(slots):
            active_functions.add(ContainerFunction.COLLECTION)

        # Prevention — if no constraint violations
        if not ConstraintSystem.has_violations(constraint_records):
            active_functions.add(ContainerFunction.PREVENTION)

        # Carrying — always active once categories exist
        if slots:
            active_functions.add(ContainerFunction.CARRYING)

        # Designation — if every slot has a proper position
        if all(s.position is not None for s in slots):
            active_functions.add(ContainerFunction.DESIGNATION)

        # Testability — if at least one testable result
        if any(t.is_testable for t in testability_results):
            active_functions.add(ContainerFunction.TESTABILITY)

        # Build container
        container = TranscendentalContainer(
            category_slots=slots,
            predication_rules=predication_rules,
            constraint_records=constraint_records,
            reference_bindings=refs,
            testability_results=testability_results,
            active_functions=active_functions,
        )

        # Step 7: Feedback loop
        container.feedback = FeedbackLoop.apply(container)

        return container
