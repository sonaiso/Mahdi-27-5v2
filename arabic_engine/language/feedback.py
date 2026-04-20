"""
Feedback loop — the reverse flow from language back to cognition.

Implements:
    Lang_tr → Clarification(C_2) → Stabilization(J_p) → SharedRationality

Language is not just a forward projection — it feeds back to:
  - Clarify composite concepts (C_2) by giving them linguistic form
  - Stabilize judgements (J_p) by binding them to expressible structure
  - Enable shared rationality by making categories communicable
"""

from __future__ import annotations

from arabic_engine.core.types_language import (
    FeedbackRecord,
    TranscendentalContainer,
)


class FeedbackLoop:
    """Implements the reverse flow from language to cognition.

    Once the transcendental container is built, it can feed back
    into the cognitive pipeline:

    1. Clarification — the container's category system clarifies
       composite concepts (C_2) by giving each part a name and role.

    2. Stabilization — the container's constraint system stabilizes
       judgements (J_p) by preventing confusion and fixing boundaries.

    3. Shared Rationality — the container's predication and reference
       systems enable judgements to be communicated and tested by others.
    """

    @staticmethod
    def apply(container: TranscendentalContainer) -> FeedbackRecord:
        """Apply the feedback loop to a completed transcendental container.

        The container must be at least partially built (some slots present).
        Each feedback step depends on the container's state.
        """
        clarification = False
        stabilization = False
        shared = False
        parts: list[str] = []

        # Step 1: Clarification — requires category slots to be present
        if container.category_slots:
            clarification = True
            parts.append(
                "توضيح المفهوم التركيبي (C_2) عبر تصنيف المقولات"
            )

        # Step 2: Stabilization — requires constraint system to be active
        if container.constraint_records and container.is_preventive:
            stabilization = True
            parts.append(
                "تثبيت الحكم (J_p) عبر نظام منع خلط الرتب"
            )

        # Step 3: Shared Rationality — requires all five container functions
        if len(container.active_functions) >= 5:
            shared = True
            parts.append(
                "تمكين العقلانية المشتركة عبر اكتمال وظائف الوعاء"
            )

        return FeedbackRecord(
            clarification_applied=clarification,
            stabilization_applied=stabilization,
            shared_rationality_enabled=shared,
            feedback_description=" ← ".join(parts) if parts else "لم يُطبَّق أي ارتجاع",
        )
