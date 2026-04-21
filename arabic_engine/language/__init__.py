"""
Language — the transcendental container (الوعاء الترنسندنتالي).

This package implements the Language layer of the Arabic Cognitive Fractal
Engine.  Language is not the origin of reason but the transcendental
container that collects cognitive categories after they form in the mind,
prevents their confusion, and renders them expressible, predicable,
referable, and testable.

Intellectual foundation:
  - al-Nabhani: reason originates from Reality + Sensation + PriorInfo + Linking
  - Kant: all of the above requires prior conditions of possibility
  - This project: language is the container that gathers these conditions
    once they become categories, and gives them an expressive form that is
    both comprehensive (جامع) and exclusive (مانع).

Subsystems:
  - categories:   CategoryRegistry — maps 𝒦 to linguistic positions
  - container:    TranscendentalContainerBuilder — constructs Lang_tr
  - constraints:  ConstraintSystem — prevents rank confusion
  - predication:  PredicationEngine — enables judgement from categories
  - reference:    ReferenceSystem — binds discourse to referents
  - testability:  TestabilityInterface — makes judgements truth-evaluable
  - feedback:     FeedbackLoop — Lang_tr → Clarification → Stabilization
  - closure:      LanguageClosureEngine — gate/closure for the language layer
"""

from .foundational_hook import LanguageFoundationalAdapter  # noqa: F401
