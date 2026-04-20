"""
Domain enumerations for the Arabic Cognitive Fractal Engine.

Defines the canonical layer ordering and compositional relation types.
"""

from enum import Enum, auto


class Layer(Enum):
    """The ten mandatory layers in strict ascending order."""

    PRE_U0_ADMISSIBILITY = 0
    SINGULAR_PERCEPTUAL = 1
    SINGULAR_INFORMATIONAL = 2
    SINGULAR_CONCEPTUAL = 3
    WEIGHT_MIZAN = 4
    COMPOSITIONAL_ROLES = 5
    PROPOSITION = 6
    JUDGEMENT = 7
    QIYAS = 8
    LANGUAGE = 9  # الوعاء الترنسندنتالي للغة — transcendental language container


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


class CommunicativeMode(Enum):
    """Communicative mode — خبر or إنشاء."""

    KHABAR = auto()    # خبر — informative
    INSHA = auto()     # إنشاء — performative
