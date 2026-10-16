# Global Forest Area Change & Sustainability Dashboard — Stage 1

## 📌 Project Overview
- **Project Title:** Global Forest Area Change and Forest Sustainability Analysis
- **Dashboard Title:** Global Forest Area Change & Sustainability Dashboard
- **Subtitle:** *Exploring forest trends, degradation, restoration, and sustainability using forest datasets.*
- **Course:** Data Visualization Lab (DV_LAB_Forest)
- **Current Milestone:** Stage 1 — Baseline Interactive Architecture, KPI Cards, Initial Visualizations, and Dataset Diagnostics

---

## 🏗️ Architecture & Created Files

| File | Purpose |
| :--- | :--- |
| [`app.py`](file:///c:/Users/user/Desktop/DV_LAB_Forest/app.py) | **Main application entrypoint**. Implements the Streamlit interface, responsive layout, sidebar navigation, dynamic filter controls, KPI cards, and view routing. |
| [`data_loader.py`](file:///c:/Users/user/Desktop/DV_LAB_Forest/data_loader.py) | **Data ingestion and transformation engine**. Caches dataset reading (`@st.cache_data`), parses and cleans numeric indicators, provides dynamic filtering, metric calculations, and generates full dataset inventory metadata. |
| [`visualizations.py`](file:///c:/Users/user/Desktop/DV_LAB_Forest/visualizations.py) | **Chart generation module**. Implements 5 interactive Plotly visualizations with a consistent dark forest-green visual theme, tooltips, responsive margins, and empty-state fallbacks. |
| [`styles.py`](file:///c:/Users/user/Desktop/DV_LAB_Forest/styles.py) | **Custom design system and CSS styling**. Injects Google Fonts (Inter, Outfit), dark forest-green gradient banners, glassmorphism badges, modern metric cards, and responsive container rules. |
| [`.streamlit/config.toml`](file:///c:/Users/user/Desktop/DV_LAB_Forest/.streamlit/config.toml) | **Streamlit runtime & theme configuration**. Sets primary forest colors (`#2d6a4f`), off-white backgrounds (`#F8FAF8`), and server settings. |
| [`requirements.txt`](file:///c:/Users/user/Desktop/DV_LAB_Forest/requirements.txt) | **Dependencies manifest** (`pandas`, `streamlit`, `plotly`, `numpy`). |

---

## 🚀 How to Run the Dashboard

### 1. Install Dependencies
Open your PowerShell or terminal in the project directory (`DV_LAB_Forest`) and run:
```powershell
pip install -r requirements.txt
```

### 2. Launch the Streamlit Dashboard
```powershell
streamlit run app.py
```
The application will launch and automatically open in your browser at:
```
http://localhost:8501
```

---

## 📊 Dataset Inspection & Findings (from `README.txt` & CSVs)

The data source is the **official Food and Agriculture Organization (FAO) Global Forest Resources Assessment (FRA) 2025/2026 reporting round** (Export date: October 16, 2026).

### Dataset Audit Summary:

| Dataset | Category | Rows | Columns | Missing Values | Key Observations & Contents |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `FRA_Years_2026-10-16.csv` | Core Forest Area & Dynamics | 1,416 | 235 | 22.1% | 236 countries across 6 milestone years (1990, 2000, 2010, 2015, 2020, 2025). Surface areas in 1,000 ha. Covers forest area, land area, naturally regenerating forest, planted forest, primary forest, growing stock, biomass, and carbon. |
| `Intervals_2026-10-16.csv` | Interval Rates | 1,180 | 17 | 20.0% | Annual average rates (1,000 ha/year) for 5 periods: 1990–2000, 2000–2010, 2010–2015, 2015–2020, 2020–2025. Covers expansion, afforestation, natural expansion, and deforestation. |
| `Annual_2026-10-16.csv` | Disturbances | 5,664 | 21 | 25.3% | Annual disturbance time series (2000–2023) covering insect damage, diseases, severe weather, and forest/land burned areas. |
| `DegradedForest_2026-10-16.csv` | Degradation | 236 | 16 | 34.0% | Qualitative country reporting on degradation definitions, monitoring systems, and criteria (many empty quantitative fields; qualitative text in national languages). |
| `ForestRestoration_2026-10-16.csv` | Restoration | 236 | 14 | 24.3% | National commitments, legislation mandates, restoration targets, and hectares restored to date (152 countries report restoration commitments). |
| `ForestPolicy_2026-10-16.csv` | Policy & Governance | 236 | 16 | 12.6% | SFM policies (192 countries), legislation (199 countries), stakeholder platforms (151 countries), and traceability systems (102 countries). |
| `NWFP_2026-10-16.csv` | Non-Wood Products | 236 | 60 | 56.1% | Top 10 non-wood forest products per country by quantity, category, and local currency economic value. |
| `NDPYear_2026-10-16.csv` | National Data Points | 236 | 15 | 12.8% | Earliest and latest national inventory years; methodologies used (NFI, remote sensing, cartographic mapping). |
| `Tiers_2026-10-16.csv` | Data Quality Tiers | 236 | 11 | 5.0% | FAO data quality ratings (Tier 1: low, Tier 2: medium, Tier 3: high) for status and trend of forest area, growing stock, and biomass. |

### Observations on Observation Status Codes ("Flags"):
- **A**: Normal value, official country reported data.
- **I**: Imputed value (desk study or FAO expert compilation).
- **M**: Missing value (undefined or denominator zero).
- **O**: Missing value (unreported).

---

## 📈 Visualizations Status

All 5 required Stage 1 charts are implemented with real data and verified:

1. **Line Chart — Forest Area Trends Over Time (1990–2025)**:
   - **Status:** **Fully Working**
   - **Data:** Plotted from `FRA_Years_2026-10-16.csv`. Supports aggregate total, regional breakdown, and country breakdown.
2. **Bar Chart — Country & Regional Comparison**:
   - **Status:** **Fully Working**
   - **Data:** Plotted from `FRA_Years_2026-10-16.csv`. Supports two modes: (1) Top 10 countries by forest area in any selected year, and (2) Top net forest gainers vs losers (1990 to target year) with green/crimson color coding.
3. **Histogram — Numeric Forest Variable Distribution**:
   - **Status:** **Fully Working**
   - **Data:** Plotted from `FRA_Years_2026-10-16.csv`. Includes interactive variable selector and log-scale toggle to handle skewed country sizes.
4. **Correlation Heatmap — Forest Indicator Correlations**:
   - **Status:** **Fully Working**
   - **Data:** Computes Pearson correlation matrix across 8 core biophysical variables (Forest Area, Land Area, Biomass, Carbon, Protected Area, etc.).
5. **Choropleth Map — Global Geographic Distribution**:
   - **Status:** **Fully Working**
   - **Data:** Plotted using `iso3` country identifiers. Displays either Total Forest Area (Million ha) or Forest Cover Percentage (% of Land Area).

### Charts Requiring Additional Preparation for Later Stages:
- **Annual Disturbance Trends (Fire, Weather, Insects)**: The raw data in `Annual_2026-10-16.csv` has significant missingness for smaller countries and requires country-level imputation or regional aggregation before displaying in Stage 2.
- **Degraded Forest Area Comparison**: Most countries in `DegradedForest_2026-10-16.csv` provided qualitative descriptions rather than numeric hectares. Only 66 countries have national definitions and ~30 reported numeric areas. Stage 2 will extract text indicators or display qualitative policy status cards.
- **NWFP Economic Valuation**: Values are reported in local national currencies without standard USD conversion rates. A currency conversion step will be needed in Stage 2 to compare product values globally.

---

## 🎯 Stage 1 Completion Checklist
- [x] Full folder and dataset inspection completed
- [x] `README.txt` reviewed and cited accurately
- [x] Clean, modern environmental theme designed (dark forest-green accents, light backgrounds)
- [x] Header banner with title, subtitle, source, and verified date
- [x] 4 Dynamic KPI cards linked to real data with proper fallbacks
- [x] 5 Interactive Plotly visualizations connected to real CSV data
- [x] Responsive sidebar filters (Region, Country, Year, Baseline)
- [x] Complete dataset diagnostics section with inventory table and interactive dataset explorer
- [x] Modular Python code (`app.py`, `data_loader.py`, `visualizations.py`, `styles.py`)
- [x] Zero modification of original CSV datasets
- [x] Smoke-tested and verified working without errors
