"""
Judgement enumerations for the Arabic Cognitive Fractal Engine.

Defines categorical distinctions for the judgement and qiyas layers.
"""

from enum import Enum, auto


class JudgementDirection(Enum):
    """Direction of a judgement — whether it affirms or negates."""

    AFFIRMATION = auto()  # إثبات
    NEGATION = auto()     # نفي


class JudgementRank(Enum):
    """Rank of a judgement in the hierarchy of certainty."""

    CERTAIN = auto()      # يقيني
    PREDOMINANT = auto()  # ظني غالب
    PROBABLE = auto()     # ظني مرجوح
    DOUBTFUL = auto()     # شكي


class QiyasKind(Enum):
    """Kind of qiyas (analogical reasoning).

    القياس هو إلحاق فرع بأصل في حكم لعلّة جامعة بينهما.
    """

    QIYAS_ILLA = auto()      # قياس العلة — analogy by effective cause
    QIYAS_DALALA = auto()    # قياس الدلالة — analogy by indication
    QIYAS_SHABAH = auto()    # قياس الشبه — analogy by resemblance


class QiyasValidity(Enum):
    """Validity of a qiyas outcome."""

    VALID = auto()     # صحيح — all pillars present and consistent
    INVALID = auto()   # فاسد — missing or contradictory pillar
    PARTIAL = auto()   # ناقص — some pillars present, needs completion
