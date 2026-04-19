"""
Weight / Mizan enumerations for the Arabic Cognitive Fractal Engine.

Defines categorical distinctions used in the weight/mizan fractal layer.
"""

from enum import Enum, auto


class InflectionKind(Enum):
    """Built vs. inflected distinction (مبني / معرب)."""

    MABNI = auto()    # مبني — built (fixed ending)
    MU3RAB = auto()   # معرب — inflected (ending changes by position)


class WeightEligibility(Enum):
    """Whether the unit is eligible to carry a morphological weight."""

    ELIGIBLE = auto()
    NOT_ELIGIBLE = auto()


class TemporalPotential(Enum):
    """Temporal potential of a verbal weight."""

    MADI = auto()       # ماضٍ — past
    MUDARI3 = auto()    # مضارع — present/future
    AMR = auto()        # أمر — imperative
    NONE = auto()       # Not applicable (nouns, particles)


class SpatialPotential(Enum):
    """Spatial potential — whether the weight can yield a place-noun."""

    HAS_SPATIAL = auto()
    NO_SPATIAL = auto()


class DescriptivePotential(Enum):
    """Descriptive potential of the weight."""

    SIFA_MUSHABBAHA = auto()   # صفة مشبهة
    ISM_FA3IL = auto()         # اسم فاعل
    ISM_MAF3UL = auto()        # اسم مفعول
    NONE = auto()
