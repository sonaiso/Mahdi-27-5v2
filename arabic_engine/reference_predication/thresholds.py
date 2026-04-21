"""Locked threshold bundle for the current execution cycle."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferencePredicationThresholdBundle:
    """Numeric acceptance bundle locked for this cycle (v1)."""

    theta_sigma1: float = 0.70
    theta_p: float = 0.70
    theta_m: float = 0.70
    theta_t: float = 0.55
    theta_l: float = 0.55
    theta_purity: float = 0.70
    theta_nu: float = 0.65
    epsilon_rho: float = 0.20
    theta_gi: float = 0.60
    # Minimum causal consistency accepted for I^(2) projection.
    theta_i2_causal_alignment: float = 0.50
    # Minimum referential consistency accepted for I^(2) projection.
    theta_i2_referential_alignment: float = 0.50


THRESHOLD_BUNDLE_V1 = ReferencePredicationThresholdBundle()
