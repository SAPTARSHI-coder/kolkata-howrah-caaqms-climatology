"""
Comprehensive 10-Station Chronological Forecasting Benchmark
Paper 1: Continuous Observational Climatology and Trans-Hooghly Directional Transport

Evaluates 1-hour and 24-hour PM2.5 forecasting under a strictly chronological
train (2024) -> test (2025) split across all 10 compliant CAAQMS stations in Kolkata and Howrah.
"""
import os
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import r2_score, root_mean_squared_error, mean_absolute_error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
DATA_DIR = os.path.join(BASE_DIR, "data", "Cleaned_Station_Data")
OUT_DIR = os.path.join(BASE_DIR, "data", "benchmarks")

STATIONS = {
    "BG": "Ballygunge",
    "BM": "Belur Math",
    "BN": "Bidhannagar",
    "FW": "Fort William",
    "GH": "Ghusuri",
    "JD": "Jadavpur",
    "PP": "Padmapukur",
    "RBU": "Rabindra Bharati University",
    "RS": "Rabindra Sarovar",
    "VC": "Victoria Memorial"
}

def load_station(code):
    f24 = os.path.join(DATA_DIR, f"{code}_2024_MLL.xlsx")
    f25 = os.path.join(DATA_DIR, f"{code}_2025_MLL.xlsx")
    if not (os.path.exists(f24) and os.path.exists(f25)):
        raise FileNotFoundError(f"Missing data files for station {code} in {DATA_DIR}")
    df24 = pd.read_excel(f24)
    df25 = pd.read_excel(f25)
    df24["DateTime"] = pd.to_datetime(df24["DateTime"])
    df25["DateTime"] = pd.to_datetime(df25["DateTime"])
    df = pd.concat([df24, df25]).set_index("DateTime").sort_index()
    num_cols = [c for c in ["PM2.5", "AT", "RH", "WS"] if c in df.columns]
    h = df[num_cols].resample("1h").mean().interpolate(method="time", limit=3)
    return h

def evaluate_station_horizon(h, code, name, horizon):
    df = h.sort_index().asfreq("1h").copy()
    lags = [0, 1, 2, 3, 6, 12, 24]
    for L in lags:
        df[f"pm25_lag_{L}"] = df["PM2.5"].shift(L)
    
    hour_rad = 2.0 * np.pi * df.index.hour / 24.0
    df["sin_h"] = np.sin(hour_rad)
    df["cos_h"] = np.cos(hour_rad)
    df["target"] = df["PM2.5"].shift(-horizon)
    df = df.dropna()

    train_mask = df.index.year == 2024
    test_mask = df.index.year == 2025
    train_df = df[train_mask]
    test_df = df[test_mask]

    feature_cols = [f"pm25_lag_{L}" for L in lags] + ["sin_h", "cos_h"]
    for c in ["AT", "RH", "WS"]:
        if c in df.columns:
            feature_cols.append(c)

    X_train = train_df[feature_cols].values
    y_train = train_df["target"].values
    X_test = test_df[feature_cols].values
    y_test = test_df["target"].values

    # Naive persistence baseline: PM2.5(t) predicts PM2.5(t+H)
    y_pers = test_df["PM2.5"].values
    r2_p = r2_score(y_test, y_pers)
    rmse_p = root_mean_squared_error(y_test, y_pers)
    mae_p = mean_absolute_error(y_test, y_pers)

    # Standardized Ridge Regression
    ridge = make_pipeline(StandardScaler(), Ridge(alpha=10.0))
    ridge.fit(X_train, y_train)
    y_pred_ridge = ridge.predict(X_test)
    r2_r = r2_score(y_test, y_pred_ridge)
    rmse_r = root_mean_squared_error(y_test, y_pred_ridge)
    mae_r = mean_absolute_error(y_test, y_pred_ridge)

    # Gradient Boosted Trees
    hgbt = HistGradientBoostingRegressor(max_iter=150, max_depth=6, random_state=42)
    hgbt.fit(X_train, y_train)
    y_pred_hgbt = hgbt.predict(X_test)
    r2_h = r2_score(y_test, y_pred_hgbt)
    rmse_h = root_mean_squared_error(y_test, y_pred_hgbt)
    mae_h = mean_absolute_error(y_test, y_pred_hgbt)

    return {
        "Station_Code": code,
        "Station_Name": name,
        "Horizon_h": horizon,
        "Train_N": len(train_df),
        "Test_N": len(test_df),
        "Persistence_R2": round(r2_p, 4),
        "Persistence_RMSE": round(rmse_p, 2),
        "Persistence_MAE": round(mae_p, 2),
        "Ridge_R2": round(r2_r, 4),
        "Ridge_RMSE": round(rmse_r, 2),
        "Ridge_MAE": round(mae_r, 2),
        "HGBT_R2": round(r2_h, 4),
        "HGBT_RMSE": round(rmse_h, 2),
        "HGBT_MAE": round(mae_h, 2)
    }

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("=" * 70)
    print("RUNNING 10-STATION FORECASTING BENCHMARK (2024 TRAIN -> 2025 TEST)")
    print("=" * 70)
    
    records = []
    for code, name in STATIONS.items():
        print(f"Processing station: {code} ({name})...")
        h = load_station(code)
        for H in [1, 24]:
            res = evaluate_station_horizon(h, code, name, H)
            records.append(res)
    
    df_res = pd.DataFrame(records)
    out_csv = os.path.join(OUT_DIR, "paper1_10station_forecasting_benchmark.csv")
    df_res.to_csv(out_csv, index=False)
    print(f"\n[OK] Results saved to {out_csv}")

    for H in [1, 24]:
        sub = df_res[df_res["Horizon_h"] == H]
        print(f"\n--- Summary for Horizon H = {H}h (10-Station Compliant Mean +/- SD) ---")
        for model in ["Persistence", "Ridge", "HGBT"]:
            m_r2 = sub[f"{model}_R2"].mean()
            s_r2 = sub[f"{model}_R2"].std()
            m_rmse = sub[f"{model}_RMSE"].mean()
            s_rmse = sub[f"{model}_RMSE"].std()
            m_mae = sub[f"{model}_MAE"].mean()
            s_mae = sub[f"{model}_MAE"].std()
            print(f"  {model:12s}: R2 = {m_r2:.4f} +/- {s_r2:.4f} | RMSE = {m_rmse:.2f} +/- {s_rmse:.2f} | MAE = {m_mae:.2f} +/- {s_mae:.2f}")

if __name__ == "__main__":
    main()
