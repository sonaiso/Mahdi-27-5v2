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
