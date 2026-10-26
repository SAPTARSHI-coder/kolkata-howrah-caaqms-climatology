"""
Statistical and Autocorrelation Analysis Utilities
Calculates autocorrelation-adjusted effective sample size (N_eff) using Bartlett's formula:
  N_eff = N * (1 - r1) / (1 + r1)
and derives Fisher z-transformed 95% confidence intervals for Spearman and Pearson correlations.
"""
import numpy as np
from scipy import stats

def compute_lag1_autocorrelation(series):
    """Computes lag-1 autocorrelation coefficient (r1) of a pandas Series."""
    s = series.dropna()
    if len(s) < 10:
        return 0.0
    return float(s.autocorr(lag=1))

def compute_effective_sample_size(series, r1=None):
    """
    Computes effective degrees of freedom / sample size adjusted for serial autocorrelation.
    """
    s = series.dropna()
    N = len(s)
    if N < 10:
        return N
    if r1 is None:
        r1 = compute_lag1_autocorrelation(s)
    r1 = np.clip(r1, -0.99, 0.99)
    # Bartlett / Quenouille formula
    n_eff = N * (1.0 - r1) / (1.0 + r1)
    return max(int(np.round(n_eff)), 10)

def compute_adjusted_confidence_interval(r, n_eff, alpha=0.05):
    """
    Computes two-sided confidence interval for correlation r under effective sample size n_eff.
    Uses Fisher z-transformation: z = 0.5 * ln((1 + r) / (1 - r)).
    """
    r = np.clip(r, -0.9999, 0.9999)
    z = np.arctanh(r)
    se = 1.0 / np.sqrt(max(n_eff - 3, 1))
    z_crit = stats.norm.ppf(1.0 - alpha / 2.0)
    z_low = z - z_crit * se
    z_high = z + z_crit * se
    r_low = np.tanh(z_low)
    r_high = np.tanh(z_high)
    return round(float(r_low), 2), round(float(r_high), 2)
