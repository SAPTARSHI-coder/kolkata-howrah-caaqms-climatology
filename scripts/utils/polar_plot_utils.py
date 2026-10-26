"""
Bivariate Polar Plot Kernel Density Utilities
Implements Carslaw and Ropkins (2012) kernel-smoothed bivariate polar concentration surfaces:
  C_bar(u, theta) = sum(w_i * C_i) / sum(w_i)
where w_i is a 2D Gaussian kernel on radial wind speed (u) and wind direction (theta).
"""
import numpy as np

def compute_kernel_polar_surface(ws, wd, conc, u_max=4.5, n_u=50, n_theta=90, h_u=0.45, h_theta_deg=18.0, min_weight=4.0):
    """
    Computes a continuous concentration surface as a joint function of wind speed (u) and direction (theta).
    
    Parameters:
      ws (array-like): Wind speed in m/s
      wd (array-like): Wind direction in degrees (0 = North, 90 = East, etc.)
      conc (array-like): Observed concentration (e.g. PM2.5 in ug/m3)
      u_max (float): Maximum wind speed radius
      n_u (int): Number of radial bins
      n_theta (int): Number of angular bins
      h_u (float): Radial Gaussian bandwidth in m/s
      h_theta_deg (float): Angular Gaussian bandwidth in degrees
      min_weight (float): Minimum kernel weight threshold to prevent edge extrapolation
      
    Returns:
      TH_G (2D array): Meshgrid of wind direction in radians
      U_G (2D array): Meshgrid of wind speed in m/s
      C_surf (2D array): Estimated concentration surface
    """
    valid = np.isfinite(ws) & np.isfinite(wd) & np.isfinite(conc) & (ws >= 0.1) & (ws <= 35.0) & (conc > 0)
    ws_v = np.asarray(ws)[valid]
    wd_v = np.asarray(wd)[valid]
    c_v = np.asarray(conc)[valid]

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
            if w_sum >= min_weight:
                C_surf[i, j] = np.sum(w * c_v) / w_sum
            else:
                C_surf[i, j] = np.nan
    return TH_G, U_G, C_surf
