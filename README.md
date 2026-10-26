# Continuous Observational Climatology and Trans-Hooghly Directional Transport across the Kolkata–Howrah Conurbation

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Target: Urban Climate](https://img.shields.io/badge/Journal-Urban%20Climate%20(Elsevier%2C%20Q1)-0073B1.svg)](https://www.sciencedirect.com/journal/urban-climate)

This repository contains the complete open-source reproducibility pipelines, quality-controlled datasets, GIS layers, and analysis scripts accompanying the research manuscript:

> **"Continuous Observational Climatology and Trans-Hooghly Directional Transport across the Kolkata–Howrah Conurbation: A Multi-Station Ground Investigation across 13 CAAQMS Stations"**  
> **Author:** Saptarshi Sadhu (Sole Author)  
> **Affiliation:** Adamas University, Kolkata 700126, West Bengal, India  
> **Correspondence:** `saptarshi1.sadhu@stu.adamasuniversity.ac.in` | `saptarshisadhuofficial@gmail.com`  
> **Target Journal:** *Urban Climate* (Elsevier, Q1, Impact Factor: 6.0, CiteScore: 10.3)

---

## 📌 Research Overview

The Kolkata–Howrah conurbation forms the primary metropolitan growth center along the lower Indo-Gangetic Plain (IGP) before its estuarine discharge into the Bay of Bengal. This study establishes a continuous multi-station observational climatology across all 13 Continuous Ambient Air Quality Monitoring System (CAAQMS) stations operated by the Central Pollution Control Board (CPCB) and West Bengal Pollution Control Board (WBPCB) across calendar years 2024 and 2025 (**721,193 validated 15-minute multi-parameter records across 26 station-years**).

### Core Scientific Contributions:
1. **Statutory Completeness Auditing:** Resolves regulatory bias wherein industrial hotspots (e.g., Dasnagar at 69.8% capture) are omitted from official non-attainment compliance reporting despite severe winter particulate exceedances.
2. **Thermodynamic Scale Amplification:** Quantifies the strengthening of particulate–meteorology coupling between 15-minute telemetry ($r_s = -0.48$) and daily synoptic means ($r_s = -0.61$) using autocorrelation-adjusted effective sample sizes ($N_{\text{eff}} \approx 7,280$ vs. $N_{\text{eff}} \approx 155$).
3. **Trans-Hooghly Directional Transport:** Maps kernel-smoothed bivariate polar concentration surfaces ($\bar{C}(u, \theta)$) demonstrating winter trans-river advection of heavy industrial plumes from West-Bank foundries into East-Bank residential zones under calm winds ($<1.5\,\text{m s}^{-1}$).
4. **Leak-Free Chronological Forecasting:** Establishes forward-chaining 1-hour and 24-hour predictive benchmarks across all 10 compliant stations ($R^2 = 0.6842 \pm 0.0706$ 24-h Ridge; reaching $R^2 = 0.7187$ at Ballygunge).

---

## 🗺️ Monitoring Network Archetypes (13 Stations)

| Code | Station Name | Bank | Latitude (°N) | Longitude (°E) | Functional Microclimatic Archetype |
|:---:|:---|:---:|:---:|:---:|:---|
| **BG** | Ballygunge | East | 22.5264 | 88.3692 | Commercial / High-Density Residential |
| **BM** | Belur Math | West | 22.6362 | 88.3521 | Industrial / Suburban Riverine Interface |
| **BN** | Bidhannagar | East | 22.5802 | 88.4331 | Traffic / Information Technology Corridor |
| **BOG** | Botanical Garden | West | 22.5473 | 88.2941 | Green Ecological Background / River Bank |
| **DN** | Dasnagar | West | 22.5921 | 88.3053 | Heavy Industrial / Metal Casting Basin |
| **FW** | Fort William | East | 22.5532 | 88.3444 | Green Urban Core / Defence Reservation |
| **GH** | Ghusuri | West | 22.5824 | 88.3163 | Heavy Industrial / Foundries & Rolling Mills |
| **JD** | Jadavpur | East | 22.4991 | 88.3713 | Mixed Commercial / Residential / Academic |
| **PP** | Padmapukur | West | 22.5651 | 88.3072 | Industrial / Suburban Water Works Corridor |
| **RBU** | Rabindra Bharati Univ. | East | 22.5932 | 88.3724 | Arterial Highway / Heavy Diesel Corridor |
| **RS** | Rabindra Sarovar | East | 22.5083 | 88.3582 | Urban Waterbody / Ecological Buffer |
| **SVSPA** | Barrackpore (SVSPA) | North | 22.7661 | 88.3644 | Northern Peri-Urban / Suburban Outpost |
| **VC** | Victoria Memorial | East | 22.5441 | 88.3432 | Heritage / Protected Urban Park Receptor |

---

## 📁 Repository Directory Structure

```text
kolkata-howrah-caaqms-climatology/
├── README.md                          <-- Master Documentation
├── LICENSE                            <-- MIT License
├── requirements.txt                   <-- Python package dependencies
├── environment.yml                    <-- Conda environment specification
├── .gitignore                         <-- Git exclusion rules
│
├── data/
│   ├── Cleaned_Station_Data/          <-- 26 station-year Excel datasets (2024 & 2025)
│   ├── master_station_metadata.csv    <-- Coordinates, archetypes, and elevation
│   └── benchmarks/                    <-- Chronological forecasting benchmark tables
│       ├── paper1_10station_forecasting_benchmark.csv
│       ├── paper1_forecasting_benchmark_results.csv
│       └── paper1_proof_results.csv
│
├── figures/                           <-- High-resolution publication artwork (300 DPI)
│   ├── fig1_study_area_map.png        (Composite 3-panel study area map)
│   ├── fig2_temporal_dynamics.png     (Monthly dynamics & PM2.5/PM10 ratio)
│   ├── fig3_diurnal_profiles.png      (Diurnal profiles by archetype)
│   ├── fig4_correlation_and_scale.png (Correlation heatmap & scale amplification)
│   └── fig5_bivariate_polar_surfaces.png (Polar transport surfaces)
│
├── gis_layers/                        <-- Source GIS map panels
│   ├── 01_india_national_context.png
│   ├── 02_west_bengal_regional_context.png
│   └── 03_kolkata_howrah_selected_locations.png
│
└── scripts/
    ├── run_10station_forecasting_benchmark.py  <-- 1-h & 24-h chronological benchmark
    ├── generate_fig1_composite_and_polar.py    <-- Builds Fig 1 & Fig 5
    ├── generate_paper1_figures.py              <-- Builds Fig 2, Fig 3, Fig 4
    └── utils/
        ├── qc_pipeline.py          <-- 3-tier QC (physical, freezing, gap filling)
        ├── polar_plot_utils.py     <-- Carslaw & Ropkins bivariate polar KDE
        └── statistical_utils.py    <-- Autocorrelation-adjusted N_eff & Fisher CIs
```

---

## 🚀 Quick Start & Installation

### Option 1: Using Conda (Recommended)

```bash
git clone https://github.com/SAPTARSHI-coder/kolkata-howrah-caaqms-climatology.git
cd kolkata-howrah-caaqms-climatology
conda env create -f environment.yml
conda activate kolkata-caaqms
```

### Option 2: Using standard `pip`

```bash
git clone https://github.com/SAPTARSHI-coder/kolkata-howrah-caaqms-climatology.git
cd kolkata-howrah-caaqms-climatology
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

---

## 📊 Reproducing Manuscript Results & Figures

All scripts use self-contained relative paths (`os.path`) and execute from any working directory:

### 1. Run the 10-Station Forecasting Benchmark (Table 5 & Section 3.6)
Evaluates 1-hour and 24-hour day-ahead forecasting using strictly chronological forward-chaining (Train: 2024; Test: 2025):
```bash
python scripts/run_10station_forecasting_benchmark.py
```
*Outputs summary metrics and saves `data/benchmarks/paper1_10station_forecasting_benchmark.csv`.*

### 2. Generate Figure 1 & Figure 5 (Polar Transport Surfaces)
Builds the composite multi-scale GIS map and computes kernel-smoothed bivariate polar concentration surfaces:
```bash
python scripts/generate_fig1_composite_and_polar.py
```
*Outputs `figures/fig1_study_area_map.png` and `figures/fig5_bivariate_polar_surfaces.png`.*

### 3. Generate Figures 2, 3, and 4
Generates the monthly temporal dynamics, diurnal profiles, and multi-scale correlation heatmap:
```bash
python scripts/generate_paper1_figures.py
```

---

## 🔬 Scientific Data Provenance & Quality Control

The raw 15-minute telemetry was collected from the Central Pollution Control Board (CPCB) official portal (https://airquality.cpcb.gov.in) and screened through a standardized 3-tier protocol:
1. **Tier 1 (Physical Plausibility):** Out-of-range concentrations, sensor diagnostic errors, and unrealistic extremes ($>1000\,\mu\text{g m}^{-3}$) flagged and masked.
2. **Tier 2 (Sensor Freezing & Rate-of-Change):** Frozen sensors ($\ge 6$ consecutive hours of identical readings) and uncorroborated single-step jumps ($>150\,\mu\text{g m}^{-3}\,\text{h}^{-1}$) removed.
3. **Tier 3 (Short-Gap Repair):** Isolated missing intervals $\le 3$ hours linearly interpolated; multi-day outages preserved explicitly to avoid variance dampening.

---

## 📜 Citation

If you use this code or dataset in your research, please cite:

```bibtex
@article{sadhu2026urbanclimate,
  title={Continuous Observational Climatology and Trans-Hooghly Directional Transport across the Kolkata--Howrah Conurbation: A Multi-Station Ground Investigation across 13 CAAQMS Stations},
  author={Sadhu, Saptarshi},
  journal={Urban Climate},
  year={2026},
  publisher={Elsevier},
  note={Under Review}
}
```

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
# kolkata-howrah-caaqms-climatology
