"""
Singular-layer enumerations for the Arabic Cognitive Fractal Engine.

Defines categorical distinctions used in the singular layers
(perceptual, informational, conceptual).
"""

from enum import Enum, auto


class StabilityKind(Enum):
    """First-order stability / transformability distinction."""

    STABLE = auto()        # ثبات — denotes a stable entity
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
