"""
Enumerations for the Arabic Cognitive Fractal Engine.

Defines the canonical layer ordering and all categorical distinctions
used across the singular, weight, and compositional layers.
"""

from enum import Enum, auto


# ---------------------------------------------------------------------------
# Layer ordering (the nine mandatory ranks)
# ---------------------------------------------------------------------------

class Layer(Enum):
    """The nine mandatory layers in strict ascending order."""

    PRE_U0_ADMISSIBILITY = 0
    SINGULAR_PERCEPTUAL = 1
    SINGULAR_INFORMATIONAL = 2
    SINGULAR_CONCEPTUAL = 3
    WEIGHT_MIZAN = 4
    COMPOSITIONAL_ROLES = 5
    PROPOSITION = 6
    JUDGEMENT = 7
    QIYAS = 8


# ---------------------------------------------------------------------------
# Gate / closure status
# ---------------------------------------------------------------------------

class ClosureStatus(Enum):
    """Status of a closure gate at any layer."""

    OPEN = auto()        # Not yet evaluated
    CLOSED = auto()      # Successfully closed — all conditions met
    BLOCKED = auto()     # A blocker prevents closure
    SUSPENDED = auto()   # Temporarily suspended pending further information


class GateVerdict(Enum):
    """Verdict returned by a gate check."""

    PASS = auto()
    REJECT = auto()
    SUSPEND = auto()


# ---------------------------------------------------------------------------
# Singular-layer categories
# ---------------------------------------------------------------------------

class StabilityKind(Enum):
    """First-order stability / transformability distinction."""

    STABLE = auto()      # ثبات — denotes a stable entity
    TRANSFORMING = auto()  # تحول — denotes a dynamic event/process


class WordCategory(Enum):
    """Fundamental tripartite word classification (اسم / فعل / حرف)."""

    ISM = auto()     # اسم — noun
    FI3L = auto()    # فعل — verb
    HARF = auto()    # حرف — particle


class DerivationKind(Enum):
    """Whether the unit is derived or non-derived (مشتق / جامد)."""

    JAMID = auto()     # جامد — non-derived / frozen
    MUSHTAQ = auto()   # مشتق — derived


class Definiteness(Enum):
    """Definiteness distinction (تعريف / تنكير)."""

    DEFINITE = auto()    # معرفة
    INDEFINITE = auto()  # نكرة


class Gender(Enum):
    """Gender distinction (تذكير / تأنيث)."""

    MASCULINE = auto()  # مذكر
    FEMININE = auto()   # مؤنث


# ---------------------------------------------------------------------------
# Weight / Mizan categories
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Compositional-layer categories
# ---------------------------------------------------------------------------

class RelationKind(Enum):
    """The three canonical compositional relation types."""

    ASNADI = auto()    # إسنادية — predicative
    TADMINI = auto()   # تضمينية — embedding / containment
    TAQYIDI = auto()   # تقييدية — restrictive / qualifying


class RoleTag(Enum):
    """Grammatical roles within a compositional structure."""

    MUSNAD = auto()        # مسند — predicate
    MUSNAD_ILAYH = auto()  # مسند إليه — subject
    FA3IL = auto()         # فاعل — agent
    MAF3UL = auto()        # مفعول — patient
    HAL = auto()           # حال — circumstantial
    TAMYIZ = auto()        # تمييز — specification
    MUDAF = auto()         # مضاف — possessor (construct state head)
    MUDAF_ILAYH = auto()   # مضاف إليه — possessed
    SIFA = auto()          # صفة — adjective / qualifier
    MAWSUF = auto()        # موصوف — qualified noun
