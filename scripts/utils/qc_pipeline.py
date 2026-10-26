"""
Quality Control Pipeline Utilities
Standard 3-Tier Screening Protocol for CAAQMS Observational Telemetry:
  Tier 1: Physical Plausibility Screening
  Tier 2: Rate-of-Change and Sensor Freezing Screening
  Tier 3: Short-Gap Repair & Completeness Auditing
"""
import numpy as np
import pandas as pd

DEFAULT_PHYSICAL_LIMITS = {
    "PM2.5": (0.0, 1000.0),
    "PM10": (0.0, 1500.0),
    "NO2": (0.0, 500.0),
    "SO2": (0.0, 500.0),
    "CO": (0.0, 50.0),
    "Ozone": (0.0, 500.0),
    "AT": (-5.0, 55.0),
    "RH": (0.0, 100.0),
    "WS": (0.0, 35.0),
    "WD": (0.0, 360.0),
    "BP": (900.0, 1100.0)
}

def apply_physical_limits(df: pd.DataFrame, limits=None) -> pd.DataFrame:
    """Flag and replace out-of-physical-range observations with NaN."""
    df_clean = df.copy()
    if limits is None:
        limits = DEFAULT_PHYSICAL_LIMITS
    for col, (vmin, vmax) in limits.items():
        if col in df_clean.columns:
            # Baseline zero drift tolerance down to -2.0 ug/m3
            mask_low = df_clean[col] < (vmin - 2.0 if vmin == 0 else vmin)
            mask_high = df_clean[col] > vmax
            df_clean.loc[mask_low | mask_high, col] = np.nan
    return df_clean

def screen_sensor_freezing(series: pd.Series, max_consecutive_hours: int = 6) -> pd.Series:
    """Flag repeated identical readings persisting longer than max_consecutive_hours."""
    s = series.copy()
    diff = s.diff().ne(0)
    groups = diff.cumsum()
    counts = s.groupby(groups).transform("count")
    s[counts >= max_consecutive_hours] = np.nan
    return s

def screen_rate_of_change(series: pd.Series, max_step: float = 150.0) -> pd.Series:
    """Flag sudden non-physical jumps exceeding max_step per observation step."""
    s = series.copy()
    step_diff = s.diff().abs()
    s[step_diff > max_step] = np.nan
    return s

def repair_short_gaps(series: pd.Series, max_gap_hours: int = 3) -> pd.Series:
    """Linearly interpolate isolated short data gaps up to max_gap_hours."""
    return series.interpolate(method="time", limit=max_gap_hours)

def audit_annual_completeness(df: pd.DataFrame, col: str = "PM2.5", target_year: int = 2024, expected_records: int = 35040) -> dict:
    """
    Audit CPCB statutory data completeness (mandates >= 75% valid capture).
    expected_records = 35,040 for 15-minute telemetry in a leap year (e.g. 2024).
    """
    sub = df[df.index.year == target_year]
    valid_count = sub[col].dropna().count()
    completeness_pct = (valid_count / expected_records) * 100.0
    is_compliant = completeness_pct >= 75.0
    return {
        "Year": target_year,
        "Column": col,
        "Valid_Records": int(valid_count),
        "Expected_Records": expected_records,
        "Completeness_Pct": round(completeness_pct, 2),
        "CPCB_Compliant": is_compliant
    }
