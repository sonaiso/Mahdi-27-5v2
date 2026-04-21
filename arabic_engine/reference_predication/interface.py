"""Stable interface for the independent Σ1→Σ2 reference-predication baseline."""

from __future__ import annotations

import os
from dataclasses import dataclass

from arabic_engine.core.enums_domain import Layer
from arabic_engine.core.enums_gate import GateVerdict
from arabic_engine.core.types_gate import GateResult
from arabic_engine.reference_predication.models import (
    GrammaticalFactorGI,
    MentalFactor,
    PropositionConstraintVector,
    RatioVector,
    SentenceSpace,
    Sigma1ReferenceUnit,
    Sigma1Thresholds,
    Sigma2Builder,
    Sigma2Matrix,
    SigmaTransitionError,
)
from arabic_engine.trace.unified import UnifiedTracer


def _parse_feature_flag(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on", "enabled"}


@dataclass(frozen=True)
class Sigma2InterfaceResult:
    """Result envelope for the stable reference-predication interface."""

    enabled: bool
    matrix: Sigma2Matrix | None = None
    skipped: bool = False
    skip_reason: str = ""


class ReferencePredicationInterface:
    """Feature-flagged, traceable facade over ``Sigma2Builder``."""

    FEATURE_FLAG_ENV = "ARABIC_ENGINE_ENABLE_REFERENCE_PREDICATION"

    def __init__(
        self,
        *,
        enabled: bool | None = None,
        tracer: UnifiedTracer | None = None,
    ) -> None:
        self._enabled = (
            enabled
            if enabled is not None
            else _parse_feature_flag(os.getenv(self.FEATURE_FLAG_ENV))
        )
        self._tracer = tracer or UnifiedTracer()

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def tracer(self) -> UnifiedTracer:
        return self._tracer

    def build_sigma2(
        self,
        first: Sigma1ReferenceUnit,
        second: Sigma1ReferenceUnit,
        *,
        sentence_space: SentenceSpace,
        mental_factor: MentalFactor,
        grammatical_factor: str | GrammaticalFactorGI,
        ratios: RatioVector,
        proposition_constraint: PropositionConstraintVector,
        thresholds: Sigma1Thresholds | None = None,
        omega: str = "omega_d",
        gamma: str = "present",
        varsigma: float = 1.0,
        subject_mark: str = "raf",
        predicate_mark: str = "raf",
    ) -> Sigma2InterfaceResult:
        """Build Σ2 through a stable interface without coupling to ``MasterChain``."""
        if not self._enabled:
            reason = (
                "reference_predication interface skipped — feature flag disabled"
            )
            self._tracer.record_closure(layer=Layer.LANGUAGE, reason=reason)
            return Sigma2InterfaceResult(
                enabled=False,
                skipped=True,
                skip_reason=reason,
            )

        self._tracer.record_closure(
            layer=Layer.LANGUAGE,
            reason="reference_predication interface started",
        )
        try:
            matrix = Sigma2Builder.build(
                first,
                second,
                sentence_space=sentence_space,
                mental_factor=mental_factor,
                grammatical_factor=grammatical_factor,
                ratios=ratios,
                proposition_constraint=proposition_constraint,
                thresholds=thresholds,
                omega=omega,
                gamma=gamma,
                varsigma=varsigma,
                subject_mark=subject_mark,
                predicate_mark=predicate_mark,
            )
        except SigmaTransitionError as exc:
            self._tracer.record_gate(
                GateResult(
                    verdict=GateVerdict.REJECT,
                    layer=Layer.LANGUAGE,
                    reason=f"reference_predication interface failed: {exc}",
                    missing_condition="sigma2_prerequisites",
                )
            )
            raise

        self._tracer.record_closure(
            layer=Layer.LANGUAGE,
            reason="reference_predication interface succeeded",
        )
        return Sigma2InterfaceResult(enabled=True, matrix=matrix)
