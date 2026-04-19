"""
Form profile builder — constructs the semantic profile of a grammatical form.

The form profile encodes 9 dimensions: category, tense, aspect, voice,
number, gender, definiteness, syntactic load, and referentiality.
"""

from __future__ import annotations

import uuid

from arabic_engine.core.enums_semantic import FormSemanticDimension
from arabic_engine.core.types_semantic import FormSemanticProfile, SemanticVector

# Number of dimensions in a form semantic vector
FORM_SEMANTIC_DIM = len(FormSemanticDimension)

# Canonical dimension names (ordered by enum value)
FORM_DIMENSION_NAMES = tuple(d.name for d in FormSemanticDimension)


class FormProfileBuilder:
    """Builds a FormSemanticProfile from raw form data."""

    @staticmethod
    def build(
        pattern_id: str,
        form_values: tuple[float, ...] = (),
        form_id: str = "",
    ) -> FormSemanticProfile:
        """Build a form semantic profile.

        Args:
            pattern_id: The pattern this form belongs to.
            form_values: 9-element tuple of float values,
                one per FormSemanticDimension.
            form_id: Optional unique ID; auto-generated if empty.

        Returns:
            A fully populated FormSemanticProfile.

        Raises:
            ValueError: If form_values does not have exactly 9 elements.
        """
        if len(form_values) != FORM_SEMANTIC_DIM:
            raise ValueError(
                f"form_values must have exactly {FORM_SEMANTIC_DIM} elements, "
                f"got {len(form_values)}"
            )

        vec = SemanticVector(
            values=form_values,
            dimension_names=FORM_DIMENSION_NAMES,
        )

        return FormSemanticProfile(
            form_id=form_id or f"form-{uuid.uuid4().hex[:8]}",
            pattern_id=pattern_id,
            form_semantic_vector=vec,
        )
