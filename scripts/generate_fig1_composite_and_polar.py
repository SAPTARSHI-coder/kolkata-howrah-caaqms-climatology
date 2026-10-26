"""
Generate Figure 1 (Multi-Scale Study Area Map) and Figure 5 (Bivariate Polar Surfaces)
Paper 1: Continuous Observational Climatology and Trans-Hooghly Directional Transport
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
DATA_DIR = os.path.join(BASE_DIR, "data", "Cleaned_Station_Data")
GIS_DIR = os.path.join(BASE_DIR, "gis_layers")
OUT_FIG_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(OUT_FIG_DIR, exist_ok=True)

def generate_fig1_composite():
    print("[1/2] Generating Figure 1 Composite Study Area Map...")
    p1 = os.path.join(GIS_DIR, "01_india_national_context.png")
    p2 = os.path.join(GIS_DIR, "02_west_bengal_regional_context.png")
    p3 = os.path.join(GIS_DIR, "03_kolkata_howrah_selected_locations.png")
    
    if not (os.path.exists(p1) and os.path.exists(p2) and os.path.exists(p3)):
        raise FileNotFoundError("Missing source GIS maps in gis_layers/ folder.")
    
    im1 = Image.open(p1).convert("RGB")
    im2 = Image.open(p2).convert("RGB")
    im3 = Image.open(p3).convert("RGB")
    
    fig = plt.figure(figsize=(12, 13.5), dpi=300)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.45], hspace=0.10, wspace=0.06)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.imshow(im1)
    ax1.axis('off')
    ax1.set_title('(a) National Context: India', fontsize=12, fontweight='bold', pad=6)

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.imshow(im2)
    ax2.axis('off')
    ax2.set_title('(b) Regional Context: West Bengal', fontsize=12, fontweight='bold', pad=6)

    ax3 = fig.add_subplot(gs[1, :])
    ax3.imshow(im3)
    ax3.axis('off')
    ax3.set_title('(c) Local Study Area: Kolkata–Howrah CAAQMS Monitoring Locations', fontsize=13, fontweight='bold', pad=8)

    plt.subplots_adjust(top=0.96, bottom=0.02, left=0.02, right=0.98)
    out_path = os.path.join(OUT_FIG_DIR, "fig1_study_area_map.png")
    plt.savefig(out_path, dpi=300, facecolor='white', bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved to: {out_path}")

def compute_kernel_polar_surface(ws, wd, conc, u_max=4.5, n_u=50, n_theta=90, h_u=0.45, h_theta_deg=18.0):
    valid = np.isfinite(ws) & np.isfinite(wd) & np.isfinite(conc) & (ws >= 0.1) & (ws <= 25.0) & (conc > 0)
    ws_v = ws[valid]
    wd_v = wd[valid]
    c_v = conc[valid]

    u_grid = np.linspace(0.1, u_max, n_u)
    theta_deg_grid = np.linspace(0.0, 360.0, n_theta, endpoint=False)
    theta_rad_grid = np.radians(theta_deg_grid)

    U_G, TH_G = np.meshgrid(u_grid, theta_rad_grid)
    C_surf = np.zeros_like(U_G)

    h_theta = np.radians(h_theta_deg)
    h_theta_sq = 2.0 * (h_theta ** 2)
    h_u_sq = 2.0 * (h_u ** 2)

    wd_rad_v = np.radians(wd_v)
    for i in range(n_theta):
        th = theta_rad_grid[i]
        d_th = np.abs(wd_rad_v - th)
        d_th = np.minimum(d_th, 2.0 * np.pi - d_th)
        w_th = np.exp(-(d_th ** 2) / h_theta_sq)
        for j in range(n_u):
            u = u_grid[j]
            d_u = ws_v - u
            w_u = np.exp(-(d_u ** 2) / h_u_sq)
            w = w_th * w_u
            w_sum = np.sum(w)
            if w_sum > 4.0:
                C_surf[i, j] = np.sum(w * c_v) / w_sum
            else:
                C_surf[i, j] = np.nan
    return TH_G, U_G, C_surf

def generate_fig5_polar_surfaces():
    print("[2/2] Generating Figure 5 Bivariate Polar Concentration Surfaces...")
    sites = [
        ("GH", "Ghusuri (Howrah Heavy Industrial Core)"),
        ("VC", "Victoria Memorial (Central Kolkata Cultural/Green)"),
        ("FW", "Fort William (Central Kolkata Urban Core)")
    ]

    station_dfs = {}
    for code, _ in sites:
        f24 = os.path.join(DATA_DIR, f"{code}_2024_MLL.xlsx")
        f25 = os.path.join(DATA_DIR, f"{code}_2025_MLL.xlsx")
        dfs = []
        if os.path.exists(f24):
            dfs.append(pd.read_excel(f24))
        if os.path.exists(f25):
            dfs.append(pd.read_excel(f25))
        df_comb = pd.concat(dfs, ignore_index=True)
        df_comb['DateTime'] = pd.to_datetime(df_comb['DateTime'])
        df_comb = df_comb.set_index('DateTime')
        station_dfs[code] = df_comb

    fig, axes = plt.subplots(2, 3, figsize=(15, 9.8), subplot_kw=dict(projection="polar"), dpi=300)
    fig.suptitle("Bivariate Polar Concentration Surfaces: Winter Advection vs. Monsoonal Ventilation",
                 fontsize=14, fontweight="bold", y=0.98)

    seasons = [
        ("Winter (Nov–Feb)", [11, 12, 1, 2], 20, 145, "YlOrRd"),
        ("Monsoon (Jun–Sep)", [6, 7, 8, 9], 5, 45, "YlOrRd"),
    ]

    for row_idx, (season_label, months, vmin, vmax, cmap_name) in enumerate(seasons):
        for col_idx, (code, title) in enumerate(sites):
            ax = axes[row_idx, col_idx]
            ax.set_theta_zero_location("N")
            ax.set_theta_direction(-1)
            ax.set_facecolor("#fefce8")

            df = station_dfs[code]
            sub = df[df.index.month.isin(months)]

            TH_G, U_G, C_surf = compute_kernel_polar_surface(
                sub["WS"].values, sub["WD"].values, sub["PM2.5"].values,
                u_max=4.5, n_u=50, n_theta=90, h_u=0.45, h_theta_deg=18.0
            )

            mappable = ax.pcolormesh(TH_G, U_G, C_surf, cmap=cmap_name,
                                     vmin=vmin, vmax=vmax, shading="gouraud")

            levels = np.linspace(vmin, vmax, 6)
            ax.contour(TH_G, U_G, np.nan_to_num(C_surf, nan=vmin),
                       levels=levels, colors="black", linewidths=0.4, alpha=0.35)

            ax.set_ylim(0, 4.5)
            ax.set_yticks([1.0, 2.5, 4.0])
            ax.set_yticklabels(["1 m/s", "2.5", "4 m/s"], fontsize=7.5, color="#334155")
            ax.set_rlabel_position(32)
            ax.set_xticks(np.radians([0, 45, 90, 135, 180, 225, 270, 315]))
            ax.set_xticklabels(["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
                               fontsize=8.5, fontweight="bold")
            ax.grid(True, linestyle="--", linewidth=0.5, color="#475569", alpha=0.5)

            if row_idx == 0:
                ax.set_title(title, fontsize=10, fontweight="bold", pad=14)

        cbar_ax = fig.add_axes([0.92, 0.54 - row_idx * 0.44, 0.014, 0.36])
        cb = fig.colorbar(mappable, cax=cbar_ax)
        cb.set_label(rf"{season_label}" + "\n" + r"$PM_{2.5}$ ($\mu\mathrm{g}\ \mathrm{m}^{-3}$)",
                     fontsize=9.5, fontweight="bold", labelpad=8)
        cb.ax.tick_params(labelsize=8)

    plt.subplots_adjust(left=0.04, right=0.90, top=0.91, bottom=0.05, wspace=0.25, hspace=0.22)
    out_path = os.path.join(OUT_FIG_DIR, "fig5_bivariate_polar_surfaces.png")
    plt.savefig(out_path, dpi=300, facecolor="white", bbox_inches="tight")
    plt.close()
    print(f"  [OK] Saved to: {out_path}")

def main():
    generate_fig1_composite()
    generate_fig5_polar_surfaces()
    print("[ALL DONE] Figure 1 and Figure 5 successfully created.")

if __name__ == "__main__":
    main()
