"""
Semantic dimension alignment — maps between root, pattern, and form spaces.

Root vectors (13-dim), pattern vectors (12-dim), and form vectors (9-dim) live
in semantically different spaces.  This module defines explicit alignment
mappings that preserve dimensional semantics when projecting between spaces,
replacing naive zero-padding/truncation.

Alignment mappings:
    ROOT_TO_PATTERN_MAP — maps each PatternSemanticDimension index to a
        SemanticDimension index (or -1 if no direct mapping exists).
    ROOT_TO_FORM_MAP — maps each FormSemanticDimension index to a
        SemanticDimension index (or -1 if no mapping exists).
    PATTERN_TO_FORM_MAP — maps each FormSemanticDimension index to a
        PatternSemanticDimension index (or -1 if no mapping exists).
"""

from __future__ import annotations

import math

from arabic_engine.core.types_semantic import SemanticVector

# ---------------------------------------------------------------------------
# Alignment maps
# ---------------------------------------------------------------------------

# Root (13-dim) → Pattern (12-dim) mapping:
# Each entry is (pattern_dim_index, root_dim_index).
# SemanticDimension order:
#   0=ENTITY, 1=EVENT, 2=QUALITY, 3=RELATION, 4=AGENCY, 5=PATIENTHOOD,
#   6=CAUSALITY, 7=RESULTATIVITY, 8=TEMPORALITY, 9=SPATIALITY,
#   10=EMBODIMENT, 11=ABSTRACTION, 12=TRANSFERABILITY
# PatternSemanticDimension order:
#   0=EVENT_SHIFT, 1=AGENCY_SHIFT, 2=TRANSITIVITY_SHIFT, 3=CAUSATIVE_SHIFT,
#   4=REFLEXIVE_SHIFT, 5=INTENSIFICATION, 6=ITERATIVITY, 7=STATIVE_SHIFT,
#   8=NOMINALIZATION, 9=INSTRUMENTALITY, 10=LOCATIVITY, 11=TEMPORALITY_SHIFT
ROOT_TO_PATTERN_MAP: tuple[int, ...] = (
    1,    # EVENT_SHIFT ← EVENT
    4,    # AGENCY_SHIFT ← AGENCY
    3,    # TRANSITIVITY_SHIFT ← RELATION
    6,    # CAUSATIVE_SHIFT ← CAUSALITY
    5,    # REFLEXIVE_SHIFT ← PATIENTHOOD
    1,    # INTENSIFICATION ← EVENT (intensifies the event)
    8,    # ITERATIVITY ← TEMPORALITY (temporal repetition)
    2,    # STATIVE_SHIFT ← QUALITY (state-like)
    0,    # NOMINALIZATION ← ENTITY (becoming a noun/entity)
    10,   # INSTRUMENTALITY ← EMBODIMENT (concrete tool)
    9,    # LOCATIVITY ← SPATIALITY
    8,    # TEMPORALITY_SHIFT ← TEMPORALITY
)

# Root (13-dim) → Form (9-dim) mapping:
# FormSemanticDimension order:
#   0=CATEGORY, 1=TENSE, 2=ASPECT, 3=VOICE, 4=NUMBER,
#   5=GENDER, 6=DEFINITENESS, 7=SYNTACTIC_LOAD, 8=REFERENTIALITY
ROOT_TO_FORM_MAP: tuple[int, ...] = (
    0,    # CATEGORY ← ENTITY
    8,    # TENSE ← TEMPORALITY
    1,    # ASPECT ← EVENT (aspect relates to event structure)
    4,    # VOICE ← AGENCY (active/passive relates to agency)
    -1,   # NUMBER — no direct root mapping
    -1,   # GENDER — no direct root mapping
    -1,   # DEFINITENESS — no direct root mapping
    3,    # SYNTACTIC_LOAD ← RELATION
    12,   # REFERENTIALITY ← TRANSFERABILITY
)

# Pattern (12-dim) → Form (9-dim) mapping:
PATTERN_TO_FORM_MAP: tuple[int, ...] = (
    8,    # CATEGORY ← NOMINALIZATION
    11,   # TENSE ← TEMPORALITY_SHIFT
    0,    # ASPECT ← EVENT_SHIFT
    1,    # VOICE ← AGENCY_SHIFT
    -1,   # NUMBER — no direct pattern mapping
    -1,   # GENDER — no direct pattern mapping
    -1,   # DEFINITENESS — no direct pattern mapping
    2,    # SYNTACTIC_LOAD ← TRANSITIVITY_SHIFT
    -1,   # REFERENTIALITY — no direct pattern mapping
)


def _project_via_map(
    source: SemanticVector,
    target_dim: int,
    alignment_map: tuple[int, ...],
) -> SemanticVector:
    """Project a source vector into a target space using an alignment map.

    For each target dimension ``i``, if ``alignment_map[i]`` is a valid
    source index (≥ 0), the source value is copied; otherwise 0.0 is used.
    """
    values: list[float] = []
    for i in range(target_dim):
        if i < len(alignment_map) and alignment_map[i] >= 0:
            src_idx = alignment_map[i]
            if src_idx < source.dim:
                values.append(source.values[src_idx])
            else:
                values.append(0.0)
        else:
            values.append(0.0)
    return SemanticVector(values=tuple(values))


def project_root_to_pattern_space(root_vec: SemanticVector) -> SemanticVector:
    """Project a 13-dim root vector into the 12-dim pattern space."""
    return _project_via_map(root_vec, 12, ROOT_TO_PATTERN_MAP)


def project_root_to_form_space(root_vec: SemanticVector) -> SemanticVector:
    """Project a 13-dim root vector into the 9-dim form space."""
    return _project_via_map(root_vec, 9, ROOT_TO_FORM_MAP)


def project_pattern_to_form_space(pattern_vec: SemanticVector) -> SemanticVector:
    """Project a 12-dim pattern vector into the 9-dim form space."""
    return _project_via_map(pattern_vec, 9, PATTERN_TO_FORM_MAP)


def project_to_common_space(
    root_vec: SemanticVector,
    pattern_vec: SemanticVector,
    form_vec: SemanticVector,
) -> tuple[SemanticVector, SemanticVector, SemanticVector]:
    """Project root, pattern, and form vectors into a common 13-dim space.

    The common space uses the root's 13 dimensions as the canonical basis.
    Pattern and form vectors are reverse-mapped into root space.
    """
    out_dim = 13  # Root space is the canonical common space

    # Root → already in root space, just pad/truncate to 13
    r_values = list(root_vec.values[:out_dim])
    r_values += [0.0] * (out_dim - len(r_values))

    # Pattern → root space (reverse mapping)
    p_values = [0.0] * out_dim
    for pat_idx, root_idx in enumerate(ROOT_TO_PATTERN_MAP):
        if pat_idx < pattern_vec.dim and root_idx >= 0 and root_idx < out_dim:
            p_values[root_idx] += pattern_vec.values[pat_idx]

    # Form → root space (reverse mapping)
    f_values = [0.0] * out_dim
    for form_idx, root_idx in enumerate(ROOT_TO_FORM_MAP):
        if form_idx < form_vec.dim and root_idx >= 0 and root_idx < out_dim:
            f_values[root_idx] += form_vec.values[form_idx]

    return (
        SemanticVector(values=tuple(r_values)),
        SemanticVector(values=tuple(p_values)),
        SemanticVector(values=tuple(f_values)),
    )
